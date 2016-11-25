import bpy

from .cats import cats,asset_icons
C = len(cats)

class xdLibraryList(bpy.types.UIList):
    bl_idname = "xd_libraries"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        exclude = context.window_manager.xd.cx.library_exclusion(item.rowid)
        op = row.operator("xd.togx",icon=["VISIBLE_IPO_ON","VISIBLE_IPO_OFF"][exclude],text="")
        op.table = "libraries"
        op.column = "exclude"
        op.index = item.rowid
        op.value = exclude
        row.label(item.name)
        row.label("%i paths" % item.path_count)
        row.label("%i blends" % item.blend_count)


class xdPathList(bpy.types.UIList):
    bl_idname = "xd_paths"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        exclude = context.window_manager.xd.cx.path_exclusion(item.rowid)
        op = row.operator("xd.togx",icon=["VISIBLE_IPO_ON","VISIBLE_IPO_OFF"][exclude],text="")
        op.table = "paths"
        op.column = "exclude"
        op.index = item.rowid
        op.value = exclude
        row.label(item.name)
        row.label(item.mtime)
        row.label("%i blends" % item.blend_count)


class xdBlendList(bpy.types.UIList):
    bl_idname = "xd_blends"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        exclude = context.window_manager.xd.cx.blend_exclusion(item.rowid)
        op = row.operator("xd.togx",icon=["VISIBLE_IPO_ON","VISIBLE_IPO_OFF"][exclude],text="")
        op.table = "blends"
        op.column = "exclude"
        op.index = item.rowid
        op.value = exclude
        row.label(item.name)
        row.label(item.size)
        row.label(item.mtime)
        row.label("%i assets" % item.asset_count)
        row.operator(["xd.scan_blend","xd.prune_blendassets"][bool(item.asset_count)]).blend_id = item.rowid


class xdAssetList(bpy.types.UIList):
    bl_idname = "xd_assets"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.label(item.category,icon=asset_icons[item.category])
        row.label(str(item.note_count),icon=["BLANK1","TEXT"][bool(item.note_count)])
        row.operator("xd.load_asset",text=item.name,icon="LIBRARY_DATA_DIRECT").asset_id = item.rowid

    def filter_items(self,context,data,propname):
        items = getattr(data,propname)
        flt_flags = []
        if self.filter_name:
            flt_flags = bpy.types.UI_UL_list.filter_items_by_name(self.filter_name,self.bitflag_filter_item,items,"name")   
        cats = context.window_manager.xd.show.categories.selection_list(context)
        if 0 < len(cats) < C:
            if flt_flags:
                for i,item in enumerate(data.data):
                    flt_flags[i] &= [1,self.bitflag_filter_item][item.category in cats]
            else:
                flt_flags = [(1,self.bitflag_filter_item)[item.category in cats] for item in data.data]
        return flt_flags,[]


class xdAssetCategegoryList(bpy.types.UIList):
    bl_idname = "xd_catx"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.operator("xd.load_asset",text=item.name).asset_id = item.rowid


class xdNoteList(bpy.types.UIList):
    bl_idname = "xd_notes"
    def draw_item(self,context,layout,data,item,icon,active_data,active_propname):
        row = layout.row()
        row.prop(item,"note")
