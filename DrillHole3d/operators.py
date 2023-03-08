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

        ## initialze the crap load of variables we need for the two "adventures"
        scene['Sheet_names']=None
        scene['Data_dir']=None
        scene['Header_dir']=None
        scene['Headers']=None
        scene['sheet_selection']=None
        scene['HoleData']=None
        scene['rendercol']='None'
        scene['colormap']='None'

        scene['render_cols']=['Collar','x','y','z','rendercol','colormap']
        scene['colorrenders']=['rendercol','colormap','holeradius']

        scene['InterpHeaders']=['LocationHeaders','SurveyHeaders','DataHeaders']
        scene['InterpData']=['LocationData','SurveyData','DataData']
        scene['interp_sheets']=['location_sheet','survey_sheet','data_sheet']

        ## columns from the three drill hole data files that we would need to merge
        scene['location_cols']=['locationcollars','x','y','z']
        scene['survey_cols']=['surveycollars','surveydepths','dip','azimuth']
        scene['data_cols']=['datacollars','datadepths']

        data_vars=[
            scene['InterpHeaders'],scene['InterpData']
        ]
        str_vars=[
            scene['interp_sheets'],scene['location_cols'],scene['survey_cols'],scene['data_cols'],scene['render_cols']
        ]
        for var in data_vars:
            for x in var :
                scene[x]=None
        
        for var in str_vars:
            for x in var:
                scene[x]='None'



        ## collumns from the we need for a single file to be merged
        scene['render_cols']=['collar','x','y','z','holeradius']
        scene['color_cols']=['rendercol','colormap']

        for x in scene['render_cols']:
            scene[x]='None'

        file_path = scene.file_path
        print('------------------------------------------------------------')
        print('Load File')
        print(file_path)
        print('-------------------------------------')
        # Do something with the file path here
        if scene['Data_dir']==None:
            self.import_data(context)
        print('------------------------------------------------------------')


        scene['choose_adventure_panel']=True
         
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


class ChooseSingleFileOperator(bpy.types.Operator):
    bl_idname = "object.single_file"
    bl_label = "Single File" 

    def execute(self,context):
        print('########## MAKE COLUMN DROP DOWN ##########')
        # Set the custom property to the value entered by the user
        scene=context.scene
        if scene['Headers']!=None:
            scene['show_data_panel']=True
            
        if scene['Sheet_names']!=None:
            scene['show_sheet_panel']=True
        return {'FINISHED'}


class ChooseMulipleFileOperator(bpy.types.Operator):
    bl_idname = "object.multiple_files"
    bl_label = "Multiple Files" 

    def execute(self,context):
        print('########## MULTIPLE FILES ##########')
        # Set the custom property to the value entered by the user

        context.scene['show_multi_sheet_panel']=True
        context.scene['choose_adventure_panel']=False
        return {'FINISHED'}


class ChooseMulipleColumnOperator(bpy.types.Operator):
    bl_idname = "object.multiple_columns"
    bl_label = "Choose Columns" 

    def execute(self,context):
        print('########## MULTIPLE columns##########')
        # Set the custom property to the value entered by the user

        context.scene['show_multi_sheet_panel']=False
        context.scene['show_multi_column_panel']=True
        return {'FINISHED'}


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
        ## reset variable and ui
        scene=context.scene
        scene['HoleData']=None
        scene['Headers']=None
        scene['Sheet_names']=None
        scene['Data_dir']=None
        scene['Header_dir']=None
        scene['render_cols']=['Collar','x','y','z','rendercol']
        scene['show_data_panel']=False
        scene['show_sheet_panel']=False
        scene["show_interp_panel"]=False
        scene["show_render_panel"]=False
        scene['choose_adventure_panel']=False
        scene['show_color_panel']=False
        
        scene['render_cols']=['Collar','x','y','z','rendercol']

        scene['InterpHeaders']=['LocationHeaders','SurveyHeaders','DataHeaders']
        scene['InterpData']=['LocationData','SurveyData','DataData']
        scene['interp_sheets']=['location_sheet','survey_sheet','data_sheet']

        ## columns from the three drill hole data files that we would need to merge
        scene['location_cols']=['locationcollars','x','y','z','holeradius']
        scene['survey_cols']=['surveycollars','surveydepths','dip','azimuth']
        scene['data_cols']=['datacollars','datadepths']

        data_vars=[
            scene['InterpHeaders'],scene['InterpData']
        ]
        str_vars=[
            scene['interp_sheets'],scene['location_cols'],scene['survey_cols'],scene['data_cols'],scene['render_cols']
        ]
        for var in data_vars:
            for x in var :
                scene[x]=None
        
        for var in str_vars:
            for x in var:
                scene[x]='None'
        context.scene['show_multi_sheet_panel']=False
        context.scene['show_multi_column_panel']=False
        context.scene['show_render_panel']=False





        return {'FINISHED'}


