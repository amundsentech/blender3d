import bpy
import pandas as pd
import numpy as np

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
        scene['render_cols']=['collar','x','y','z','rendercol']#,'dip','azimuth']
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
        scene=context.scene
        selection_options=[]
        for x in scene['render_cols']:
            print(x,scene[x])
            selection_options.append(scene[x])
        data=scene['HoleData']
        data = pd.read_json(data)
        data=(data - data.min(0)) / (data.max(0) - data.min(0))
        # print(data)
        #grab corindates from specified columns
        cord_cols=[scene['x'],scene['y'],scene['z']]
        collar_col=scene['collar']
        
        # rot_cols=[scene['dip'],scene['azimuth']]

        data=self.drop_bad_rows(data=data,cols=cord_cols
                                    # +rot_cols
                                    )
        cords=self.normalize_col(data=data,cols=cord_cols)
        
        
        
        
        print('COLLAR COLUMNS:',collar_col)
        groups=data.groupby(collar_col)
        print('Selected_options',selection_options)
        scene['show_data_panel']=False
        scene['show_sheet_panel']=False

        for drillgroup in groups:
            #grab the data and the name
            drill_collar=drillgroup[0]
            print(drill_collar)
            group=drillgroup[1]
            print(group.shape)

            mesh_data = bpy.data.meshes.new(name=drill_collar)


            # material = bpy.data.materials[drill_collar]
            cord_data=group[cord_cols]
            cords=self.get_cords(cord_data)
            
            mesh_data.from_pydata(cords, [], [])
            mesh_data.update()
            mesh_obj = bpy.data.objects.new(name=drill_collar, object_data=mesh_data)
            mesh_obj=self.add_points(mesh_obj=mesh_obj)

            # rot_data=group[rot_cols]
            # if 'None' not in rot_cols:
            #     rots=self.get_rots(cord_data)

            scene.collection.objects.link(mesh_obj)


        return{'FINISHED'}


    def drop_bad_rows(self,data,cols):
        print('##### Drop bad rows #####')
        for col in cols:
            drop_index=data[data[col].isna()].index
            data=data.drop(drop_index)
        return data

    def normalize_col(self,data,cols):
        print('##### Drop bad rows #####')
        for col in cols:
            data[col]=(data[col] - data[col].min()) / (data[col].max() - data[col].min())

        return data
    def get_cords(self,data):
        all_cords=[]
        data=data.values
        
        for i in range(data.shape[0]):
            row=data[i,:]
            cords=tuple([c for c in row])
            print(cords)
            all_cords.append(cords)
        return all_cords

    def add_points(self,mesh_obj):
        mesh_data=mesh_obj.data
        bpy.ops.mesh.primitive_uv_sphere_add()
        sphere = bpy.context.active_object
        sphere.name = "Sphere"
        sphere.show_instancer_for_render = True
        sphere.show_instancer_for_viewport = True

        # Set the viewport display settings for the sphere object
        sphere.display_type = 'SOLID'


        psys = mesh_obj.modifiers.new(name="Spheres", type='PARTICLE_SYSTEM').particle_system
        psys.settings.type = 'HAIR'
        psys.settings.count = len(mesh_data.vertices)
        psys.settings.particle_size = .5/ len(mesh_data.vertices)
        psys.settings.render_type = 'OBJECT'

        # Set the object used to render the particles to a sphere object
        psys.settings.instance_object = sphere
        # Set the particle source to "Verts"
        psys.settings.emit_from = 'VERT'

        # Disable rotation and velocity for the particles
        psys.settings.use_rotations = False
        psys.settings.use_velocity_length = False
        return mesh_obj



    def get_rots(self,data):
        all_rots=[]
        data=data.values
        for i in data.shape[0]:
            row=data[i,:]
            cords=tuple([c for c in row])
            all_rots.append(cords)
        return all_rots