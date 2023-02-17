import bpy




## panels that will render

class VIEW3D_PT_file_panel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_file_panel"
    bl_label = "File Import"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Drill Hole Importer"

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


class VIEW3D_PT_choose_sheet(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_choose_xlsx_sheet"
    bl_label = "Choose Sheet to Render"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Drill Hole Importer"
    header_chosen=False

    @classmethod
    def poll(self, context):
        # Only display the panel if the property is set to True
        return context.scene.get("show_sheet_panel", False)
    
    def draw(self, context):
        scene=context.scene

        # Create the first dropdown box
        layout=self.layout
        layout.menu('OBJECT_MT_sheet_dropdown_menu')

        layout.label(text="Selected option: " + scene['sheet_selection'])
        box=layout.box()
        row=box.row()
        row.operator('object.get_columns')



class VIEW3D_PT_choose_headers(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_choose_columns"
    bl_label = "Choose Columns"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Drill Hole Importer"
    header_chosen=False

    @classmethod
    def poll(self, context):
        # Only display the panel if the property is set to True
        return context.scene.get("show_data_panel", False)


    def draw(self, context):
        # Create the first dropdown box
        layout=self.layout
        scene=context.scene

        box1 = layout.box()

        

        row1 = box1.row()

        row1.label(text="Select XYZ,(Z_from-Z_to) and Collar Collumns:")

        for c in scene['render_cols']:
            layout.menu(f'OBJECT_MT_{c}_dropdown_menu')
            layout.label(text=f"{c} Selection= " + scene[c])

        box2 = layout.box()
        row2 = box2.row()
        row2.operator('object.render_holes')


        

    # def update_callback(self, context):
    #     # Update the menu when the keyword variable is updated
    #     self.layout.menu('OBJECT_MT_column_dropdown_menu', text=context.scene[c])'''helper tool'''


def create_dropdown_options(items):
    options = []
    for i,op in enumerate(items):
        row=tuple([op,op,str(i)])
        options.append(row)

    return options