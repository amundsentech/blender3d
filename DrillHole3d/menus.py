import bpy
import matplotlib as mpl


class SheetDropDownMenu(bpy.types.Menu):
    bl_label = "Sheets"
    bl_idname = "OBJECT_MT_sheet_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Sheet_names']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.sheet_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['sheet_selection']

class CollarDropDownMenu(bpy.types.Menu):
    bl_label = "Collar"
    bl_idname = "OBJECT_MT_collar_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Headers']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.collar_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['collar']

class XDropDownMenu(bpy.types.Menu):
    bl_label = "X"
    bl_idname = "OBJECT_MT_x_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Headers']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.x_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['x']

class YDropDownMenu(bpy.types.Menu):
    bl_label = "Y "
    bl_idname = "OBJECT_MT_y_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Headers']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.y_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['y']

class ZDropDownMenu(bpy.types.Menu):
    bl_label = "Z"
    bl_idname = "OBJECT_MT_z_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Headers']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.z_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['z']

class DipDropDownMenu(bpy.types.Menu):
    bl_label = "Dip"
    bl_idname = "OBJECT_MT_dip_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Headers']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.dip_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['z']

class AzimuthDropDownMenu(bpy.types.Menu):
    bl_label = "Azimuth"
    bl_idname = "OBJECT_MT_azimuth_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Headers']
        
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.azimuth_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['z']

class VolumeDropDownMenu(bpy.types.Menu):
    bl_label = "Hole Radius (meters)"
    bl_idname = "OBJECT_MT_holeradius_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        dropdown_items = ['.1','.2','.5','.7','.9','1','5','10','20']
        options= create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.holeradius_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['z']

class RenderDropDownMenu(bpy.types.Menu):
    bl_label = "RenderCol"
    bl_idname = "OBJECT_MT_rendercol_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = context.scene['Headers']
        options= create_dropdown_options(dropdown_items)
        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.rendercol_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['rendercol']

class ColormapDropDownMenu(bpy.types.Menu):
    bl_label = "colormap"
    bl_idname = "OBJECT_MT_colormap_dropdown_menu"

    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        color_options=mpl.colormaps()
        options= create_dropdown_options(sorted(color_options))

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator("object.colormap_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['z']

'''Drop down Helper tool'''
def create_dropdown_options(items):
    options = []
    for i,op in enumerate(items):
        row=tuple([op,op,str(i)])
        options.append(row)

    return options