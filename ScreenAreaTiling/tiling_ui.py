import bpy

from bpy.types import (
    Panel,
    Menu,
)

from . tiling_ops import get_areas


class VIEW3D_PT_tiling_ui_main(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SAT"
    bl_label = "Screen Area Tiling"
    bl_idname = "VIEW3D_PT_tiling_ui_main"

    @classmethod
    def poll(cls, context):
        pref = bpy.context.preferences.addons["ScreenAreaTiling"].preferences
        return pref.sidebar_toggle

    def draw(self, context):
        layout = self.layout
        pref = bpy.context.preferences.addons["ScreenAreaTiling"].preferences

        box = layout.box()
        col = box.column()
        col.label(text="Area Settings:")

        area_dict = {
            "RIGHT": {"name": "Right", "type": "area_types_right", "ratio": "split_ratio_right"},
            "LEFT": {"name": "Left", "type": "area_types_left", "ratio": "split_ratio_left"},
            "TOP": {"name": "Top", "type": "area_types_top", "ratio": "split_ratio_top"},
            "BOTTOM": {"name": "Bottom", "type": "area_types_bottom", "ratio": "split_ratio_bottom"},
        }

        for key in area_dict.keys():
            area = area_dict[key]
            col.separator()
            col.label(text=area["name"])
            col.prop(pref, area["type"], text="")
            col.prop(pref, area["ratio"])

        col.operator("sat.move_area")


class VIEW3D_MT_PIE_tiling_ui_main(Menu):
    bl_label = "Screen Area Tiling"

    def draw(self, context):
        layout = self.layout

        area_dictionary = get_areas()
        parent_area_pointer = str(bpy.context.area.as_pointer())

        directions = ["LEFT", "RIGHT", "BOTTOM", "TOP"]

        pie = layout.menu_pie()
        for direction in directions:
            title = direction.title()
            if parent_area_pointer+direction in area_dictionary.keys():
                toggle = pie.operator(
                    "sat.close_area", text=f"Close {title} Area", icon="REMOVE")
                toggle.direction = direction

            else:
                pie.operator(
                    "sat.split_area", text=f"Split to {title} Area", icon="ADD").direction = direction

        pie.operator("sat.move_area")


classes = (
    VIEW3D_PT_tiling_ui_main,
    VIEW3D_MT_PIE_tiling_ui_main,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
