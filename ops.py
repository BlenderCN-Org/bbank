import bpy
import os

from . import post

from .cats import cats

post_loadfuncs = {cat:getattr(post,cat) for cat in cats if hasattr(post,cat)}

# this function gets called when there is not found an associated loading function
loadfunc_not_implemented = lambda *_:None

# after loading an asset, call a function to deal with scene linkage
# specific to the type of the asset
def post_load(category,asset,context):
    post_loadfuncs.get(category,loadfunc_not_implemented)(asset,context)

#given an asset id from the database, load it and call the related post_load func
class XD_OT_load_asset(bpy.types.Operator):
    bl_idname = "xd.load_asset"
    bl_label = "load"
    bl_options = {"INTERNAL"}
    asset_id = bpy.props.IntProperty(default=-1,min=-1)
    def execute(self,context):
        cx = context.window_manager.xd.cx
        blend_id,name,category = cx.execute("select blend_id,name,category from assets where id=?",(self.asset_id,)).fetchone()
        blend = cx.execute("select name from blends where id=?",(blend_id,)).fetchone()[0]
        with bpy.data.libraries.load(blend) as (L,G):
            cat = getattr(G,category)
            cat.append(name)
        assetcontainer = getattr(G,category)
        post_load(category,assetcontainer[0],context)
        msg = "%s %s loaded from %s" % (category,name,blend)
        #commented out because breaks the interface when header buttons get replaced by text
        # need to make an area on the header to display messages
        #context.area.header_text_set(msg)
        print(msg)
        return {"FINISHED"}

# remove assets from the database based on which blend they belong to
class XD_OT_prune_blendassets(bpy.types.Operator):
    bl_idname = "xd.prune_blendassets"
    bl_label = "Prune this blend's assets from the database"
    bl_options = {"INTERNAL"}
    blend_id = bpy.props.IntProperty()
    def execute(self,context):
        xd = context.window_manager.xd
        xd.cx.prune_blendassets(self.blend_id)
        xd.view_mode = xd.view_mode
        return {"FINISHED"}

# could probably combine the next two ops into one
# to avoid duplicate code...
class XD_OT_scan_included_blends(bpy.types.Operator):
    bl_idname = "xd.scan_included_blends"
    bl_label = "Scan Included Blends"
    bl_options = {"INTERNAL"}
    def execute(self,context):
        cx = context.window_manager.xd.cx
        for blend_id in cx.included_blends:
            cx.scan_blend_for_assets(blend_id)
        context.window_manager.xd.view_mode = context.window_manager.xd.view_mode
        return {"FINISHED"}

class XD_OT_scan_blend(bpy.types.Operator):
    bl_idname = "xd.scan_blend"
    bl_label = "Scan Blend"
    bl_options = {"INTERNAL"}
    blend_id = bpy.props.IntProperty()
    def execute(self,context):
        context.window_manager.xd.cx.scan_blend_for_assets(self.blend_id)
        context.window_manager.xd.view_mode = context.window_manager.xd.view_mode
        return {"FINISHED"}


