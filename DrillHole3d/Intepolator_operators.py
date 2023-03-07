import bpy
import numpy as np 
import pandas as pd
from math import radians

class ChooseLocationSHEETOperator(bpy.types.Operator):
    bl_idname = "object.location_sheet"
    bl_label = " CHoose Location Sheet"

    def execute(self, context):
        print('########## GET LOCATION SHEET, MAKE SHEET DROP DOWN ##########')

        scene=context.scene
        sheet_names=scene['Sheet_names']
        return {'FINISHED'}

class ChooseSurveySHEETOperator(bpy.types.Operator):
    bl_idname = "object.survey_sheet"
    bl_label = "Survey Sheet"

    def execute(self, context):
        print('########## GET SURVEY SHEET, MAKE SHEET DROP DOWN ##########')
        scene=context.scene
        sheet_names=scene['Sheet_names']
        return {'FINISHED'}

class ChooseDataSHEETOperator(bpy.types.Operator):
    bl_idname = "object.data_sheet"
    bl_label = "Survey Sheet"

    def execute(self, context):
        print('########## GET DATA SHEET, MAKE SHEET DROP DOWN ##########')
        scene=context.scene
        sheet_names=scene['Sheet_names']
        return {'FINISHED'}

class BuildHolesOperator(bpy.types.Operator):

    bl_idname = "object.build_holes"
    bl_label = "Build Drill Holes"


    def __init__(self):
        
        self.context=None
                
    def execute(self, context):
        # print (dir(bpy.ops.bgis))
        print('############## Begin Build ############')
        print('------------------------------------------')
        
        # bpy.ops.bgis.add_predef_crs(1)
        # bpy.ops.geoscene.init_org()
        scene=context.scene
        self.context=context
        location_options=[]
        for x in scene['location_cols']:
            print(x,scene[x])
            location_options.append(scene[x])
        print('Location Colls',location_options)


        survey_options=[]
        for x in scene['survey_cols']:
            print(x,scene[x])
            survey_options.append(scene[x])
        print('Location Colls',survey_options)


        data_options=[]
        for x in scene['data_cols']:
            print(x,scene[x])
            data_options.append(scene[x])
        print('Location Colls',survey_options)


        collars=scene['LocationData']
        survey=scene['SurveyData']
        target_data=scene['DataData']

        target_data = pd.read_json(target_data)
        collars = pd.read_json(collars)
        survey = pd.read_json(survey)
        print('######### Collar_data ###########')
        print(collars.head(5) )

        print('######### Survery_data ###########')
        print(survey.head(5) )

        print('#########target_data###########')
        print(target_data.head(5))

        #grab user specified columns
        location_collar_col=scene['locationcollars']
        x_col=scene['x']
        y_col=scene['y']
        z_col=scene['z']


        ## grab survey columns
        survey_collar_col=scene['surveycollars']
        dip_col=scene['dip']
        azi_col=scene['azimuth']
        survey_depth_col=scene['surveydepths']

        ### grab the data columns
        data_collar_col=scene['datacollars']
        data_z_col=scene['datadepths']

        drill_data=[]
        for name,group in target_data.groupby(data_collar_col):
            surv=survey[survey[survey_collar_col]==name].reset_index(drop=True)
            start_data=collars[collars[location_collar_col]==name].reset_index(drop=True)
            for i in surv[survey_depth_col].values:
                group.loc[-1,data_z_col]=i
                group=group.reset_index(drop=True)

            group=group.sort_values(data_z_col)
            data=pd.merge(group,surv,left_on=[data_z_col],right_on=[survey_depth_col],how = 'left',
                                                                                        suffixes=('', '_delme')  # Left gets no suffix, right gets something identifiable
                                                                                        )
            # data = data[[c for c in data.columns if not c.endswith('_delme')]]
            data[[azi_col,dip_col]]=data[[azi_col,dip_col]].fillna(method='ffill').fillna(method='bfill')
            drop=data[data[data_collar_col].isna()].index
            data=data.drop(drop).fillna(0).reset_index(drop=True)
            
            ## convert angles to radians
            data [azi_col]=data [azi_col].apply(radians)
            data [dip_col]=data [dip_col].apply(radians)

            ## grab starting coordinates
            start_x=start_data[x_col].values[0]
            start_y=start_data[y_col].values[0]
            start_z=start_data[z_col].values[0]
            print('Starting xyz',start_x,start_y,start_z)

            # grab starting depth
            print('###### Merged_data #####')
            last_depth=data.loc[0,data_z_col]

            data.loc[0,x_col]=start_x
            data.loc[0,y_col]=start_y
            data.loc[0,z_col]=start_z

            
            for i, row in data.iterrows():
                if i>0:
                    new_depth=row[data_z_col]

                    azi=row[azi_col]
                    dip=row[dip_col]

                    distance=np.abs(new_depth-last_depth)

                
                    x_hat,y_hat,z_hat=self.calc_xyz(azi=azi,dip=dip,depth=distance)


                    x=start_x+x_hat
                    y=start_y+y_hat
                    z=start_z+z_hat

                    data.loc[i,x_col]=x
                    data.loc[i,y_col]=y
                    data.loc[i,z_col]=z
                    
                    start_x=x
                    start_y=y
                    start_z=z

                    last_depth=new_depth

            drill_data.append(data)
        

        drill_holes=pd.concat(drill_data,axis=0).reset_index(drop=True)
        print('DRILL HOLES')
        print(drill_holes.columns)

        print(drill_holes)
        scene['HoleData']=drill_holes.to_json()
        scene['Headers']=drill_holes.columns
        scene['collar']=data_collar_col
        context.scene['show_multi_column_panel']=False
        scene['show_render_panel']=True
        return{'FINISHED'}

    def calc_xyz(self,azi,dip,depth):
        # scalar length be is the distance from the previous point or depth in geo terms

        x_hat = depth*np.cos(dip)*np.sin(azi)
        y_hat = depth*np.cos(dip)*np.cos(azi) 
        z_hat = depth*np.sin(dip) 
        return x_hat,y_hat,z_hat