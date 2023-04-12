import bpy

from bpy.types import (
    PropertyGroup,
)

from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
    StringProperty,
    CollectionProperty,
)


class SAT_Properties(PropertyGroup):
    area_types: EnumProperty(
        name="Area Types",
        items=[
            ("VIEW_3D", "3D Viewport", ""),
            ("IMAGE_EDITOR", "Image Editor", ""),
            ("UV", "UV Map", ""),
            ("CompositorNodeTree", "Compositor Node Tree", ""),
            ("TextureNodeTree", "Texture Node Tree", ""),
            ("GeometryNodeTree", "Geometry Node Tree", ""),
            ("ShaderNodeTree", "Shader Node Tree", ""),
            ("SEQUENCE_EDITOR", "Sequence Editor", ""),
            ("CLIP_EDITOR", "Clip Editor", ""),
            ("DOPESHEET", "Dopesheet", ""),
            ("TIMELINE", "Timeline", ""),
            ("FCURVES", "F-Curves", ""),
            ("DRIVERS", "Drivers", ""),
            ("NLA_EDITOR", "NLA Editor", ""),
            ("TEXT_EDITOR", "Text Editor", ""),
            ("CONSOLE", "Console", ""),
            ("INFO", "Info", ""),
            ("OUTLINER", "Outliner", ""),
            ("PROPERTIES", "Properties", ""),
            ("FILES", "Files", ""),
            ("ASSETS", "Assets", ""),
            ("SPREADSHEET", "Spreadsheet", ""),
            ("PREFERENCES", "Preferences", ""),
        ],
    )

    split_ratio: IntProperty(
        name="Split_Ratio",
        default=25,
        min=5,
        max=95,
    )


classes = (
    SAT_Properties,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.WindowManager.sat_props = PointerProperty(type=SAT_Properties)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.WindowManager.sat_props