class RenderOperator(bpy.types.Operator):

    bl_idname = "object.render_holes"
    bl_label = "Render Drill Holes"
    

    def __init__(self):
        
        self.context=None
        self.color_cols=[]
        self.color_data=pd.DataFrame()
        self.colormaps={}
        self.render_col=''
        self.volume=1
                
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
        print('####### data columns #########')
        print(data.columns)
        # print(data)
        #grab corindates from specified columns
        cord_cols=[scene['x'],scene['y'],scene['z']]
        rot_cols=[scene['dip'],
                scene['azimuth'],
                scene['surveycollars'],
                scene['surveydepths'],
                scene['datacollars'],
                scene['datadepths'],
                scene['collar'],
                
                ]


        ### grab the data columns
        collar_col=scene['collar']
        self.volume=int(scene['holeradius'])
        self.render_col=scene['rendercol']


        
        # rot_cols=[scene['dip'],scene['azimuth']]
        ## drop na depths and locations
        data=self.drop_bad_rows(data=data,cols=cord_cols
                                    # +rot_cols
                                    )

        
        print('COLLAR COLUMNS:',collar_col)

        print('Selected_options',selection_options)
        print('XYZ=',cord_cols)
        print('hole_size :',self.volume)
        # scene['show_data_panel']=False
        # scene['show_sheet_panel']=False

        ### normalize the color mapping
        
        try:volume=float(volume)
        except:volume=1
        

        str_cols=data.select_dtypes(object).columns.to_list()
        num_cols=data.select_dtypes(np.number).columns.to_list()
        color_cols=[c for c in num_cols if c not in cord_cols+rot_cols]
        self.color_cols=color_cols

        view_layer = bpy.context.view_layer

        print('------------------------------------------')
        print ('String dtypes')
        print(str_cols)
        print('------------------------------------------')
        print ('Numeric dtypes') 
        print(num_cols)
        cmap=scene['colormap']
        if cmap=='None':
            cmap='coolwarm'


        self.color_data=data.copy()

        color_cols.append(self.render_col)
        for c in color_cols:
            print(c)
            data[c]=pd.to_numeric(data[c],errors='coerce').fillna(0)

            std=data[c].std(ddof=4)
            mean=data[c].mean()

            self.color_data[c]=data[c]

            max=self.color_data[c].max()
            min=self.color_data[c].min()


            self.colormaps[c]=MplColorHelper(cmap_name=cmap,center_val=mean,range=std)


        ## check the variable we need to render
        if scene['sheet_selection']!=None:
        #make a collection for the data
            collection_name=scene['sheet_selection']
        
        else:
            collection_name=scene['file_path'].split('/')[-1]

        sheet_collection = self.get_collection(name=collection_name)
        try:bpy.context.scene.collection.children.link(sheet_collection)
        except:pass

        groups=self.color_data.groupby(collar_col)
        
        ## lop through all the drill holes
        for drillgroup in groups:
            
            #grab the data and the name
            collar_name=drillgroup[0]
            group=drillgroup[1].reset_index(drop=True)
            print(f'################# Start Drill hole {collar_name}########################')
            print(collar_name)   
            ## clear old versions
            self.clear_old_hole(name=collar_name)

            #### add a new collection to store the spheres
            collar_collection = self.get_collection(name=collar_name)

            try:sheet_collection.children.link(collar_collection)
            except:pass

            
            ## grab the cords from the data
            cord_data=group[cord_cols]

            coords=self.get_cords(cord_data)

            # # ake one big tube. Takes to long to color
            hole_mesh=self.make_one_big_hole(
                                            name=collar_name,
                                            coords=coords,
                                            collar_collection=collar_collection,
                                            )
            gpencil=self.generate_pencil_stroke(
                                                data=group,
                                                coords=coords,
                                                name=collar_name,
                                                collection=collar_collection)
            
            self.color_mesh(gpencil=gpencil,mesh_obj=hole_mesh,color_name=self.render_col)


        print('--------------------------------')
        print('Finished Render')
        scene["show_color_panel"]=False
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

    def create_num_attrs(self,hole_obj,data):
        bar=tqdm(range(len(self.color_cols)))
        bar.set_description(f'Processing {hole_obj.name} Attr table')
        for obj in hole_obj.children:
            if obj.data.name in bpy.data.meshes:
                for c in self.color_cols:
                    bar.update(1)
                    try:
                        ## update the attributes 
                        float_layer = obj.data.attributes.new(name=c,type='FLOAT',domain='FACE')
                        for i, row in data.iterrows():
                            i = int(i)
                            val=row[c]    
                            if val==np.nan:
                                val=0

                            float_layer.data[i].value=val
                    except Exception as e : print(f'Expcetion:{c}',e)
        return obj
    
    def create_shape_keys(self,obj,data,coords):

        for i, row in data.iterrows():
            print(dir(obj.data))
            shape_key=obj.data.shape_keys(f'sample_{i}')

            i = int(i)
            shape_key.co=coords[i]
            shape_key.value=(i/len(coords))
        return obj

    def create_color_attrs(self,hole_obj,data):
        print('######## CREATE COLOR ATTRIBUTES########')

        for obj in hole_obj.children:
            if obj.data.name in bpy.data.meshes:
                bar=tqdm(range(len(self.color_cols)))
                bar.set_description(f'Processing {obj.data.name } Color Attr table')
                for c in self.color_cols:
                    bar.update(1)
                    colormap=self.colormaps[c]
                    color_layer =obj.data.color_attributes.new(name=f'{c}_color',type='FLOAT_COLOR',domain='POINT')
                    try:
                        ## update the attributes 
                        bar=tqdm(data.iterrows())
                        for i,row in bar:
                            val=row[c]  
                            if val==np.nan:
                                val=0
                            colors=colormap.get_rgb(val)
                            color_layer.data[i].color=colors
                
                    except Exception as e : print(f'Exception:{c}',e)
                obj.data.update()
        return obj

    def make_tube(self,curve_obj,name,coords,collar_collection):
        print('######## MAKE TUBE ########')


        # Create a tube that follows the curve
        bpy.ops.curve.primitive_bezier_circle_add(radius=self.volume, location=coords[0],enter_editmode=True, align='WORLD')
        circle=bpy.data.objects["BezierCircle"].copy()
        circle.name=f'{name}_start'
        collar_collection.objects.link(circle)

        bpy.context.view_layer.objects.active = circle

        circle_obj = bpy.data.objects.new(name=name, object_data=circle.data)

        curve_obj.data.bevel_object = circle
        curve_obj.data.dimensions='3D'
        curve_obj.data.bevel_mode='OBJECT'
        curve_obj.data.bevel_factor_mapping_start = 'SEGMENTS'
        curve_obj.data.bevel_factor_mapping_end = 'SEGMENTS'
        curve_obj.data.bevel_depth = self.volume
        curve_obj.data.bevel_resolution = 2
        curve_obj.data.use_path_follow=True
        curve_obj.data.use_path_follow=True



        collar_collection.objects.link(curve_obj)
        bpy.context.view_layer.objects.active=curve_obj
        circle.parent=curve_obj

        return curve_obj


    def generate_spline(self,coords,curve):
        print('######## GENERATE SPLINE ########')
        spline = curve.splines.new(type='BEZIER')
        spline.bezier_points.add(len(coords)-1)

        for i, row in enumerate(coords):
            coord=coords[i]
            spline.bezier_points[i].co=coord
            if i > 0:
                spline.bezier_points[i].handle_left = (coords[i-1][0],coords[i-1][1], coords[i-1][2])
                spline.bezier_points[i-1].handle_right = (coord[0], coord[1], coord[2])


        return spline


    def generate_pencil_stroke(self,data,coords,name,collection):
        print('######## GENERATE GPENCIL ########')
        gpencil_data = bpy.data.grease_pencils.new(name)
        # print(dir(gpencil_data))
        gpencil = bpy.data.objects.new(gpencil_data.name, gpencil_data)
        collection.objects.link(gpencil)
        bar=tqdm(range(len(self.color_cols)))
        
        for c in [self.render_col]:
            color_layer = gpencil_data.layers.new(f'{name} {c}')
            gp_frame = color_layer.frames.new(bpy.context.scene.frame_current)
            gp_stroke = gp_frame.strokes.new()
            gp_stroke.line_width = int(self.volume)*10
            gp_stroke.start_cap_mode = 'FLAT'
            gp_stroke.end_cap_mode = 'FLAT'


            gp_stroke.points.add(len(coords))
            colormap=self.colormaps[c]

                ## update the attributes 

            for i,row in data.iterrows():
                val=row[c]  
                if val==np.nan:
                    val=0
                colors=colormap.get_rgb(val)
                gp_stroke.points[0].vertex_color
                coord=coords[i]
                gp_stroke.points[i].co=coord
                gp_stroke.points[i].pressure=int(self.volume)*10
                gp_stroke.points[i].vertex_color=colors

            mat = bpy.data.materials.new(name=f"{name}_{c}_colors")
            bpy.data.materials.create_gpencil_data(mat)
            gpencil.data.materials.append(mat)

        bpy.context.view_layer.objects.active = gpencil
        # bpy.ops.gpencil.convert(type='CURVE', use_timing_data=False)
        
        # curve = bpy.data.curves[-1]
        # curve.name=f'{name}_hole'

        # curve_obj=bpy.data.objects.new(f'{name}', curve)
        # collection.objects.link(curve_obj)
        # # curve_obj.data.extrude = 1
        # curve_obj.data.use_path_follow=True
        # curve_obj.data.bevel_factor_mapping_start = 'SEGMENTS'
        # curve_obj.data.bevel_factor_mapping_end = 'SEGMENTS'
        # curve_obj.data.dimensions='3D'
        # curve_obj.data.bevel_mode='ROUND'
        # curve_obj.data.bevel_depth = radius
        # curve_obj.data.bevel_resolution = 2


        # curve_mesh=self.convert_curve_to_mesh(curve_obj,name=name)
        # spline=self.generate_spline(coords=coords,curve=curve_obj.data)

        # for gp_layer in  gpencil_data.layers:
        #     print((gp_layer.frames))

        #     # Create a new material for the curve data and set up the shader nodes
        #     self.color_mesh(points=gp_layer.frames[0].strokes[0].points, mesh_obj=curve_mesh,color_name=name)
        # # collection.objects.link(curve_mesh)


        # curve_obj.data.materials.active=f'{name}_{self.render_col}'

        # bpy.ops.gpencil.active_frames_delete_all()
        # bpy.ops.gpencil.convert(type='curve')

        return gpencil


    def make_one_big_hole(self,name,coords,collar_collection):

        # create the path for the drill hole to follow
        print('######## BUILD HOLE ########')
        curve= bpy.data.curves.new(name=name, type='CURVE',)
        spline=self.generate_spline(coords,curve,)

        # wrap the path for the drill hole with an object so we can convert it to a mesh
        curve_obj = bpy.data.objects.new(f"{name}_path", curve.copy())

        # use a circle as the bevel object and generate a tube along the path
        curve_obj=self.make_tube(curve_obj=curve_obj,name=name,coords=coords,collar_collection=collar_collection)
        
        ## parent stuff so they are organized      
        curve_mesh=self.convert_curve_to_mesh(curve_obj=curve_obj,name=name)
        curve_mesh.parent=curve_obj

        collar_collection.objects.link(curve_mesh)
        # bpy.data.objects.remove(curve_obj)

        return curve_mesh


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


    def color_mesh(self,gpencil, mesh_obj,color_name):
        print('######## collor_mesh faces ########')
        gpencil_data=gpencil.data
        gp_layer = gpencil_data.layers[0]
        gp_frame=gp_layer.frames[0]
        gp_strokes=gp_frame.strokes[0]
        points=gp_strokes.points

        bm=bmesh.new()
        bm.from_mesh(mesh_obj.data)

        bar=tqdm(range(len(bm.faces)))
        bar.set_description(f'Processing {color_name} Color Attr Faces')

        for face in bm.faces:
            bar.update(1)
            min_dist=np.inf
            for i,point in enumerate(points):
                gp_pos = mesh_obj.matrix_world @ point.co
                face_center = mesh_obj.matrix_world @ face.calc_center_median()
                dist = abs(gp_pos.z - face_center.z)
                if dist < min_dist:
                    samp_index=i
                    closest_point = point
                    min_dist = dist
            mat_name=f'{mesh_obj.name} Sample {samp_index} {color_name}'

            if mat_name not in bpy.data.materials:
                mat = bpy.data.materials.new(mat_name)
                mat.diffuse_color = closest_point.vertex_color
                mesh_obj.data.materials.append(mat)
                mesh_obj.data.update()

            mat_index=mesh_obj.data.materials.find(mat_name)
            face.material_index = mat_index

        bm.to_mesh(mesh_obj.data)
        mesh_obj.data.update()

    def convert_curve_to_mesh(self,curve_obj,name):

        curve_mesh=curve_obj.to_mesh()
        depsgraph = self.context.evaluated_depsgraph_get()

        obj_eval= curve_mesh.evaluated_get(depsgraph)
        bm = bmesh.new()
        tmpMesh = bpy.data.meshes.new(f'{name}_mesh')

        bm.from_mesh(obj_eval)
        bm.to_mesh(tmpMesh)       
        curve_mesh=bpy.data.objects.new(f"{name}", tmpMesh)
        
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

    def make_curve_material(self,curve_obj,gp_layer):

        # set up vertex colors for Bezier Curve object
        mat = bpy.data.materials.new(name=f"{curve_obj} VertexColors")
        mat.use_nodes = True
        print(dir(mat))
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        bsdf_node = nodes.get("Principled BSDF")
        vertex_color_node = nodes.new("ShaderNodeVertexColor")
        links.new(vertex_color_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        vertex_color_node.layer_name = gp_layer.info
        print(gp_layer.info)

        
        curve_obj.data.materials.append(mat)

    def clear_old_hole(self, name,):

        for mat in bpy.data.grease_pencils:
            if name in mat.name:
                bpy.data.grease_pencils.remove(bpy.data.grease_pencils[mat.name])

        for mat in bpy.data.materials:
            if name in mat.name:
                bpy.data.materials.remove(bpy.data.materials[mat.name])

        for obj in bpy.data.objects:
            if name in obj.name:
                bpy.data.objects.remove(bpy.data.objects[obj.name])

        for curve in bpy.data.curves:
            if name in curve.name:
                bpy.data.curves.remove(bpy.data.curves[curve.name])
        for mesh in bpy.data.meshes:
            if name in mesh.name:
                bpy.data.meshes.remove(bpy.data.meshes[mesh.name])

    def get_collection(self,name):
            # find all the collections and remove them
        collection_names = [col.name for col in bpy.data.collections]
        if name in collection_names:
            collection=bpy.data.collections[name]
        else :
            collection = bpy.data.collections.new(name)

        return collection



import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

'''color mappper helper class'''


class MplColorHelper:

  def __init__(self, cmap_name, start_val=1, stop_val=0,center_val=None,range=None):
    self.cmap_name = cmap_name
    self.cmap = plt.get_cmap(cmap_name)
    if center_val:
        self.norm = mpl.colors.CenteredNorm(vcenter=center_val, halfrange=range)
    else:
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