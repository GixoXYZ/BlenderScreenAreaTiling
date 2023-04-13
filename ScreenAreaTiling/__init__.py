import bpy

from . import (
    tiling_ops,
    tiling_ui,
    properties,
)


bl_info = {
    "name": "Screen Area Tiling",
    "author": "Gixo",
    "description": "",
    "blender": (3, 5, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}


def register():
    properties.register()
    tiling_ops.register()
    tiling_ui.register()


def unregister():
    properties.unregister()
    tiling_ops.unregister()
    tiling_ui.unregister()
