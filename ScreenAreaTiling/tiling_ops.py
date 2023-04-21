import bpy

from bpy.types import (
    Operator,
)

from bpy.props import (
    StringProperty,
    FloatProperty,
    BoolProperty,
)

# TODO if subarea gets deleted manually update the area_dictionary
# TODO find a way to store sub areas when the file closes so they would be recognized when file gets reopened

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

        existing_areas = []
        existing_areas.clear()

        # Saving a list of existing areas
        for area in areas:
            existing_areas.append(area)

        if self.direction == "LEFT":
            factor = (pref.split_ratio_left)/100
            split_direction = "VERTICAL"
            area_type = pref.area_types_left

        elif self.direction == "RIGHT":
            factor = (100 - pref.split_ratio_right)/100
            split_direction = "VERTICAL"
            area_type = pref.area_types_right

        elif self.direction == "TOP":
            factor = (100 - pref.split_ratio_top)/100
            split_direction = "HORIZONTAL"
            area_type = pref.area_types_top

        elif self.direction == "BOTTOM":
            factor = (pref.split_ratio_bottom)/100
            split_direction = "HORIZONTAL"
            area_type = pref.area_types_bottom

        bpy.ops.screen.area_split(direction=split_direction, factor=factor)

        for new_area in areas:
            if new_area not in existing_areas:
                new_area.ui_type = area_type
                area_dictionary.update(
                    {parent_area_pointer+self.direction: new_area.as_pointer()})

        print(area_dictionary)

        return {"FINISHED"}


class SAT_OT_PIE_tiling_ui_main_call(Operator):
    bl_idname = "sat.tiling_ui_main_call"
    bl_label = "SAT Pie Menu Caller"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_tiling_ui_main")
        return {"FINISHED"}


# ---------------------------------------------------------------------------------------------------------

class SAT_OT_close_area(Operator):
    bl_idname = "sat.close_area"
    bl_label = "Close Selected Area"
    bl_description = "Close selected area"

    direction: StringProperty(
        name="Direction",
        default="",
    )

    delay: FloatProperty(
        name="Delay",
        default=0.000001,
    )

    direction: StringProperty(
        name="Direction",
        default="",
    )

    delta: FloatProperty(
        default=0
    )

    def execute(self, context):
        self.cancelled = False
        context.window_manager.modal_handler_add(self)
        self.timer = context.window_manager.event_timer_add(
            self.delay,
            window=context.window
        )

        current_area = bpy.context.area
        parent_area_pointer = current_area.as_pointer()
        parent_area_key = str(parent_area_pointer)+self.direction

        if parent_area_key in area_dictionary.keys():
            areas = bpy.context.screen.areas
            sub_area = None

            for area in areas:
                if area.as_pointer() == area_dictionary[parent_area_key]:
                    sub_area = area
                    break
            org_height = current_area.height + sub_area.height
            org_width = current_area.width + sub_area.width

            if sub_area != None:
                with bpy.context.temp_override(
                    area=sub_area,
                ):
                    bpy.ops.screen.area_close()

            del area_dictionary[parent_area_key]

            horizontal = ["TOP", "BOTTOM"]

            if self.direction in horizontal:
                self.delta = org_height - bpy.context.area.height

            else:
                self.delta = org_width - bpy.context.area.width

            return {"RUNNING_MODAL"}

        else:
            return {"FINISHED"}

    def modal(self, context, event):
        print("Running")
        delta = self.delta
        if delta > 0:
            area = bpy.context.area
            edge = self.direction
            move_cursor = True

            if not area:
                return

            if edge not in {"BOTTOM", "LEFT", "RIGHT"}:
                edge = "TOP"

            mouse_x, mouse_y = event.mouse_x, event.mouse_y
            x, y = mouse_x, mouse_y
            if edge == "TOP":
                y = area.y + area.height
                mouse_y += delta * move_cursor
            elif edge == "BOTTOM":
                y = area.y
                mouse_y += delta * move_cursor
                delta = -delta
            elif edge == "RIGHT":
                x = area.x + area.width
                mouse_x += delta * move_cursor
            elif edge == "LEFT":
                x = area.x
                mouse_x += delta * move_cursor
                delta = -delta

            bpy.context.window.cursor_warp(x, y)
            cmd = (
                "bpy.ops.screen.area_move(x=%d, y=%d, delta=%d);"
                "bpy.context.window.cursor_warp(%d, %d)"
            ) % (x, y, delta, mouse_x, mouse_y)

            if event.type == "TIMER":
                if self.cancelled:
                    context.window_manager.event_timer_remove(self.timer)
                    self.timer = None
                    return {"FINISHED"}

                if self.timer.time_duration >= self.delay:
                    try:
                        exec(cmd, None)
                    except Exception as err:
                        print(err)
                    self.cancelled = True
                    print("Moved")
                    return {"FINISHED"}

            return {"PASS_THROUGH"}


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
