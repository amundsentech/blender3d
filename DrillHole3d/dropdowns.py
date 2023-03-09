import bpy

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
        scene['LocationHeaders']=headers
        scene['SurveyHeaders']=headers
        scene['DataHeaders']=headers



        return {'FINISHED'}

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

class RenderDropDownOperator(bpy.types.Operator):
    bl_label = "RenderCol Drop-Down Operator"
    bl_idname = "object.rendercol_dropdown_operator"

    option : bpy.props.StringProperty()

    def execute(self, context):
        scene=context.scene
        print("Selected Rendercolumn : ", self.option)
        selection=self.option
        scene['rendercol']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}

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

'''Drop down Helper tool'''
def create_dropdown_options(items):
    options = []
    for i,op in enumerate(items):
        row=tuple([op,op,str(i)])
        options.append(row)

    return options