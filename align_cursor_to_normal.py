import bpy
import bmesh
import mathutils

def align_cursor_to_normal():
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    # Obtén el contexto de la selección
    sel_faces = [f for f in bm.faces if f.select]
    sel_edges = [e for e in bm.edges if e.select]
    sel_verts = [v for v in bm.verts if v.select]
    
    # Alinea a la normal de la cara seleccionada
    if sel_faces:
        face = sel_faces[0]
        normal = face.normal
        location = face.calc_center_median()
        tangent = (face.verts[1].co - face.verts[0].co).normalized()
        
    # Alinea a la normal de la arista seleccionada
    elif sel_edges:
        edge = sel_edges[0]
        normal = edge.verts[0].normal.lerp(edge.verts[1].normal, 0.5).normalized()
        location = edge.verts[0].co.lerp(edge.verts[1].co, 0.5)
        tangent = (edge.verts[1].co - edge.verts[0].co).normalized()
        
    # Alinea a la normal del vértice seleccionado
    elif sel_verts:
        vert = sel_verts[0]
        normal = vert.normal
        location = vert.co
        # Encontrar un vector tangente para el vértice
        linked_edges = vert.link_edges
        if len(linked_edges) > 0:
            tangent = (linked_edges[0].verts[1].co - linked_edges[0].verts[0].co).normalized()
        else:
            tangent = mathutils.Vector((1, 0, 0))
    
    else:
        print("No hay selección válida")
        return
    
    # Asegúrate de que el vector tangente no sea paralelo a la normal
    if abs(normal.dot(tangent)) == 1.0:
        tangent = mathutils.Vector((1, 0, 0))
    
    binormal = normal.cross(tangent).normalized()
    tangent = binormal.cross(normal).normalized()
    
    # Crear la matriz de orientación
    orientation_matrix = mathutils.Matrix((tangent, binormal, normal)).transposed().to_4x4()
    loc_matrix = mathutils.Matrix.Translation(location)
    transform_matrix = loc_matrix @ orientation_matrix
    
    # Aplicar la orientación al cursor 3D
    bpy.context.scene.cursor.matrix = obj.matrix_world @ transform_matrix

class MESH_OT_align_cursor_to_normal(bpy.types.Operator):
    bl_idname = "mesh.align_cursor_to_normal"
    bl_label = "Align Cursor to Normal"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        align_cursor_to_normal()
        return {'FINISHED'}

class VIEW3D_PT_align_cursor_to_normal_panel(bpy.types.Panel):
    bl_label = "Align Cursor to Normal"
    bl_idname = "VIEW3D_PT_align_cursor_to_normal_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.align_cursor_to_normal")

def register():
    bpy.utils.register_class(MESH_OT_align_cursor_to_normal)
    bpy.utils.register_class(VIEW3D_PT_align_cursor_to_normal_panel)

def unregister():
    bpy.utils.unregister_class(MESH_OT_align_cursor_to_normal)
    bpy.utils.unregister_class(VIEW3D_PT_align_cursor_to_normal_panel)
