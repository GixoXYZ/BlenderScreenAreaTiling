import bpy

from . import (
    preferences,
    tiling_ops,
    tiling_ui,
)


bl_info = {
    "name": "Screen Area Tiling",
    "author": "Gixo <notgixo@proton.me>",
    "description": "Split screen areas using a pie menu.",
    "blender": (3, 0, 0),
    "version": (0, 1, 1, "alpha"),
    "location": 'View3D > "Alt" + "Space"',
    "warning": "",
    "support": "COMMUNITY",
    "category": "Interface",
}


def register():
    preferences.register()
    tiling_ops.register()
    tiling_ui.register()


def unregister():
    preferences.unregister()
    tiling_ops.unregister()
    tiling_ui.unregister()
