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

class SheetDropDownOperator(bpy.types.Operator):
    bl_label = "Simple Drop-Down Operator"
    bl_idname = "object.sheet_dropdown_operator"

    option : bpy.props.StringProperty()

    def execute(self, context):
        scene=context.scene
        print("Selected sheet: ", self.option)
        selection=self.option
        scene['sheet_selection']=self.option
        ##update the headers after a selecetion
        data_dir=scene['Data_dir']
        header_dir=scene['Header_dir']

        data=data_dir[selection]
        headers=header_dir[selection]


        scene['HoleData']=data
        scene['Headers']=headers

        return {'FINISHED'}

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

class CollarDropDownOperator(bpy.types.Operator):
    bl_label = "Collar Drop-Down Operator"
    bl_idname = "object.collar_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected collar: ", self.option)
        selection=self.option
        scene['collar']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

class XDropDownOperator(bpy.types.Operator):
    bl_label = "x Drop-Down Operator"
    bl_idname = "object.x_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected x: ", self.option)
        selection=self.option
        scene['x']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

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

class YDropDownOperator(bpy.types.Operator):
    bl_label = "Y Drop-Down Operator"
    bl_idname = "object.y_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected y: ", self.option)
        selection=self.option
        scene['y']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

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

class ZDropDownOperator(bpy.types.Operator):
    bl_label = "Z Drop-Down Operator"
    bl_idname = "object.z_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected z: ", self.option)
        selection=self.option
        scene['z']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}


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

class DipDropDownOperator(bpy.types.Operator):
    bl_label = "Dip Drop-Down Operator"
    bl_idname = "object.dip_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected dip: ", self.option)
        selection=self.option
        scene['dip']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}


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


class AzimuthDropDownOperator(bpy.types.Operator):
    bl_label = "Azimuth Drop-Down Operator"
    bl_idname = "object.azimuth_dropdown_operator"
    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected azimuth: ", self.option)
        selection=self.option
        scene['azimuth']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

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

class VolumeDropDownOperator(bpy.types.Operator):
    bl_label = "Hole Radius Drop-Down Operator"
    bl_idname = "object.holeradius_dropdown_operator"
    option : bpy.props.StringProperty()

    def execute(self, context):
        scene=context.scene
        print("Selected holeradius: ", self.option)
        selection=self.option
        scene['holeradius']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

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

class RenderDropDownOperator(bpy.types.Operator):
    bl_label = "RenderCol Drop-Down Operator"
    bl_idname = "object.rendercol_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected Render: ", self.option)
        selection=self.option
        scene['rendercol']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

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

class ColormapDropDownOperator(bpy.types.Operator):
    bl_label = "colormap Drop-Down Operator"
    bl_idname = "object.colormap_dropdown_operator"

    option : bpy.props.StringProperty()


    def execute(self, context):
        
        scene=context.scene
        print("Selected ColorMap: ", self.option)
        selection=self.option
        scene['colormap']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

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