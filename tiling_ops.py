import bpy
import re

from bpy.types import (
    Operator,
)

from bpy.props import (
    StringProperty,
)

# TODO if sub area gets deleted manually update the area_dictionary
# TODO find a way to store sub areas when the file closes so they would be
# recognized when file gets reopened or close all sub areas on exit

addon_keymaps = []
area_dictionary = {}


def get_areas():
    return area_dictionary


def _add_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if not kc:
        print("Keymap Error")
        return

    km = kc.keymaps.new(name="Object Mode", space_type="EMPTY")
    # Adding "Alt" + "Space" as pie menu hotkey
    kmi = km.keymap_items.new(
        SAT_OT_PIE_tiling_ui_main_call.bl_idname, "SPACE", "PRESS", alt=True)
    addon_keymaps.append((km, kmi))


def _remove_hotkey():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def close_area(self, context, direction, parent_area_pointer, parent_area_key):
    factor = 0
    # Checking if there's any split sub areas in current 3d viewport
    if parent_area_key in area_dictionary.keys():
        areas = bpy.context.screen.areas
        outside_area = None
        sub_area = next(
            (
                area
                for area in areas
                if area.as_pointer() == area_dictionary[parent_area_key]
            ),
            None,
        )

    # If selected sub area exists
    if sub_area is not None:
        # Checking outer areas to find if any of them has the same height or width as sub area
        for area in areas:
            area_pointer = area.as_pointer()
            pointer_list = [sub_area.as_pointer(), parent_area_pointer]

            width_check = (area.width == sub_area.width)
            height_check = (area.height == sub_area.height)
            wh_check = None
            xy_check = None

            if direction == "RIGHT":
                split_direction = "HORIZONTAL"
                sub_area_right_edge_x = (sub_area.x + sub_area.width)
                edge_delta = (area.x - sub_area_right_edge_x)
                if area_pointer not in pointer_list and height_check and 10 > edge_delta > -10:
                    outside_area = area
                    wh_check = (area.width == outside_area.width)
                    xy_check = (area.y > outside_area.y)

            elif direction == "LEFT":
                split_direction = "HORIZONTAL"
                area_right_edge_x = (area.x + area.width)
                edge_delta = (sub_area.x - area_right_edge_x)
                if area_pointer not in pointer_list and height_check and 10 > edge_delta > -10:
                    outside_area = area
                    wh_check = (area.width == outside_area.width)
                    xy_check = (area.x > outside_area.x)

            elif direction == "TOP":
                split_direction = "VERTICAL"
                sub_area_top_edge_y = (sub_area.y + sub_area.height)
                edge_delta = (area.y - sub_area_top_edge_y)
                if area_pointer not in pointer_list and width_check and 10 > edge_delta > -10:
                    outside_area = area
                    wh_check = (area.height == outside_area.height)
                    xy_check = (area.y > outside_area.y)

            elif direction == "BOTTOM":
                split_direction = "VERTICAL"
                area_top_edge_y = (area.y + area.height)
                edge_delta = (sub_area.y - area_top_edge_y)
                if area_pointer not in pointer_list and width_check and 10 > edge_delta > -10:
                    outside_area = area
                    wh_check = (area.height == outside_area.height)
                    xy_check = (area.y > outside_area.y)

            for i, area in enumerate(areas):
                if area == outside_area:
                    outside_area_index = i

            for i, area in enumerate(areas):
                if wh_check and i < outside_area_index and xy_check:
                    factor = 0
                else:
                    factor = 1
                break

    # If there was any outer area with the same height or width as sub area
    if outside_area is not None and outside_area.as_pointer() not in area_dictionary.values():
        existing_areas = []
        existing_areas.clear()

        # Saving a list of existing areas
        for area in areas:
            existing_areas.append(area)

        # Splitting outer area to avoid the closed area getting added to it
        with bpy.context.temp_override(
            area=outside_area,
        ):

            bpy.ops.screen.area_split(
                direction=split_direction,
                factor=factor
            )

        # Closing sub area
        with bpy.context.temp_override(
            area=sub_area,
        ):
            bpy.ops.screen.area_close()

        # Removing the dummy split area created in outer area
        for area in areas:
            if area not in existing_areas:
                dummy = area
                with bpy.context.temp_override(
                    area=dummy,
                ):
                    bpy.ops.screen.area_close()
                break

    # If there was no outer area with the same height or width as sub area
    elif sub_area is not None:
        with bpy.context.temp_override(
            area=sub_area,
        ):
            bpy.ops.screen.area_close()

        # bpy.ops.screen.area_close({"area": area})

    # Removing sub area from dictionary
    del area_dictionary[parent_area_key]


