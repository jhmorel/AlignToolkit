import bpy
import mathutils

def set_pivot_to_base():
    obj = bpy.context.active_object
    
    if obj is None:
        print("No object selected")
        return

    # Guardar la posición actual del cursor 3D
    cursor_location = bpy.context.scene.cursor.location.copy()

    # Obtener el bounding box en coordenadas locales
    local_bbox = [mathutils.Vector(corner) for corner in obj.bound_box]

    # Encontrar las coordenadas mínimas en el eje Z (la base del objeto en coordenadas locales)
    min_z = min([v.z for v in local_bbox])
    
    # Encontrar el centro de la base en coordenadas locales
    min_x = min([v.x for v in local_bbox])
    max_x = max([v.x for v in local_bbox])
    min_y = min([v.y for v in local_bbox])
    max_y = max([v.y for v in local_bbox])
    
    base_center_local = mathutils.Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, min_z))
    
    # Convertir la coordenada de la base al espacio mundial
    base_center_world = obj.matrix_world @ base_center_local
    
    # Ajustar el pivote a la base del objeto
    bpy.context.scene.cursor.location = base_center_world
    bpy.context.view_layer.objects.active = obj  # Asegura que el objeto esté activo
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    # Restaurar la posición original del cursor 3D
    bpy.context.scene.cursor.location = cursor_location

class OBJECT_OT_set_pivot_to_base(bpy.types.Operator):
    bl_idname = "object.set_pivot_to_base"
    bl_label = "Set Pivot to Base"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        set_pivot_to_base()
        return {'FINISHED'}

class VIEW3D_PT_set_pivot_to_base_panel(bpy.types.Panel):
    bl_label = "Set Pivot to Base"
    bl_idname = "VIEW3D_PT_set_pivot_to_base_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Align Toolkit'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.set_pivot_to_base")

def register():
    bpy.utils.register_class(OBJECT_OT_set_pivot_to_base)
    bpy.utils.register_class(VIEW3D_PT_set_pivot_to_base_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_set_pivot_to_base)
    bpy.utils.unregister_class(VIEW3D_PT_set_pivot_to_base_panel)
