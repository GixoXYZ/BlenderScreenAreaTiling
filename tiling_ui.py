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
        pref = bpy.context.preferences.addons[__package__].preferences
        return pref.sidebar_toggle

    def draw(self, context):
        layout = self.layout
        pref = bpy.context.preferences.addons[__package__].preferences

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
            col.prop(pref, area["type"], text="")
            col.prop(pref, area["ratio"])


class VIEW3D_MT_PIE_tiling_ui_main(Menu):
    bl_label = "Screen Area Tiling"

    def draw(self, context):
        layout = self.layout
        area_dictionary = get_areas()
        parent_area_pointer = str(bpy.context.area.as_pointer())
        pref = bpy.context.preferences.addons[__package__].preferences

        directions = ["LEFT", "RIGHT", "BOTTOM", "TOP"]

        pie = layout.menu_pie()
        for direction in directions:
            area_type_enum = pref.bl_rna.properties[f"area_type_{direction.lower()}"].enum_items
            area_type = getattr(pref, f"area_type_{direction.lower()}")
            item = area_type_enum.get(area_type)
            title = item.name
            icon = item.icon
            if parent_area_pointer + direction in area_dictionary.keys():
                toggle = pie.operator("sat.close_area", text=f"Close {title}", icon=icon)
                toggle.direction = direction

            else:
                pie.operator(
                    "sat.split_area", text=f"Open {title}",
                    icon=icon
                ).direction = direction


def view3d_header_icons(self, context):
    layout = self.layout
    area_dictionary = get_areas()
    parent_area_pointer = str(bpy.context.area.as_pointer())
    pref = bpy.context.preferences.addons[__package__].preferences

    directions = ["LEFT", "RIGHT", "TOP", "BOTTOM"]

    row = layout.row(align=True)
    row.alignment = "RIGHT"
    for direction in directions:
        area_type_enum = pref.bl_rna.properties[f"area_type_{direction.lower()}"].enum_items
        area_type = getattr(pref, f"area_type_{direction.lower()}")
        item = area_type_enum.get(area_type)
        title = item.name
        icon = item.icon
        if parent_area_pointer + direction in area_dictionary.keys():
            sub_row = row.row()
            sub_row.active_default = True
            toggle = sub_row.operator("sat.close_area", text=title, icon=icon)
            toggle.direction = direction

        else:
            row.operator(
                "sat.split_area", text=title,
                icon=icon
            ).direction = direction


classes = (
    VIEW3D_PT_tiling_ui_main,
    VIEW3D_MT_PIE_tiling_ui_main,
)


def register():
    bpy.types.VIEW3D_HT_tool_header.append(view3d_header_icons)
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    bpy.types.VIEW3D_HT_tool_header.remove(view3d_header_icons)
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
