import bpy

from bpy.types import (
    AddonPreferences,
)

from bpy.props import (
    IntProperty,
    EnumProperty,
    BoolProperty,
)


# TODO Get area type items from ui_type.
"""
def area_type_items_callback(self, context):
    return bpy.types.Area.bl_rna.properties['ui_type'].enum_items
"""


class SATPreferences(AddonPreferences):
    bl_idname = __package__

    sidebar_toggle: BoolProperty(
        name="Toggle Sidebar Panel",
        default=False,
    )

    area_types = [
        ("VIEW_3D", "3D Viewport", "", "VIEW3D", 0),
        ("IMAGE_EDITOR", "Image Editor", "", "IMAGE", 1),
        ("UV", "UV Editor", "", "UV", 2),
        ("CompositorNodeTree", "Compositor", "", "NODE_COMPOSITING", 3),
        ("TextureNodeTree", "Texture Node Editor", "", "NODE_TEXTURE", 4),
        ("GeometryNodeTree", "Geometry Node Editor", "", "GEOMETRY_NODES", 5),
        ("ShaderNodeTree", "Shader Editor", "", "NODE_MATERIAL", 6),
        ("SEQUENCE_EDITOR", "Video Sequencer", "", "SEQUENCE", 7),
        ("CLIP_EDITOR", "Movie Clip Editor", "", "TRACKER", 8),
        ("DOPESHEET", "Dope Sheet", "", "ACTION", 9),
        ("TIMELINE", "Timeline", "", "TIME", 10),
        ("FCURVES", "Graph Editor", "", "GRAPH", 11),
        ("DRIVERS", "Drivers", "", "DRIVER", 12),
        ("NLA_EDITOR", "Nonlinear Animation", "", "NLA", 13),
        ("TEXT_EDITOR", "Text Editor", "", "TEXT", 14),
        ("CONSOLE", "Python Console", "", "CONSOLE", 15),
        ("INFO", "Info", "", "INFO", 16),
        ("OUTLINER", "Outliner", "", "OUTLINER", 17),
        ("PROPERTIES", "Properties", "", "PROPERTIES", 18),
        ("FILES", "File Browser", "", "FILEBROWSER", 19),
        ("ASSETS", "Asset Browser", "", "ASSET_MANAGER", 20),
        ("SPREADSHEET", "Spreadsheet", "", "SPREADSHEET", 21),
        ("PREFERENCES", "Preferences", "", "PREFERENCES", 22),
    ]

    area_type_left: EnumProperty(
        name="Left Editor Type",
        items=area_types,
        default="ShaderNodeTree",
    )

    area_type_right: EnumProperty(
        name="Right Editor Type",
        items=area_types,
        default="GeometryNodeTree",
    )

    area_type_bottom: EnumProperty(
        name="Bottom Editor Type",
        items=area_types,
        default="ASSETS",
    )

    area_type_top: EnumProperty(
        name="Top Editor Type",
        items=area_types,
        default="INFO",
    )

    ratio_default = 20
    ratio_min = 5
    ratio_max = 45

    split_ratio_left: IntProperty(
        name="Left Split Ratio (%)",
        default=ratio_default,
        min=ratio_min,
        max=ratio_max,
    )

    split_ratio_right: IntProperty(
        name="Right Split Ratio (%)",
        default=ratio_default,
        min=ratio_min,
        max=ratio_max,
    )

    split_ratio_bottom: IntProperty(
        name="Bottom Split Ratio (%)",
        default=ratio_default,
        min=ratio_min,
        max=ratio_max,
    )

    split_ratio_top: IntProperty(
        name="Top Split Ratio (%)",
        default=ratio_default,
        min=ratio_min,
        max=ratio_max,
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        col = box.column()
        col.label(text="Area Settings:")

        area_dict = {
            "LEFT": {"name": "Left", "type": "area_type_left", "ratio": "split_ratio_left"},
            "RIGHT": {"name": "Right", "type": "area_type_right", "ratio": "split_ratio_right"},
            "TOP": {"name": "Top", "type": "area_type_top", "ratio": "split_ratio_top"},
            "BOTTOM": {"name": "Bottom", "type": "area_type_bottom", "ratio": "split_ratio_bottom"},
        }

        for area in area_dict.values():
            col.separator()
            col.label(text=area["name"])
            row = col.row()
            row.prop(self, area["type"], text="")
            row.prop(self, area["ratio"])

        box = layout.box()
        col = box.column()
        col.label(text="Sidebar Settings:")
        col.prop(self, "sidebar_toggle")


classes = (
    SATPreferences,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
