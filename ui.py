import bpy
from . import uilists

from . import display

from . import button

from .infotxt import infotxt


class xdModalPane:
    bl_space_type = "USER_PREFERENCES"
    bl_region_type = "WINDOW"
    bl_options = {"HIDE_HEADER"}
    bl_label = " "
    @classmethod
    def poll(self,context):
        return context.window_manager.xd.activate and context.window_manager.xd.view_mode == self.xd_mode


class XD_MT_library_menu(bpy.types.Menu):
    bl_idname = "XD_MT_library_menu"
    bl_label = "Library"
    def draw(self,context):
        layout = self.layout
        layout.operator("xd.add_library",text="Add Library...",icon="ZOOMIN")
    

class XD_PT_libraries(bpy.types.Panel,xdModalPane):
    xd_mode = "LIBRARY"
    bl_options = set()
    def draw_header(self,context):
        self.layout.menu("XD_MT_library_menu")
    def draw(self,context):
        self.layout.prop(context.window_manager.xd.layout,"libraries",expand=True)
        if context.window_manager.xd.layout.libraries == "SPLIT":
            split = self.layout.split(percentage=0.25)
            display.libraries(split.column(),context)
            display.paths(split.column(),context)
        elif context.window_manager.xd.layout.libraries == "LIST":
            display.ls_libraries(self.layout,context)
      

class XD_PT_paths(bpy.types.Panel,xdModalPane):
    xd_mode = "PATH"
    def draw(self,context):
        self.layout.prop(context.window_manager.xd.layout,"paths",expand=True)
        if context.window_manager.xd.layout.paths == "SPLIT":
            split = self.layout.split(percentage=0.25)
            display.paths(split.column(),context)
            display.blends(split.column(),context)
        elif context.window_manager.xd.layout.paths == "LIST":
            display.ls_paths(self.layout,context)


class XD_PT_blends(bpy.types.Panel,xdModalPane):
    xd_mode = "BLEND"
    def draw(self,context):
        self.layout.prop(context.window_manager.xd.layout,"blends",expand=True)
        if context.window_manager.xd.layout.blends == "SPLIT":
            split = self.layout.split(percentage=0.25)
            display.blends(split.column(),context)
            display.assets(split.column(),context)
        elif context.window_manager.xd.layout.blends == "LIST":
            display.ls_blends(self.layout,context)


class XD_PT_assets(bpy.types.Panel,xdModalPane):
    xd_mode = "ASSET"
    def draw(self,context):
        self.layout.prop(context.window_manager.xd.layout,"assets",expand=True)
        if context.window_manager.xd.layout.assets == "SPLIT":
            split = self.layout.split(percentage=0.25)
            display.categories(split.column(),context)
            display.assets(split.column(),context)
        elif context.window_manager.xd.layout.assets == "LIST":
            display.ls_assets(self.layout,context)


class XD_PT_categories(bpy.types.Panel,xdModalPane):
    xd_mode = "CATEGORY"
    def draw(self,context):
        display.category(self.layout,context)


class XD_PT_banks(bpy.types.Panel,xdModalPane):
    xd_mode = "BANK"
    def draw(self,context):
        layout = self.layout
        r = [[[] for i in range(10)] for j in range(10)]
        split = layout.split(percentage=0.1)
        for i in range(10):
            col = split.column(align=True)
            box = col.box()
            for j in range(10):
                row = box.row(align=True)
                row.label(icon="DOT")
                r[i][j].append(row)
        for b,s,a,i in context.window_manager.xd.cx.execute("select banks.bank,banks.slot,assets.name,assets.id from banks join assets on banks.asset_id=assets.id"):
            r[b][s][0].operator("xd.load_asset",text=a,icon="LIBRARY_DATA_DIRECT").asset_id = i


class XD_PT_notes(bpy.types.Panel,xdModalPane):
    xd_mode = "NOTE"
    def draw(self,context):
        layout = self.layout
        display.notes(layout,context)


class XD_PT_info(bpy.types.Panel,xdModalPane):
    xd_mode = "INFO"
    def draw(self,context):
        layout = self.layout
        split = layout.split(percentage=0.1)
        col = split.column()
        col.label("Information",icon="QUESTION")
        col = split.column()
        list(map(col.label,infotxt))

