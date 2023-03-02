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

class EXAMPLE_OT_modal_operator(bpy.types.Operator): 
    
    bl_idname = "example.modal_operator"
    bl_label = "Modal Operator"
    
    def __init__(self):
        
        self.step = 0
        self.timer = None
        self.done = False
        self.max_step = None
        
        self.timer_count = 0 #timer count, need to let a little bit of space between updates otherwise gui will not have time to update
                
    def modal(self, context, event):
        
        global Operations
        
        #update progress bar
        if not self.done:
            print(f"Updating: {self.step+1}/{self.max_step}")
            #update progess bar
            context.object.progress = ((self.step+1)/(self.max_step))*100
            #update label
            context.object.progress_label = list(Operations.keys())[self.step]
            #send update signal
            context.area.tag_redraw()
            
            
        #by running a timer at the same time of our modal operator
        #we are guaranteed that update is done correctly in the interface
        
        if event.type == 'TIMER':
            
            #but wee need a little time off between timers to ensure that blender have time to breath, so we have updated inteface
            self.timer_count +=1
            if self.timer_count==10:
                self.timer_count=0
                
                if self.done:
                    
                    print("Finished")
                    self.step = 0
                    context.object.progress = 0
                    context.window_manager.event_timer_remove(self.timer)
                    context.area.tag_redraw()
                    
                    return {'FINISHED'}
            
                if self.step < self.max_step:
                        
                    #run step function
                    list(Operations.values())[self.step]()
                    
                    self.step += 1
                    if self.step==self.max_step:
                        self.done=True
                    
                    return {'RUNNING_MODAL'}
        
        return {'RUNNING_MODAL'}