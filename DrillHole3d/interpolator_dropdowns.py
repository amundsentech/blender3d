import bpy

class LocationSheetDropDownOperator(bpy.types.Operator):
    bl_label = "Simple Drop-Down Operator"
    bl_idname = "object.location_sheet_dropdown_operator"

    option : bpy.props.StringProperty()

    def execute(self, context):
        scene=context.scene
        print("Selected Location Sheet: ", self.option)
        selection=self.option
        scene['location_sheet']=self.option
        ##update the headers after a selecetion
        data_dir=scene['Data_dir']
        header_dir=scene['Header_dir']

        data=data_dir[selection]
        headers=header_dir[selection]


        scene['LocationData']=data
        scene['LocationHeaders']=headers
        scene['Headers']=headers

        return {'FINISHED'}

class SurveySheetDropDownOperator(bpy.types.Operator):
    bl_label = "Simple Drop-Down Operator"
    bl_idname = "object.survey_sheet_dropdown_operator"

    option : bpy.props.StringProperty()

    def execute(self, context):
        scene=context.scene
        print("Selected Survey sheet: ", self.option)
        selection=self.option
        scene['survey_sheet']=self.option
        ##update the headers after a selecetion
        data_dir=scene['Data_dir']
        header_dir=scene['Header_dir']

        data=data_dir[selection]
        headers=header_dir[selection]


        scene['SurveyData']=data
        scene['SurveyHeaders']=headers

        return {'FINISHED'}

class DataSheetDropDownOperator(bpy.types.Operator):
    bl_label = "Simple Drop-Down Operator"
    bl_idname = "object.data_sheet_dropdown_operator"

    option : bpy.props.StringProperty()

    def execute(self, context):
        scene=context.scene
        print("Selected Data sheet: ", self.option)
        selection=self.option
        scene['data_sheet']=self.option
        ##update the headers after a selecetion
        data_dir=scene['Data_dir']
        header_dir=scene['Header_dir']

        data=data_dir[selection]
        headers=header_dir[selection]
        
        scene['sheet_selection']=selection
        scene['DataData']=data
        scene['DataHeaders']=headers

        return {'FINISHED'}

class LocationCollarDropDownOperator(bpy.types.Operator):
    bl_label = "Location Collar Drop-Down Operator"
    bl_idname = "object.locationcollars_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected location Collars Column: ", self.option)
        selection=self.option
        scene['locationcollars']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

class SurveyCollarsDropDownOperator(bpy.types.Operator):
    bl_label = "Survey Collar Drop-Down Operator"
    bl_idname = "object.surveycollars_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected Survey Collars Column: ", self.option)
        selection=self.option
        scene['surveycollars']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

class SurveyDepthsDropDownOperator(bpy.types.Operator):
    bl_label = "Survey Depth Drop-Down Operator"
    bl_idname = "object.surveydepths_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected Survey Depths Column: ", self.option)
        selection=self.option
        scene['surveydepths']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

class DataCollarsDropDownOperator(bpy.types.Operator):
    bl_label = "Data Collar Drop-Down Operator"
    bl_idname = "object.datacollars_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected Data Collars Column: ", self.option)
        selection=self.option
        scene['datacollars']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

class DataDepthsDropDownOperator(bpy.types.Operator):
    bl_label = "Data Depth Drop-Down Operator"
    bl_idname = "object.datadepths_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected Data Depth Column: ", self.option)
        selection=self.option
        scene['datadepths']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}



