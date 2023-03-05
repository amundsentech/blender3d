import bpy

'''
we need the sheet to be selected from the xcel sheet to do the interpolation 

['location_sheet','survey_sheet','data_sheet','sheet_selection']


'''


class LocationSheetDropDownMenu(bpy.types.Menu):
    bl_label = "Location Sheet"
    bl_idname = "OBJECT_MT_location_sheet_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Sheet_names']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.location_sheet_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['sheet_selection']

class SurveySheetDropDownMenu(bpy.types.Menu):
    bl_label = "Survey_Sheet"
    bl_idname = "OBJECT_MT_survey_sheet_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Sheet_names']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.survey_sheet_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['sheet_selection']

class DataSheetDropDownMenu(bpy.types.Menu):
    bl_label = "Data_Sheet"
    bl_idname = "OBJECT_MT_data_sheet_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Sheet_names']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.data_sheet_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['sheet_selection']

class LocationCollarsDropDownMenu(bpy.types.Menu):
    bl_label = "Collar"
    bl_idname = "OBJECT_MT_locationcollars_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['LocationHeaders']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.locationcollars_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['collar']

class SurveyCollarsDropDownMenu(bpy.types.Menu):
    bl_label = "Collar"
    bl_idname = "OBJECT_MT_surveycollars_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['SurveyHeaders']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.surveycollars_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['collar']

class SurveyDepthsDropDownMenu(bpy.types.Menu):
    bl_label = "Depths"
    bl_idname = "OBJECT_MT_surveydepths_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['SurveyHeaders']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.surveydepths_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['collar']

class DataCollarsDropDownMenu(bpy.types.Menu):
    bl_label = "Collar"
    bl_idname = "OBJECT_MT_datacollars_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['DataHeaders']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.datacollars_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['collar']

class DataDepthsDropDownMenu(bpy.types.Menu):
    bl_label = "Depth"
    bl_idname = "OBJECT_MT_datadepths_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['DataHeaders']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.datadepths_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['collar']
'''Drop down Helper tool'''
def create_dropdown_options(items):
    options = []
    for i,op in enumerate(items):
        row=tuple([op,op,str(i)])
        options.append(row)

    return options