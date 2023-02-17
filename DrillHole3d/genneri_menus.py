import bpy

class BaseDropDownMenu(bpy.types.Menu):
    bl_label = ''
    bl_idname = 'OBJECT_MT_Gen'

    def __init__(self,label='Generic',drop_times=None):

        self.bl_label = label
        self.bl_idname = f"OBJECT_MT_{label.lower()}_dropdown_menu"
        self.drop_items=drop_times


    # Define the dropdown options
    def draw(self, context):
        layout = self.layout
        
        dropdown_items = self.drop_items
        
        options= self.create_dropdown_options(dropdown_items)

        # Add the dropdown options to the menu
        for item in options:
            selection=layout.operator(f"object.{self.label}_dropdown_operator", text=item[0])
            selection.option = item[1]
            # self.bl_label= context.scene['sheet_selection']
          
    ''' drop down helper tool'''
    def create_dropdown_options(self,items):
        options = []
        for i,op in enumerate(items):
            row=tuple([op,op,str(i)])
            options.append(row)

        return options

class BaseDropDownOperator(bpy.types.Operator):
        
    bl_label = ''
    bl_idname = 'object._'

    def __init__(self,label='Generic',drop_times=None):
        
        self.bl_label = f'{label} Drop-Down Operator'
        self.bl_idname = f"object.{label.lower()}_dropdown_operator"
        self.drop_items=drop_times
        self.option : bpy.props.StringProperty()


    def execute(self, context):
        scene=context.scene
        print("Selected Render: ", self.option)
        selection=self.option
        scene['rendercol']=self.option
        ##update the headers after a seleceton
        return {'FINISHED'}
