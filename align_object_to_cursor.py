import bpy

def align_object_to_cursor():
    cursor_location = bpy.context.scene.cursor.location
    cursor_rotation = bpy.context.scene.cursor.rotation_euler
    
    obj = bpy.context.active_object
    if obj:
        obj.location = cursor_location
        obj.rotation_euler = cursor_rotation
    else:
        print("No object selected")

class OBJECT_OT_align_object_to_cursor(bpy.types.Operator):
    bl_idname = "object.align_object_to_cursor"
    bl_label = "Align Object to Cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        align_object_to_cursor()
        return {'FINISHED'}

class VIEW3D_PT_align_object_to_cursor_panel(bpy.types.Panel):
    bl_label = "Align Object to Cursor"
    bl_idname = "VIEW3D_PT_align_object_to_cursor_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Align Toolkit'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.align_object_to_cursor")

def register():
    bpy.utils.register_class(OBJECT_OT_align_object_to_cursor)
    bpy.utils.register_class(VIEW3D_PT_align_object_to_cursor_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_align_object_to_cursor)
    bpy.utils.unregister_class(VIEW3D_PT_align_object_to_cursor_panel)