def split_area(self, context, direction):
    areas = bpy.context.screen.areas
    parent_area_pointer = str(bpy.context.area.as_pointer())
    pref = bpy.context.preferences.addons[__package__].preferences

    existing_areas = []
    existing_areas.clear()

    # Saving a list of existing areas
    for area in areas:
        existing_areas.append(area)

    # Setting the rotation and direction of split
    if direction == "LEFT":
        factor = (pref.split_ratio_left) / 100
        split_direction = "VERTICAL"
        area_type = pref.area_types_left

    elif direction == "RIGHT":
        factor = (100 - pref.split_ratio_right) / 100
        split_direction = "VERTICAL"
        area_type = pref.area_types_right

    elif direction == "TOP":
        factor = (100 - pref.split_ratio_top) / 100
        split_direction = "HORIZONTAL"
        area_type = pref.area_types_top

    elif direction == "BOTTOM":
        factor = (pref.split_ratio_bottom) / 100
        split_direction = "HORIZONTAL"
        area_type = pref.area_types_bottom

    # Splitting 3d viewport based on selected direction
    bpy.ops.screen.area_split(direction=split_direction, factor=factor)

    # Changing the newly created sub area's type
    for new_area in areas:
        if new_area not in existing_areas:
            new_area.ui_type = area_type
            area_dictionary.update(
                {parent_area_pointer + direction: new_area.as_pointer()}
            )


class SAT_OT_split_area(Operator):
    bl_idname = "sat.split_area"
    bl_label = "Split Selected Area"
    bl_description = "Split selected screen area"

    direction: StringProperty(
        name="Direction",
        default="",
    )

    def execute(self, context):
        split_area(self, context, self.direction)

        return {"FINISHED"}


class SAT_OT_close_area(Operator):
    bl_idname = "sat.close_area"
    bl_label = "Close Selected Area"
    bl_description = "Close selected area"

    direction: StringProperty(
        name="Direction",
        default="",
    )

    def execute(self, context):
        parent_area_pointer = bpy.context.area.as_pointer()
        parent_area_key = str(parent_area_pointer) + self.direction
        sub_areas = [key for key in area_dictionary.keys() if key.startswith(str(parent_area_pointer))]
        rev_sub_areas = sub_areas[::-1]

        for sub_area in rev_sub_areas:
            direction = re.sub(r"\d", "", sub_area)
            close_area(self, context, direction, parent_area_pointer, sub_area)

        sub_areas.remove(parent_area_key)
        if sub_areas:
            directions = [re.sub(r"\d", "", char) for char in sub_areas]
            for direction in directions:
                print(direction)
                split_area(self, context, direction)

        return {"FINISHED"}


class SAT_OT_PIE_tiling_ui_main_call(Operator):
    bl_idname = "sat.tiling_ui_main_call"
    bl_label = "SAT Pie Menu Caller"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_tiling_ui_main")
        return {"FINISHED"}


classes = (
    SAT_OT_split_area,
    SAT_OT_close_area,
    SAT_OT_PIE_tiling_ui_main_call,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    _add_hotkey()


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    _remove_hotkey()
