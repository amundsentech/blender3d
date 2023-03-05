import bpy

class VIEW3D_PT_choose_multi_sheets(bpy.types.Panel):

    bl_idname = "VIEW3D_PT_choose_interp_sheets"
    bl_label = "Choose Location,Survey,and Data Sheets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Drill Hole Importer"
    header_chosen=False

    @classmethod
    def poll(self, context):
        # Only display the panel if the property is set to True
        return context.scene.get('show_multi_sheet_panel', False)


    def draw(self, context):
        # Create the first dropdown box
        layout=self.layout
        scene=context.scene

        box1 = layout.box()
        row1 = box1.row()

        row1.label(text="Select location,survey, and Data Sheets:")

        for c in scene['interp_sheets']:
            layout.label(text=f"{c.title()} Selection= " + scene[c])
            layout.menu(f'OBJECT_MT_{c}_dropdown_menu')


        box2 = layout.box()
        box3=layout.box()
        row3 = box3.row()
        row3.operator('object.multiple_columns')

class VIEW3D_PT_choose_multi_headers(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_choose_multi_columns"
    bl_label = "Choose Columns"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Drill Hole Importer"
    header_chosen=False

    @classmethod
    def poll(self, context):
        # Only display the panel if the property is set to True
        return context.scene.get('show_multi_column_panel', False)



    def draw(self, context):
        # Create the first dropdown box
        layout=self.layout
        scene=context.scene

        ## location_columns
        box1 = layout.box()
        row1 = box1.row()
        loc_cols=scene['location_cols']
        # print(loc_cols)
        row1.label(text=f" Select {loc_cols } ")

        for c in scene['location_cols']:
            layout.label(text=f"{c.title()} Selection= " + scene[c])
            layout.menu(f'OBJECT_MT_{c}_dropdown_menu')

        ## survey_columns
        box2 = layout.box()
        row2 = box2.row()
        loc_cols=scene['survey_cols']
        # print(loc_cols)

        row2.label(text=f" Select {loc_cols } ")

        for c in scene['survey_cols']:
            layout.label(text=f"{c.title()} Selection= " + scene[c])
            layout.menu(f'OBJECT_MT_{c}_dropdown_menu')  

        # print(loc_cols)
         

        ## survey_columns

        box3 = layout.box()
        row3 = box3.row()
        loc_cols=scene['data_cols']
        row3.label(text=f" Select {loc_cols } ")

        for c in scene['data_cols']:
            layout.label(text=f"{c.title()} Selection= " + scene[c])
            layout.menu(f'OBJECT_MT_{c}_dropdown_menu')  

        box4 = layout.box()
        row4 = box4.row()
        row4.operator('object.build_holes')

class VIEW3D_PT_render_holes(bpy.types.Panel):

    bl_idname = "VIEW3D_PT_render_panel"
    bl_label = "Render Drill Holes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Drill Hole Importer"
    header_chosen=False

    @classmethod
    def poll(self, context):
        # Only display the panel if the property is set to True
        return context.scene.get('show_render_panel', False)


    def draw(self, context):
        # Create the first dropdown box
        layout=self.layout
        scene=context.scene

        box1 = layout.box()
        row1 = box1.row()
        for c in scene['colorrenders']:
            layout.label(text=f"{c.title()} Selection= " + scene[c])
            layout.menu(f'OBJECT_MT_{c}_dropdown_menu')

        row1.operator('object.render_holes')

