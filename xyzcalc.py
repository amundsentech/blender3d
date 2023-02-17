import bpy

class CustomProperties(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')

class CustomOperator(bpy.types.Operator):
    bl_idname = "object.custom_operator"
    bl_label = "Custom Operator"

    def execute(self, context):
        props = context.scene.custom_props
        file_path = props.file_path
        print(f"File path: {file_path}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class CustomPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_custom_panel"
    bl_label = "Custom Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Custom Add-on"

    def draw(self, context):
        layout = self.layout
        props = context.scene.custom_props
        layout.prop(props, "file_path")
        layout.operator("object.custom_operator", text="Import Data")

classes = [CustomProperties, CustomOperator, CustomPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.custom_props

if __name__ == "__main__":
    register()