import bpy

from bpy.types import (
    Operator,
)

from bpy.props import (
    StringProperty,
)


addon_keymaps = []
old_areas = []
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
    kmi = km.keymap_items.new(
        SAT_OT_PIE_tiling_ui_main_call.bl_idname, "SPACE", "PRESS", alt=True)
    addon_keymaps.append((km, kmi))


def _remove_hotkey():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


class SAT_OT_split_area(Operator):
    bl_idname = "sat.split_area"
    bl_label = "Split Selected Area"
    bl_description = "Split selected screen area"

    direction: StringProperty(
        name="Direction",
        default="",
    )

    def execute(self, context):
        areas = bpy.context.screen.areas
        parent_area_pointer = str(bpy.context.area.as_pointer())
        pref = bpy.context.preferences.addons["ScreenAreaTiling"].preferences

        old_areas.clear()

        for area in areas:
            old_areas.append(area)

        if self.direction == "LEFT":
            factor = (pref.split_ratio_left)/100
            split_direction = "VERTICAL"
            area_type = pref.area_types_left

        if self.direction == "RIGHT":
            factor = (100 - pref.split_ratio_right)/100
            split_direction = "VERTICAL"
            area_type = pref.area_types_right

        if self.direction == "TOP":
            factor = (100 - pref.split_ratio_top)/100
            split_direction = "HORIZONTAL"
            area_type = pref.area_types_top

        if self.direction == "BOTTOM":
            factor = (pref.split_ratio_bottom)/100
            split_direction = "HORIZONTAL"
            area_type = pref.area_types_bottom

        bpy.ops.screen.area_split(direction=split_direction, factor=factor)

        for new_area in areas:
            if new_area not in old_areas:
                new_area.ui_type = area_type
                area_dictionary.update({parent_area_pointer+self.direction: new_area.as_pointer()})

        print(area_dictionary)

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
        parent_area_pointer = str(bpy.context.area.as_pointer())+self.direction
        if parent_area_pointer in area_dictionary.keys():
            areas = bpy.context.screen.areas

            for area in areas:
                if area.as_pointer() == area_dictionary[parent_area_pointer]:
                    with bpy.context.temp_override(
                        area=area,
                    ):
                        bpy.ops.screen.area_close('INVOKE_DEFAULT')

                    # bpy.ops.screen.area_close({"area": area})
                    # print(area_dictionary)

                    break

            del area_dictionary[parent_area_pointer]

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
