import bpy
import bmesh
import pandas as pd
import numpy as np
import sys
import os
import matplotlib as plt
from pyproj import Transformer,Proj
import math
from tqdm.auto import tqdm
# import BlenderGIS as bgis
# from BlenderGIS.geoscene import GeoScene, GEOSCENE_OT_coords_viewer
class InvalidFileException(Exception):
    'File must be a .csv or .xslx'
    pass

class LoadFileOperator(bpy.types.Operator):
    bl_idname = "object.load_file"
    bl_label = "Launch File Loader"

    def execute(self, context):
        scene=context.scene
        scene['HoleData']=None
        scene['Headers']=None
        scene['Sheet_names']=None
        scene['Data_dir']=None
        scene['Header_dir']=None
        scene['sheet_selection']='None'
        scene['render_cols']=['collar','x','y','z','dip','azimuth','holeradius','rendercol','colormap']
        for x in scene['render_cols']:
            scene[x]='None'

        file_path = scene.file_path
        print('------------------------------------------------------------')
        print('Load File')
        print(file_path)
        print('-------------------------------------')
        # Do something with the file path here
        self.import_data(context)
        print('------------------------------------------------------------')

        if scene['Headers']!=None:
            scene['show_data_panel']=True
            
        if scene['Sheet_names']!=None:
            scene['show_sheet_panel']=True
            
        return {'FINISHED'}

    def import_data(self,context):
        scene=context.scene
        filepath= context.scene.file_path

        if filepath.endswith('.csv'):
            data=pd.read_csv(skip_blank_lines=True)
            headers=data.headers
            print('-----------------------')
            print('Headers:')
            print(headers)
            print('-----------------------')

            scene['HoleData']=data
            scene['Headers']=headers

        if filepath.endswith('.xlsx'):
            sheet=pd.ExcelFile(filepath)

            sheet_names=sheet.sheet_names
            print('##########')
            print('Sheet Names:')
            print(sheet_names)
            print('##########')

            data_list=sheet_names
            data_dir={sheet:pd.read_excel(filepath,sheet_name=sheet) for sheet in data_list}
            header_dir={sheet:[c for c in data_dir[sheet].columns] for sheet in data_list}

            data_save={sheet:data_dir[sheet].to_json() for sheet in data_dir}

            print('##### SAVE SHEET NAMES #####')
            scene['Sheet_names']=sheet_names
            scene['Data_dir']=data_save
            scene['Header_dir']=header_dir

        else:
            raise InvalidFileException
          
class ChooseColumnsOperator(bpy.types.Operator):
    bl_idname = "object.get_columns"
    bl_label = "Choose Header Columns" 

    def execute(self,context):
        print('########## MAKE COLUMN DROP DOWN ##########')
        # Set the custom property to the value entered by the user

        context.scene['show_data_panel']=True
        return {'FINISHED'}
  
class ChooseSheetOperator(bpy.types.Operator):
    bl_idname = "object.get_sheet"
    bl_label = "Get Sheet"

    def execute(self, context):
        print('########## GET SHEET, MAKE SHEET DROP DOWN ##########')


        scene=context.scene
        sheet_names=scene['Sheet_names']
        return {'FINISHED'}

class ResetOperator(bpy.types.Operator):

    bl_idname = "object.reset_tool"
    bl_label = "Reset Tool"
    def execute(self, context):
        scene=context.scene
        scene['HoleData']=None
        scene['Headers']=None
        scene['Sheet_names']=None
        scene['Data_dir']=None
        scene['Header_dir']=None
        scene['render_cols']=['Collar','x','y','z','Render']
        scene['show_data_panel']=False
        scene['show_sheet_panel']=False
        return {'FINISHED'}

