import bpy

from bpy.types import (
    Operator,
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

old_areas = []
area_dictionary = {}


def get_areas():
    return area_dictionary


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
        wm = bpy.context.window_manager
        sat_props = wm.sat_props

        old_areas.clear()

        for area in areas:
            old_areas.append(area)

        hor = ["TOP", "BOTTOM"]

        if self.direction in hor:
            split_direction = "HORIZONTAL"

        else:
            split_direction = "VERTICAL"

        inverse = ["RIGHT", "TOP"]
        if self.direction in inverse:
            factor = 100 - sat_props.split_ratio

        else:
            factor = sat_props.split_ratio

        bpy.ops.screen.area_split(direction=split_direction, factor=factor/100)

        if sat_props.split_ratio < 50:
            for new_area in areas:
                if new_area not in old_areas:
                    new_area.ui_type = sat_props.area_types
                    area_dictionary.update({parent_area_pointer+self.direction: new_area.as_pointer()})
        else:
            area = bpy.context.area
            area.ui_type = sat_props.area_types
            for new_area in areas:
                if new_area not in old_areas:
                    area_dictionary.update({str(new_area.as_pointer())+self.direction: area.as_pointer()})

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
                        bpy.ops.screen.area_close()

                    # bpy.ops.screen.area_close({"area": area})

                    print(area_dictionary)
                    break

            del area_dictionary[parent_area_pointer]

        return {"FINISHED"}


classes = (
    SAT_OT_split_area,
    SAT_OT_close_area,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
