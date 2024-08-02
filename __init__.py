bl_info = {
    "name": "Align Toolkit",
    "author": "Javier Hernández Morel",
    "blender": (2, 80, 0),
    "category": "Object",
}

import importlib
import bpy

# Importa los sub-addons
from . import align_cursor_to_normal
from . import align_object_to_cursor
from . import set_pivot_to_base
from . import set_pivot_to_cursor

# Lista de sub-addons
sub_addons = [
    align_cursor_to_normal,
    align_object_to_cursor,
    set_pivot_to_base,
    set_pivot_to_cursor,
]

def register():
    for addon in sub_addons:
        importlib.reload(addon)
        addon.register()

def unregister():
    for addon in sub_addons:
        addon.unregister()
