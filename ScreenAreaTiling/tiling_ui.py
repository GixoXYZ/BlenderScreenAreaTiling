import bpy

from bpy.types import (
    Panel,
)

from . tiling_ops import get_areas


class VIEW3D_PT_tiling_ui_main(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SAT"
    bl_label = "Screen Area Tiling"
    bl_idname = "VIEW3D_PT_tiling_ui_main"

    def draw(self, context):
        wm = bpy.context.window_manager
        sat_props = wm.sat_props
        area_dictionary = get_areas()
        parent_area_pointer = str(bpy.context.area.as_pointer())

        layout = self.layout
        col = layout.column()

        col.label(text="Area Type")
        col.prop(sat_props, "area_types", text="")
        col.prop(sat_props, "split_ratio", text="")

        directions = ["TOP", "BOTTOM", "LEFT", "RIGHT",]

        for direction in directions:
            title = direction.title()
            if parent_area_pointer+direction in area_dictionary.keys():
                row = layout.row()
                row.active_default = True
                top = row.operator("sat.close_area", text=f"Close {title} Area")
                top.direction = direction

            else:
                row = layout.row()
                row.operator("sat.split_area", text=f"Split to {title} Area").direction = direction


classes = (
    VIEW3D_PT_tiling_ui_main,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