# more or less an afterthought to be able to annotate
# see WATDO
class XD_OT_annotate_asset(bpy.types.Operator):
    bl_idname = "xd.annotate_asset"
    bl_label = "add note to asset"
    bl_options = {"INTERNAL"}
    index = bpy.props.IntProperty()
    blend = bpy.props.StringProperty()
    category = bpy.props.StringProperty()
    asset = bpy.props.StringProperty()
    text = bpy.props.StringProperty()
    def draw(self,context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(self.blend)
        row.label(self.category)
        row.label(self.asset)
        row = layout.row(align=True)
        row.prop(self,"text",text="")
    def invoke(self,context,event):
        self.blend,self.asset,self.category = context.window_manager.xd.cx.asset_info(self.index)
        context.window_manager.invoke_props_dialog(self,width=context.window.width-100,height=context.window.height-100)
        return {"RUNNING_MODAL"}
    def execute(self,context):
        xd = context.window_manager.xd
        cx = xd.cx
        cx.execute("insert into notes (asset_id,note) values (?,?)",(self.index,self.text))
        nct = cx.execute("select count(*) from notes where asset_id=?",(self.index,)).fetchone()[0]
        cx.execute("update assets set note_count=? where id=?",(nct,self.index))
        cx.commit()
        xd.view_mode = xd.view_mode
        return {"FINISHED"}

# adding a library is the main bit of user input that is needed.
class XD_OT_add_library(bpy.types.Operator):
    bl_idname = "xd.add_library"
    bl_label = "Add Library"
    bl_description = "Choose a directory which contains blend files."
    bl_options = {"INTERNAL"}
    directory = bpy.props.StringProperty(subtype="DIR_PATH")
    recurse = bpy.props.BoolProperty(default=True)
    def invoke(self,context,event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
    def execute(self,context):
        context.window_manager.xd.cx.add_library(self.directory,self.recurse)
        context.window_manager.xd.view_mode = "LIBRARY"
        return {"FINISHED"}


# togx = toggle exclusion.  (state of being included)
class XD_OT_togx(bpy.types.Operator):
    bl_idname = "xd.togx"
    bl_label = "xd:togx"
    bl_options = {"INTERNAL"}
    table = bpy.props.StringProperty()
    column = bpy.props.StringProperty()
    index = bpy.props.IntProperty()
    value = bpy.props.BoolProperty()
    def execute(self,context):
        cx = context.window_manager.xd.cx
        statement = "update %s set %s=? where id=?" % (self.table,self.column)
        arguments = (int(not self.value),self.index)
        cx.execute(statement,arguments)
        cx.commit()
        return {"FINISHED"}


# delete the database file
class XD_OT_database_delete(bpy.types.Operator):
    bl_idname = "xd.database_delete"
    bl_label = "Delete Database"
    bl_options = {"INTERNAL"}
    def execute(self,context):
        dbfile = context.user_preferences.addons[__package__].preferences.dbfile
        os.remove(dbfile)
        return {"FINISHED"}


# remove a library (path) from the database
# delete cascades to paths,blends,assets,notes... but currently not banks maybe thats a bug
class XD_OT_remove_library(bpy.types.Operator):
    bl_idname = "xd.remove_library"
    bl_label = "Remove Library"
    bl_options = {"INTERNAL"}
    index = bpy.props.IntProperty(default=-1)
    def execute(self,context):
        context.window_manager.xd.cx.remove_library(self.index)
        return {"FINISHED"}

# this is basically the entry point for the program
# SINCE I finally learned to use blender's built-in preset system, this needs a rework
class XD_OT_activate(bpy.types.Operator):
    bl_idname = "xd.activate"
    bl_label = "xd:activate"
    bl_options = {"INTERNAL"}
    def execute(self,context):
        context.window_manager.xd.activate = True
        return {"FINISHED"}

#ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^
#next three ops are commented out in __init__.py for the time being
# they are irrelevant to the functioning
class XD_OT_areatype_switch(bpy.types.Operator):
    bl_idname = "xd.areatype_switch"
    bl_label = "areatype_switch"
    bl_options = {"INTERNAL"}
    switchto = bpy.props.StringProperty()
    post_op = bpy.props.StringProperty()
    post = bpy.props.BoolProperty()
    def invoke(self,context,event):
        self.post = event.shift
        return self.execute(context)
    def execute(self,context):
        context.area.type = self.switchto
        if self.post and self.post_op:
            __import__("_bpy").ops.call(self.post_op,None)
        return {"FINISHED"}

class XD_OT_spliteroo(bpy.types.Operator):
    bl_idname = "xd.areasplitter"
    bl_label = "Split (VIEW_3D|IMAGE_EDITOR)"
    bl_options = {"INTERNAL"}
    def execute(self,context):
        thisarea = context.area
        thistype = context.area.type
        thisarea.type = "IMAGE_EDITOR"
        areas = [area for area in context.screen.areas]
        bpy.ops.screen.area_split(direction="VERTICAL")
        a = None
        for area in context.screen.areas:
            if area not in areas:
                a = area
                break
        if a:
            a.type = thistype
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

class XD_OT_joinareas(bpy.types.Operator):
    bl_idname = "xd.areajoiner"
    bl_label = "join areas"
    bl_options = {"INTERNAL"}
    def execute(self,context):
        one = context.area
        tx = one.x + one.width + 1
        two = None
        for area in context.screen.areas:
            if area.x == tx and area.y == one.y:
                two = area
                break
        if two:
            bpy.ops.screen.area_join(min_x=one.x,min_y=one.y,max_x=two.x,max_y=two.y)
            bpy.ops.screen.screen_full_area()
            bpy.ops.screen.screen_full_area()
        else:
            return {"CANCELLED"}
        return {"FINISHED"}

#ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^ˆ^

# assign an asset to a slot of a bank
# for easy loading
class XD_OT_bank_put(bpy.types.Operator):
    bl_idname = "xd.bankput"
    bl_label = "bank put"
    bl_options = {"INTERNAL"}
    bank = bpy.props.IntProperty()
    slot = bpy.props.IntProperty()
    a_id = bpy.props.IntProperty()
    def execute(self,context):
        xd = context.window_manager.xd
        xd.cx.execute("insert into banks(bank,slot,asset_id) values (?,?,?)",(self.bank,self.slot,self.a_id))
        xd.cx.commit()
        return {"FINISHED"}

# wanted to make it so you could "dial-an-asset" on the number-pad
# but currently commented out in __init__.py
# because I don't know the polite way to assign hotkeys
class XD_OT_bank_leader(bpy.types.Operator):
    bl_idname = "xd.bank"
    bl_label = "bank leader key"
    bl_options = {"INTERNAL"}
    bank_wait = bpy.props.BoolProperty()
    def modal(self, context, event):
        v = -1
        if not event.value == "PRESS":
            return {"RUNNING_MODAL"}
        if event.type in {"ESC","Q"}:
            return {"CANCELLED"}
        elif event.type == "NUMPAD_0":
            v = 0
        elif event.type == "NUMPAD_1":
            v = 1
        elif event.type == "NUMPAD_2":
            v = 2
        elif event.type == "NUMPAD_3":
            v = 3
        elif event.type == "NUMPAD_4":
            v = 4
        elif event.type == "NUMPAD_5":
            v = 5
        elif event.type == "NUMPAD_6":
            v = 6
        elif event.type == "NUMPAD_7":
            v = 7
        elif event.type == "NUMPAD_8":
            v = 8
        elif event.type == "NUMPAD_9":
            v = 9
        elif event.type == "NUMPAD_ASTERIX":
            if not self.bank_wait:
                msg = "Bank #?"
                context.area.header_text_set(text=msg)
                self.bank_wait = True
            else:
                xd = context.window_manager.xd
                cx = xd.cx
                if not cx and context.user_preferences.addons[__package__].preferences.auto:
                    from .xddb import init_on
                    init_on(context.user_preferences.addons[__package__].preferences.dbfile)
                    cx = xd.cx
                if not cx:
                    return {"CANCELLED"}
                list(map(print,cx.execute("select banks.bank,banks.slot,assets.name,assets.category,blends.name from banks join assets on banks.asset_id=assets.id join blends on assets.blend_id=blends.id where banks.asset_id>-1")))
                return {"FINISHED"}
        if v > -1:
            if self.bank_wait:
                context.window_manager.xd.bank = v
                msg = "bank:%i | slot #?" % v
                context.area.header_text_set(text=msg)
                print(msg)
            else:
                xd = context.window_manager.xd
                cx = xd.cx
                if not cx and context.user_preferences.addons[__package__].preferences.auto:
                    from .xddb import init_on
                    init_on(context.user_preferences.addons[__package__].preferences.dbfile)
                    cx = xd.cx
                if not cx:
                    return {"CANCELLED"}
                asset_id = cx.execute("select asset_id from banks where bank=? and slot=?",(xd.bank,v)).fetchone()[0]
                if asset_id and asset_id > -1:
                    bpy.ops.xd.load_asset(asset_id=asset_id)
                    context.area.tag_redraw()
                else:
                    msg = "nothing loaded from bank %i slot %i."%(xd.bank,v)
                    context.area.header_text_set(text=msg)
                    print(msg)
            context.area.header_text_set(text="")
            return {"FINISHED"}
        return {"RUNNING_MODAL"}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        msg = "Bank #%i Slot #?" % context.window_manager.xd.bank
        context.area.header_text_set(text=msg)
        print(msg)
        return {'RUNNING_MODAL'}
