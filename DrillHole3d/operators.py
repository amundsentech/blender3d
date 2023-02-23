import bpy
import bmesh
import pandas as pd
import numpy as np
import sys
import os
import matplotlib as plt
from pyproj import Transformer,Proj
# import BlenderGIS as bgis
# from BlenderGIS.geoscene import GeoScene, GEOSCENE_OT_coords_viewer


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
        scene['render_cols']=['collar','x','y','z','rendercol','colormap']#,'dip','azimuth']
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
            print('File must be a .csv or .xslx')
          
class ChooseColumnsOperator(bpy.types.Operator):
    bl_idname = "object.get_columns"
    bl_label = "Choose Header Columns" 

    def execute(self,context):
        print('########## MAKE COLUMN DROP DOWN##########')
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


    def execute(self, context):
        print (dir(bpy.ops.bgis))
        print('############## Begin Render ############')
        print('------------------------------------------')
        
        # bpy.ops.bgis.add_predef_crs(1)
        # bpy.ops.geoscene.init_org()
        scene=context.scene
        selection_options=[]
        for x in scene['render_cols']:
            print(x,scene[x])
            selection_options.append(scene[x])
        data=scene['HoleData']
        data = pd.read_json(data)
        # print(data)
        #grab corindates from specified columns
        cord_cols=[scene['x'],scene['y'],scene['z']]
        render_col=scene['rendercol']
        cmap=scene['colormap']
        collar_col=scene['collar']
        
        # rot_cols=[scene['dip'],scene['azimuth']]
        ## drop na depths and locations
        data=self.drop_bad_rows(data=data,cols=cord_cols
                                    # +rot_cols
                                    )

        
        print('COLLAR COLUMNS:',collar_col)
        groups=data.groupby(collar_col)
        print('Selected_options',selection_options)
        print('XYX=',cord_cols)
        # scene['show_data_panel']=False
        # scene['show_sheet_panel']=False

        ### normalize the color mapping
        
        if cmap==None:
            cmap='coolwarm'

        if render_col==None:
            render_col=scene['z']
        else:
            render_col=render_col


        print('render_using:',render_col)
        print('Colormap:',cmap)
        mean=data[render_col].mean()
        std=data[render_col].std()
        min=data[render_col].min()
        max=data[render_col].max()
        print(f'{render_col} Column Stats:')
        print('Mean:',mean,'Std:',std,'Min:',min,'Max:',max)
        upper=mean+std
        lower=mean-std
        colormap= MplColorHelper(cmap_name=cmap,start_val=min,stop_val=max)


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
        for n in num_cols:
            mean=data[n].mean()
            std=data[n].std()
            min=data[n].min()
            max=data[n].max()
            print(f'{n} Columns Stats')
            print('Mean:',mean,'Std:',std,'Min:',min,'Max:',max)
            print('------------------------------------------')

            upper=mean+std
            lower=mean-std
            colormap= MplColorHelper(cmap_name=cmap,start_val=min,stop_val=max)
            colormaps[n]=colormap

        if scene['sheet_selection']!=None:
        #make a collection for the data
            collection_name=scene['sheet_selection']
        else:
            collection_name=scene["File Path"].split('/')[-1]
        # top of the node tree

        sheet_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(sheet_collection)
        for drillgroup in groups:
            #grab the data and the name
            collar_name=drillgroup[0]
            group=drillgroup[1].reset_index(drop=True)
            print('#########################################')
            print(collar_name)   

            #### add a new collection to store the spheres
            collar_collection = bpy.data.collections.new(f'{collar_name}')
            
            ## grab the cords from the data
            cord_data=group[cord_cols]
            cords=self.get_cords(cord_data)

            # ## create a mesh for the entire hole
            hole_mesh=bpy.data.meshes.new(f'{collar_name}_data')
            hole_mesh.from_pydata(cords,[],[])
            hole_mesh.update()
            hole_obj= bpy.data.objects.new(f"{collar_name}_{render_col}", hole_mesh)


            hole_obj=self.create_str_attrs(columns=str_cols,obj=hole_obj,data=group)
            hole_obj=self.create_num_attrs(columns=num_cols,obj=hole_obj,data=group)
            hole_obj=self.create_color_attrs(columns=num_cols,obj=hole_obj,data=group,colormaps=colormaps)
            
            spheres=self.spheres_at_cords(cords=cords,group_name=collar_name,color_map_object=hole_obj,render_col=render_col)

            collar_collection.objects.link(hole_obj)
            [collar_collection.objects.link(s) for s in spheres]

            sheet_collection.children.link(collar_collection)     

        print('--------------------------------')
        print('Finished Render')
        return{'FINISHED'}

    def drop_bad_rows(self,data,cols):
        print('##### Drop bad rows #####')
        for col in cols:
            try:
                drop_index=data[data[col].isna()].index
                data=data.drop(drop_index)
            except:pass
        return data

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
                float_layer = obj.data.vertex_layers_float.new(name=f'{c}_values')
                
                for i, row in data.iterrows():
                    i = int(i)
                    val=row[c]    
                    if val==np.nan:
                        val=-99
                    float_layer.data[i].value=val
            except Exception as e : print(f'Expcetion:{c}',e)
        return obj

    def create_color_attrs(self,columns,obj,data,colormaps):
        for c in columns:
            try:
                colormap=colormaps[c]
                ## update the attributes 
                color_layer=obj.data.color_attributes.new(name=f'{c}_colors',
                        type='FLOAT_COLOR',domain='POINT'
                        )
                for i, row in data.iterrows():
                    i = int(i)
                    val=row[c]    
                    if val==np.nan:
                        val=-99

                    colors=colormap.get_rgb(val)
                    color_layer.data[i].color=colors
            except Exception as e : print(f'Expcetion:{c}',e)
        return obj

    def spheres_at_cords(self,cords,group_name,color_map_object,render_col):
        spheres=[]
                    ## grab the top and bottom
        top=cords[0][-1] ## top z coulmn val
        bottom=cords[-1][-1] ## bottom z column values
        hole_size=np.abs(top-bottom)
        bpy.ops.mesh.primitive_uv_sphere_add()
        parent_sphere = bpy.context.active_object
        parent_sphere.name = f'{group_name}_start'
        parent_sphere.location=cords[0]
        spheres.append(parent_sphere)
        for i,cord in enumerate(cords[1:]):
            bpy.ops.mesh.primitive_uv_sphere_add()
            sphere = bpy.context.active_object
            sphere.name = f'{group_name}_{i}'
            sphere.location=cord
            # [print(c) for c in dir(sphere)]
            # sphere.display_size=hole_size/len(cords)/4
            sphere.parent = parent_sphere
            sphere.matrix_parent_inverse = parent_sphere.matrix_world.inverted()
            spheres.append(sphere)

        # material = bpy.data.materials.new(name="SphereMaterial")
        # material.use_nodes = True
        color_map_mesh = color_map_object.data
        for color_map_layer in color_map_mesh.color_attributes:

            print(color_map_layer)
            for i, vertex in enumerate(color_map_mesh.vertices):
                color = tuple([c for c in color_map_layer.data[i].color])
                sphere=spheres[i]
                material=bpy.data.materials.new(name=f'{color_map_layer.name}_Material')
                material.diffuse_color=color
                sphere.active_material=material

        return spheres
        
    def get_cords(self,data):
        all_cords=[]
        data=data.values
        trans = Transformer.from_crs(3857, 4326, always_xy=True)
        
        for i in range(data.shape[0]):
            row=data[i,:]
            row=[r for r in row]
            x,y=row[0],row[1]
            # print(x,y)
            # if (x>180) or (y>180):


            #     if i<1:
            #         print('update projection')
            #     xx, yy = trans.transform(x, y)
            #     row[0]=xx
            #     row[1]=yy
            cords=tuple([c for c in row])
            all_cords.append(cords)
        return all_cords


    def add_spheres(self,mesh_obj,hole_size,coords,name):
        mesh_data=mesh_obj.data
        bpy.ops.mesh.primitive_uv_sphere_add(location=coords[0])
        sphere = bpy.context.active_object
        sphere.name = name
        # Set the viewport display settings for the sphere object
        sphere.display_type = 'SOLID'

        psys = mesh_obj.modifiers.new(name="Hole_Samples", type='PARTICLE_SYSTEM').particle_system
        # psys.settings.type = 'HAIR'
        psys.settings.count = len([v for v in mesh_data.vertices])
        psys.settings.particle_size =hole_size/len(mesh_data.vertices)/2
        psys.settings.render_type = 'OBJECT'
        # Set the particle system to use vertex colors
        psys.settings.color_maximum = 1.0
        psys.settings.display_color = 'MATERIAL'
        # [print(c) for c in dir(psys.settings)]

        
        # Set the object used to render the particles to a sphere object
        psys.settings.instance_object = sphere
        # Create a material for the particles
        particle_material = bpy.data.materials.new(name=f"{name} Particle Material")

        # Set the particle material to use vertex colors
        particle_material.use_nodes = True
        particle_material_output = particle_material.node_tree.nodes["Material Output"]
        vertex_color_node = particle_material.node_tree.nodes.new('ShaderNodeVertexColor')
        vertex_color_node.layer_name = name
        particle_material.node_tree.links.new(
            vertex_color_node.outputs["Color"],
            particle_material_output.inputs["Surface"],
        )

        # Assign the particle material to the particle system
        # psys.settings.materials_slot = 'Default Material'
        # [print(c) for c in dir(psys)]
        [print(c) for c in dir(psys.settings.material)]
        # psys.settings.material.real=True
        # psys.settings.material_slot = 'Default Material'
        psys.settings.material = particle_material

        return mesh_obj,sphere



    def get_rots(self,data):

        all_rots=[]
        data=data.values
        for i in data.shape[0]:
            row=data[i,:]
            cords=tuple([c for c in row])
            all_rots.append(cords)
        return all_rots


    def get_cylnder_faces(self,cords):
        pass
    # Define a function to create a new diffuse shader node tree
    def make_Material(self,color_layer,name):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True


        # set up the material node tree
        tree = mat.node_tree
        nodes = tree.nodes


        diffuse_node = nodes.new(type="ShaderNodeBsdfDiffuse")
        vertex_color_node = nodes.new(type="ShaderNodeVertexColor")
        tree.links.new(vertex_color_node.outputs[0], diffuse_node.inputs[0])
        
        
        return mat

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