class RenderOperator(bpy.types.Operator):

    bl_idname = "object.render_holes"
    bl_label = "Render Drill Holes"


    def __init__(self):
        
        self.context=None
                
    def execute(self, context):
        # print (dir(bpy.ops.bgis))
        print('############## Begin Render ############')
        print('------------------------------------------')
        
        # bpy.ops.bgis.add_predef_crs(1)
        # bpy.ops.geoscene.init_org()
        scene=context.scene
        self.context=context
        selection_options=[]
        for x in scene['render_cols']:
            print(x,scene[x])
            selection_options.append(scene[x])
        data=scene['HoleData']
        data = pd.read_json(data)
        # print(data)
        #grab corindates from specified columns
        cord_cols=[scene['x'],scene['y'],scene['z']]
        rot_cols=[scene['azimuth'],scene['dip']]

        render_col=scene['rendercol']
        cmap=scene['colormap']
        collar_col=scene['collar']
        volume=scene['holeradius']
        
        # rot_cols=[scene['dip'],scene['azimuth']]
        ## drop na depths and locations
        data=self.drop_bad_rows(data=data,cols=cord_cols
                                    # +rot_cols
                                    )

        
        print('COLLAR COLUMNS:',collar_col)
        groups=data.groupby(collar_col)
        print('Selected_options',selection_options)
        print('XYZ=',cord_cols)
        print('Rotations=',cord_cols)
        print('hole_size :',volume)
        # scene['show_data_panel']=False
        # scene['show_sheet_panel']=False

        ### normalize the color mapping
        
        if cmap=='None':
            cmap='coolwarm'

        if render_col=='None':
            render_col=scene['z']

        try:volume=float(volume)
        except:volume=1
        
        for i,col in enumerate(rot_cols):
            if col=='None':
                data[f'rot_{i}']=0
                rot_cols[i]=f'rot_{i}'

        print('render_using:',render_col)
        print('Colormap:',cmap)
        mean=data[render_col].mean()
        std=data[render_col].std()
        min=data[render_col].min()
        max=data[render_col].max()
        upper=mean+std
        lower=mean-std
        colormap= MplColorHelper(cmap_name=cmap,start_val=lower,stop_val=upper)

        print(f'{render_col} Column Stats:')
        print('Mean:',mean,'Std:',std,'Min:',min,'Max:',max)
        print('Lower Bound:',lower,'Upper Bound:',upper)

        str_cols=data.select_dtypes(object).columns.to_list()
        num_cols=data.select_dtypes(np.number).columns.to_list()
        view_layer = bpy.context.view_layer

        print('------------------------------------------')
        print ('String dtypes')
        print(str_cols)
        print('------------------------------------------')
        print ('Numeric dtypes') 
        print(num_cols)
        colormaps={}

        ## print column stats and make the color maps
        for n in num_cols:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.')
            mean=data[n].mean()
            std=data[n].std()
            min=data[n].min()
            max=data[n].max()
            upper=mean+std
            lower=mean-std
            print(f'{n} Columns Stats')
            print('Mean:',mean,'Std:',std,'Min:',min,'Max:',max)
            print('Lower Bound:',lower,'Upper Bound:',upper)
            colormap= MplColorHelper(cmap_name=cmap,start_val=min,stop_val=max)
            colormaps[n]=colormap
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.')

        ## check the variable we need to render
        if scene['sheet_selection']!=None:
        #make a collection for the data
            collection_name=scene['sheet_selection']
        
        else:
            collection_name=scene["File Path"].split('/')[-1]

        sheet_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(sheet_collection)
        
        
        ## lop through all the drill holes
        for drillgroup in groups:
            #grab the data and the name
            collar_name=drillgroup[0]
            group=drillgroup[1].reset_index(drop=True)
            print(f'################# Start Drill hole {collar_name}########################')
            print(collar_name)   
            

            #### add a new collection to store the spheres
            collar_collection = bpy.data.collections.new(f'{collar_name}')
            sheet_collection.children.link(collar_collection)

            
            ## grab the cords from the data
            cord_data=group[cord_cols]
            rot_data=group[rot_cols]
            coords=self.get_cords(cord_data)
            sizes=self.get_sizes(cord_data,cord_cols[-1])
            rots=self.get_rots(rot_data)

            # # # ake one big tube. Takes to long to color
            hole_curve,hole_mesh=self.make_one_big_hole(name=collar_name,
                                            coords=coords,
                                            volume=volume,
                                            collar_collection=collar_collection,
                                            data=group,
                                            num_columns=num_cols,
                                            color_maps=colormaps
                                            )

            hole_curve=self.generate_spline_colors(
                                                name=collar_name,
                                                curve=hole_mesh,
                                                data=group,
                                                render_col=render_col,
                                                coords=coords,
                                                colormaps=colormaps )



        print('--------------------------------')
        print('Finished Render')
        return{'FINISHED'}

    def get_cords(self,data):
        print('######## Get Cords ########')
        
        all_cords=[]
        data=data.values
        trans = Transformer.from_crs(3857, 4326, always_xy=True)
        num_cords=data.shape[0]
        num_cords=data.shape[0]
        for i in range(num_cords):
            row=data[i,:]
            row=[r for r in row]
            x,y,z=row[0],row[1],row[2]

            cords=tuple([c for c in row])
            last_z=z
            all_cords.append(cords)
        print('cord len:',len(all_cords))
        return all_cords

    def get_rots(self,data):
        print('######## GET ROTATIONS ########')

        all_rots=[]
        data=data.values
        num_cords=data.shape[0]
        for i in range(num_cords):
            row=data[i,:]
            dip=row[0]
            azi=row[1]
            if dip==np.nan:
                dip=0.
            if azi==np.nan:
                azi=0
            rot=[0,dip,0]
            rots=tuple([math.radians(x) for x in rot])
            all_rots.append(rots)
        print('rots len',len(all_rots))
        return all_rots
    
    def get_sizes(self,data,zcol):
        print('######## GET SIZES  ########')

        sizes=data[[zcol]].diff().fillna(0).values
        sizes=[np.abs(c[0]) for c in sizes]
        
        print('size len:',len(sizes))
        return sizes

    def convert_radians(self,angle):


        if angle==0:
            rad=0
        else:
            rad=angle*np.pi/180
        return rad

    def drop_bad_rows(self,data,cols):
        print('##### Drop bad rows #####')
        for col in cols:
            try:
                drop_index=data[data[col].isna()].index
                data=data.drop(drop_index)
            except:pass
        return data
    
    def create_color_map(self,name,obj,data,zcol,):
        print('######## CREATE COLOR UV MAP########')

        mesh=obj.data
        uv_layer=mesh.uv_layers.new(name=f'color_map')
        uv_layer = mesh.uv_layers['color_map']


        color_idx=0
        #progress bar cuz it take a while
        n_faces=(len(mesh.loops))
        bar=tqdm(range(n_faces))
        bar.set_description(f'Processing {name}_colors')
        
        color_vertex_mapping={}
        color_idx=0
        color_vertex_mapping[color_idx]=[]
        for i,loop in enumerate(mesh.loops):
            bar.update(1)
            vert = mesh.vertices[loop.vertex_index]
            z=vert.co.z
            color_index=data[data[zcol]<=z].index
            uv_layer.data[loop.index].uv = (vert.co.x, vert.co.y)

            if len(color_index)>0:
                color_idx=int(color_index[-1])
                
            if color_idx not in color_vertex_mapping:
                color_vertex_mapping[color_idx]=[]

            color_vertex_mapping[color_idx].append(loop.vertex_index)

        mesh.update()


        return obj,color_vertex_mapping

    def create_str_attrs(self,columns,obj,data):
        for c in columns:
            try:
                ## update the attributes 
                str_layer = obj.data.vertex_layers_string.new(name=c)
                
                for i, row in data.iterrows():
                    str_layer.data[i].value=str(row[c]  ).encode()

            except Exception as e : print(f'Expcetion:{c}',e)
        return obj

    def create_num_attrs(self,columns,obj,data):
        for c in columns:
            try:
                ## update the attributes 
                float_layer = obj.data.polygon_layers_float.new(name=f'{c}_values')
                
                for i, row in data.iterrows():
                    i = int(i)
                    val=row[c]    
                    if val==np.nan:
                        val=-99
                    float_layer.data[i].value=val
            except Exception as e : print(f'Expcetion:{c}',e)
        return obj

    def create_color_attrs(self,columns,zcol,obj,data,colormaps):
        print('######## CREATE COLOR ATTRIBUTES########')
        
        for c in columns:
            print(f'float_colors {c}')
            colormap=colormaps[c]
            color_layer =obj.data.color_attributes.new(name=c,type='FLOAT_COLOR',domain='POINT')
            obj.data.update()
            try:
                ## update the attributes 
                bar=tqdm(data.iterrows())
                for i,row in bar:
                    bar.set_description(f'{c}')
                    val=row[c]  
                    loc=row[zcol] 
                    if val==np.nan:
                        val=0
                    colors=colormap.get_rgb(val)
                    color_layer.data[loc].color=colors

            except Exception as e : print(f'Exception:{c}',e)
            obj.data.update()
        return obj

    def make_tube(self,curve_obj,name,coords,radius,collar_collection):
        print('######## MAKE TUBE ########')
        
        # Create a tube that follows the curve
        bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=coords[0],enter_editmode=True, align='WORLD')

        
        circle=bpy.data.objects["BezierCircle"].copy()
        circle.name=f'{name}_start'
        collar_collection.objects.link(circle)
        bpy.context.view_layer.objects.active = circle

        # circle_obj = bpy.data.objects.new(name=name, object_data=circle)

        curve_obj.data.bevel_object = circle
        curve_obj.data.dimensions='3D'


        # curve_obj.data.extrude = 1

        curve_obj.data.bevel_factor_mapping_start = 'SEGMENTS'
        curve_obj.data.bevel_factor_mapping_end = 'SEGMENTS'
        curve_obj.data.bevel_depth = radius
        curve_obj.data.bevel_resolution = 4
        # circle.data.use_stretch=True
        curve_obj.data.use_path_follow=True
        # circle.data.use_path_clamp=True
        # circle.data.use_fill_caps=True
        # curve_obj.data.use_deform_bounds=True
        
        # print(dir(curve_obj))
        # bpy.context.scene.collection.objects.link(curve_obj)
        # bpy.context.view_layer.objects.active=curve_obj
        # bpy.ops.curve.select_all(action='Select')
        # bpy.ops.curve.split()

        # hole_mesh=curve_obj.to_mesh().copy()
       
        # hole_mesh.update()
        # bpy.data.objects.remove(curve_obj)

        return circle,curve_obj

    def generate_spline(self,coords,curve):
        print('######## GENERATE SPLINE ########')
        
        spline = curve.splines.new(type='BEZIER')


        spline.bezier_points.add(len(coords)-1)

        for i, row in enumerate(coords):
            coord=coords[i]

            if i > 0:
                spline.bezier_points[i].handle_left = (coords[i-1][0],coords[i-1][1], coords[i-1][2])
                spline.bezier_points[i-1].handle_right = (coord[0], coord[1], coord[2])


        return spline

    def generate_spline_colors(self,curve,data,render_col,coords,colormaps,name ):

        print('######## GENERATE SPLINE COLOR ATTRS ########')

        cmap=colormaps[render_col]
        ## make a loadin bar to monitor progress
        bar=tqdm(range(len(data)))
        bar.set_description(f'processing {render_col} colors')


        # make a uv map for the colors
        curve.data.uv_layers.new(name=f'{name} UV')


        for i, row in data.iterrows():
            bar.update(1)
            coord=coords[i]
            shape_key=curve.shape_key_add(name=f'{name} Sample {i}')
            shape_key.data[0].co=coords[i]



            val=row[render_col]
            if val==np.nan:
                val=0
            color=cmap.get_rgb(val)
            shape_key.value=1

            prop_name=str(f"{name} sample color {i}")
            prop=self.make_custom_color_prop(obj=curve,color=color,name=prop_name)
            shape_key.value=val
            # get the faces for the colors to be added to
            # print(dir(shape_key))
            # print(dir(shape_key.normals_polygon_get().index))

            # uv_map = shape_key.vertex_group.index
            # print(uv_map)
            # print(dir(uv_map))

        #     rgb = nodes.new(type="ShaderNodeRGB")
        #     # Add Texture Coordinate nodes for each UV map
        #     tex = nodes.new(type="ShaderNodeTexCoord")


        #     # tex.location = uv_map

        #     links.new(prop.driver_add("value").driver.outputs[0], rgb.inputs["Fac"])
        #     links.new(rgb.outputs["Color"],tex.inputs['Color'])
        #     links.new(tex.outputs["UVMap"], group_output.inputs[i])

        # # Assign material to object
        # curve.data.materials.append(mat)
        # curve.materials.active=mat

        
        return curve

    def generate_spline_mats(self,curve ,col):

        # print('######## MAKE COLORING MATERIALS ########')
        
        spline=curve.data.splines.active

        color_layer =spline.points.new(name=col,type='FLOAT_COLOR',default=(1,0,0,1))

        name=color_layer.name

        mat = bpy.data.materials.new(f"{name}_mat")
        mat.use_nodes = True
        node = mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
        mat.node_tree.links.new(node.outputs['Color'], mat.node_tree.nodes['ShaderNodeBsdfDiffuse'].inputs[0])
        node.attribute_name = col

        # Create a new separate RGB node and add it to the material
        curve.data.materials.append(mat)
        curve.active_material=mat
        curve.data.update()

        return color_layer

    def make_one_big_hole(self,name,coords,volume,collar_collection,data,num_columns,color_maps):
        # create the path for the drill hole to follow
        print('######## BUILD HOLE ########')

        curve= bpy.data.curves.new(name=name, type='CURVE',)
        spline=self.generate_spline(coords,curve,)


        # example color

        # print('Curve Dir:',dir(curve))

        # wrap the path for the drill hole with an object so we can convert it to a mesh
        curve_obj = bpy.data.objects.new(f"{name}_path", curve)

        # use a circle as the bevel object and generate a tube along the path
        circle,curve_obj=self.make_tube(curve_obj=curve_obj,name=name,coords=coords,radius=volume,collar_collection=collar_collection)
        ## parent stuff so they are organized
        curve_mesh=self.convert_curve_to_mesh(curve_obj,name)

        
        curve_mesh.parent=curve_obj
        circle.parent=curve_obj
        collar_collection.objects.link(curve_mesh)
        collar_collection.objects.link(curve_obj)


        # curve_mesh=curve_obj.to_mesh()
        # depsgraph = self.context.evaluated_depsgraph_get()

        # obj_eval= curve_mesh.evaluated_get(depsgraph)
        # bm = bmesh.new()
        # tmpMesh = bpy.data.meshes.new(f'{name}_mesh')

        # bm .from_mesh(obj_eval)
        # bm.to_mesh(tmpMesh)       
        # curve_mesh=bpy.data.objects.new(f"{name}_path_mesh", tmpMesh)
        
        # bm.transform(curve_obj.matrix_world)
        # collar_collection.objects.link(curve_mesh)


        # curve_mesh.parent=curve_obj


        return curve_obj,curve_mesh

    def cyls_at_cords(self,coords,rots,sizes,collar_collection,volume=1,name='Hole'):
        cylinders=[]
 
        for i,coord in enumerate(coords):
            if i==0:
                size=sizes[1]
            else:
                size=sizes[i]
            # print(coords[i],rots[i],size)
            bpy.ops.mesh.primitive_cylinder_add(
                                    
                                    location=coords[i],
                                    rotation=rots[i],
                                    radius=volume,
                                    depth=size,
                                    vertices=6,
                                    )

            cly = bpy.context.active_object
            bpy.context.view_layer.objects.active=cly 


            cly.name = f'{name}_{i}'
            collar_collection.objects.link(cly)

    def colors_at_cords(self,coords,data,render_col):
        
        for i, row in data.iterrows():
            
            pass

    def circles_at_cords(self,coords,rots,sizes,collar_collection,volume=1,name='Hole'):

        hole_obj=bpy.data.objects.new(name,None)

        # Create a curve
        # curve_data = bpy.data.curves.new('Curve', 'CURVE')
        # curve_data.dimensions = '3D'
        # curve_object = bpy.data.objects.new('CurveObj', curve_data)
        # bpy.context.scene.collection.objects.link(curve_object)
 
        for i,coord in enumerate(coords):
            if i==0:
                size=sizes[1]
            else:
                size=sizes[i]
            # print(coords[i],rots[i],size)
            bpy.ops.curve.primitive_nurbs_circle_add(radius=volume, location=coords[i],enter_editmode=True,)
            circle= bpy.context.active_object
            circle.name = f'{name}_{i}'
            circle.dimensions = '3D'

            circle.resolution_u = 32
            circle.fill_mode = 'FULL'
            circle.bevel_depth = 0.1

            circle .parent=hole_obj
            bpy.context.view_layer.objects.active=circle


        collar_collection.objects.link(hole_obj)

        print(dir(hole_obj))

    def spline_at_cords(self,coords,rots,sizes,data,render_col,color_maps,collar_collection,volume=1,name='Hole'):

        # Create a curve
        n_circles = len(coords)-1
        circles = []
        samp_objs = []
        scene = self.context.scene

        bar=tqdm(range(n_circles))
        bar.set_description(f'processing {name} points')
        for i, row in data.iterrows():
            bar.update(1)
            bpy.ops.mesh.primitive_cylinder_add(

                        location=coords[i],
                        # rotation=rots[i],
                        radius=volume,
                        depth=sizes[i],
                        vertices=4,
                        )
            #grab the cyl
            circle= bpy.context.active_object
            circle.name = f'{name}_sample_{i}'
            cmap=color_maps[render_col]          
            val=row[render_col]

            if val==np.nan:
                val=0

            colors=cmap.get_rgb(val)

            # set material to the object:
            circle=self.make_tube_material(obj=circle,col=render_col,val=colors,index=i)
            

            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            collar_collection.objects.link(circle)
            # print(dir(circle))

            
            circles.append(circle.data)
            samp_objs .append(samp_objs)
            

        print('-------------------------')
        # print(dir(collar_collection))          
        
        # print(dir(curve_object))
        # print('-------------------------')
        # print(dir(curve_object.children))
        # print('-------------------------')
        # print(dir(curve_object.vertex_groups))

        # self.context.view_layer.update()

        # # print(circles)
        # obj1 = circles[0]
        # sample_object = bpy.data.objects.new(f'{name}_samples', obj1)


        # bm1=bmesh.new()
        # bm1.from_mesh(obj1)
        # old_edges=bm1.edges
        # old_faces=bm1.edges
        # # uv_layer = bm1.loops.layers.uv.active
        # color_layers={}
        # bar=tqdm(range(len(data)))
        # bar.set_description(f'Processing {name} faces')

        # for i,row in data.iterrows():
        #     # print(i)
        #     bar.update(1)
        #     if i>0:
        #         try:
        #             obj2 = circles[i]
        #             bm1.from_mesh(obj2)

        #             bmesh.ops.remove_doubles(bm1)


        #             newfe=bmesh.ops.grid_fill(bm1,**{'edges': old_edges})
        #             newfe=bmesh.ops.edgeloop_fill(bm1,**{'edges': old_edges})
        #             newfe=bmesh.ops.bridge_loops(bm1,**{'edges': old_edges})
        #             bmesh.ops.recalc_face_normals(bm1,**{'faces': bm1.faces})

        #             new_edges= [e for e in bm1.edges if e not in old_edges]
        #             new_faces= [e for e in bm1.faces if e not in old_faces]

        #             bmesh.ops.dissolve_faces(bm1,**{'faces':new_faces ,'use_verts':True})
        #             bmesh.ops.face_attribute_fill(bm1,**{'faces' :new_faces})
        #             old_faces=new_faces
        #             old_edges=new_edges
        #             bm1.to_mesh(obj1)
        #             obj1.update()
        #         except Exception as e:print(e)
        # bm1.to_mesh(obj1)
        # bm1.free()

        # collar_collection.objects.link(sample_object)
        # sample_object
        return 

    def add_cylinder_particles(self,coords,rots,sizes,collar_collection,volume=1,name='Hole'):
        print('########## MAKE CYLINDER PARTICLES ############')
        mesh=bpy.data.meshes.new(f'{name}_data')
        mesh.from_pydata(coords,[],[])
        obj = bpy.data.objects.new(f"{name}",mesh)
        psys=obj.modifiers.new(f"{name}_particles", type='PARTICLE_SYSTEM').particle_system
        collar_collection.objects.link(obj)

        psys.settings.emit_from = 'VERT'
        psys.settings.type = 'HAIR'

        psys.settings.physics_type = 'NO'
        psys.settings.render_type = 'OBJECT'

        # spline=self.generate_spline(coords,curve)


        #wrap the path for the drill hole with an object so we can convert it to a mesh
        # path_obj=bpy.data.objects.new(f"{name}_path", curve)
        # collar_collection.objects.link(path_obj)

        bpy.ops.curve.primitive_bezier_circle_add(radius=volume, location=coords[0],enter_editmode=True, align='WORLD')
        circle=bpy.data.objects[f'{name}_start']
        circle.name=f'{name}_start'
        bpy.context.view_layer.objects.active = circle
        print(dir(psys.settings))
   
        psys.settings.instance_object = circle
        psys.settings.show_unborn = True
        psys.settings.use_dead = True
        obj = bpy.context.active_object
        bpy.ops.object.duplicates_make_real()
        # Update the particle system
        psys.seed = 1
        psys.update()



        print('------------------------------------------------------')
        # print('path_obj Dir:',dir(path_obj))

        

        return obj

    def make_tube_material(self,obj,index,col,val):
        # print('######## MAKE COLORING MATERIALS ########')

        color_layer =obj.data.attributes.new(name=col,type='FLOAT_COLOR',domain='GEOMETERY')
        color_layer.data[0].color=val

        name=color_layer.name

        mat = bpy.data.materials.new(f"{name} {index}_mat")
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeAttribute")
        mat.node_tree.links.new(node.outputs['Color'], mat.node_tree.nodes['Principled BSDF'].inputs[0])
        node.attribute_name = col

        # Create a new separate RGB node and add it to the material
        obj.data.materials.append(mat)
        obj.active_material=mat
        obj.data.update()

        return obj

    def color_particles(self,obj,color_attr):
        # Get the vertex colors of the object
        # Create a material for the object
        material = bpy.data.materials.new(name=f"{color_attr.name} Material")

        # Set the material to use vertex colors
        material.use_nodes = True

        material_output = material.node_tree.nodes["Material Output"]
        color_node = material.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
        color_node.layer_name = color_attr.name

        material.node_tree.links.new(color_node.outputs[0], material.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
        material.node_tree.links.new(material.node_tree.nodes['color_map'].outputs[0], color_node.inputs[0])
        obj.data.materials.append(material)
        return obj
    
    def check_context(self,func):
        old_area=self.context.area.type
                #try each type
        for area in self.context.screen.areas:
                            #set the context
            print('TRY:',area.type)
            # override['area'] = area
            #print out context where operator works (change the ops below to check a different operator)
            try:
                override = bpy.context.copy()
                override['area'] = area

                print(func(area).poll())
                print('Select all will work in: ',area.type)
                return override

            except Exception as e: print(e)

    def make_uvmap(self,obj,name):
        uv_map_name = f"{name} UVMap"
        uv_map = obj.data.uv_layers.new(name=uv_map_name)

        # Assign the new UV map as the active UV map
        obj.data.mesh.uv_layers.active = uv_map
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        return obj

    def convert_curve_to_mesh(self,curve_obj,name):

        curve_mesh=curve_obj.to_mesh()
        depsgraph = self.context.evaluated_depsgraph_get()

        obj_eval= curve_mesh.evaluated_get(depsgraph)
        bm = bmesh.new()
        tmpMesh = bpy.data.meshes.new(f'{name}_mesh')

        bm .from_mesh(obj_eval)
        bm.to_mesh(tmpMesh)       
        curve_mesh=bpy.data.objects.new(f"{name}_path_mesh", tmpMesh)
        
        bm.transform(curve_obj.matrix_world)

        return curve_mesh

    def make_custom_color_prop(self,obj,color,name):
        
        rna_ui = obj.get('_RNA_UI')
        if rna_ui is None:
            obj['_RNA_UI'] = {}

        rna_ui = obj['_RNA_UI']
        custom_prop={ 'property_name':name, 'property_type':'FLOAT_ARRAY',"default":color,'description':f"{name} color", "array_length":4, 'subtype':'COLOR'}
        obj[name]=color
        rna_ui[name]=custom_prop
        return obj[name]


import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

'''color mappper helper class'''


class MplColorHelper:

  def __init__(self, cmap_name, start_val, stop_val):
    self.cmap_name = cmap_name
    self.cmap = plt.get_cmap(cmap_name)
    self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
    self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

  def get_rgb(self, val):
    return self.scalarMap.to_rgba(val)


def color_modifier(particle, color, psys):
    # get the name of the color attribute to use
    color_attr_name = psys.settings.color_attribute
    # get the value of the specified color attribute
    color_attr = getattr(particle, color_attr_name, color)
    if color_attr is not None:
        # interpolate between two colors based on the color attribute value
        particle.color = color