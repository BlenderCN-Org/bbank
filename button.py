#this file is just functions for drawing buttons
#which are commented out in __init__.py because they are only for dev
def for_changing_userprefs_back_to_a_timeline(self,context):
    self.layout.operator("xd.areatype_switch").switchto = "TIMELINE"

def for_changing_the_timeline_into_userprefs(self,context):
    op = self.layout.operator("xd.areatype_switch",
        icon="PREFERENCES",text="",emboss=False)
    op.switchto = "USER_PREFERENCES"
    op.post_op = "xd.activate"

def for_splitting_the_viewport_with_an_img_editor(self,context):
    looking_for_target_x_value = context.area.x + context.area.width + 1
    found_one = False
    for area in context.screen.areas:
        if area == context.area:
            continue
        elif area.x == looking_for_target_x_value and area.y == context.area.y:
            found_one = True
            break
    if found_one:
        self.layout.operator("xd.areajoiner",icon="SCREEN_BACK",text="")
    else:
        self.layout.operator("xd.areasplitter",icon="IMAGE_COL",text="")

