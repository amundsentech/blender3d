import bpy


class VIEW3D_PT_file_panel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_file_panel"
    bl_label = "File Import"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Resource Modeling"

    def draw(self, context):
        layout = self.layout
        
        # Create the first row to describe what it does
        box1 = layout.box()
        box2 = layout.box()
        box3 = layout.box()
        box4 = layout.box()

        row1 = box1.row()
        row2 = box2.row()
        row3 = box3.row()
        row4 = box4.row()

        row1.label(text="File Path: .csv or .xlsx")

        # second row to allow for  choosing the file path
        row2.prop(context.scene, "file_path")
        ## creat third spot to run the loading of the csv
        row3.operator('object.load_file')
        row4.operator('object.reset_tool')