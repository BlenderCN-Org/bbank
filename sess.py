#properties of a session

import bpy

from . import xddb
from . import header
from . import updates

from .cats import cats,asset_icons

# must maintain references to the types while they are inactive
hidden_while_active = list(
        (panel for panel in bpy.types.Panel.__subclasses__() if
            (hasattr(panel,"bl_space_type") and
                getattr(panel,"bl_space_type") == "USER_PREFERENCES")))

# keep the draw function of the header also, so can set it back
original_header_draw = bpy.types.USERPREF_HT_header.draw


# toggle the ui
# we unregister the types of the things we wish to clear out of the way
# going to use "all" of the user preferences view as a "scripts window"
#
# the function is called as a property update function of the window-
# manager's `xd` propertygroup
#
# if xd's `activate` boolean property is true,
# check to see what xd's `cx` property returns
# something ( a database connection ) or nothing ( None )
# if nothing, then use the value of the user-preferences `dbfile` property
# as the name of the database to connect to.
'''
    This ^ 
         |  when switching to use blender's presets system
    will change to more resemble what is demo-ed in WATDO
'''
# we set xd's `view_mode` property, in order to trigger
# an update which loads the data
#
def ui_toggle(self,context):
    list(
            map(
                [bpy.utils.register_class,
                    bpy.utils.unregister_class][self.activate],
                hidden_while_active))
    bpy.types.USERPREF_HT_header.draw = [
            original_header_draw,header.draw][self.activate]
    if self.activate:
        if not self.cx:
            xddb.init_on(context.user_preferences.addons[__package__].preferences.dbfile)
        self.view_mode = self.view_mode
        if context.area.type == "USER_PREFERENCES":
            bpy.ops.screen.header_flip()
    else:
        from .button import for_changing_userprefs_back_to_a_timeline as switchback
        bpy.types.USERPREF_HT_header.prepend(switchback)
        if context.area.type == "USER_PREFERENCES":
            bpy.ops.screen.header_flip()


class xdSessionLibrary(bpy.types.PropertyGroup):
    rowid = bpy.props.IntProperty()
    name = bpy.props.StringProperty()
    path_count = bpy.props.IntProperty()
    blend_count = bpy.props.IntProperty()

class xdLibraryViewingSession(bpy.types.PropertyGroup):
    def load(self,row):
        n = self.data.add()
        n.rowid,n.name,n.path_count,n.blend_count = row
    data = bpy.props.CollectionProperty(type=xdSessionLibrary)
    index = bpy.props.IntProperty(min=-1,default=-1)

class xdSessionPath(bpy.types.PropertyGroup):
    rowid = bpy.props.IntProperty()
    name = bpy.props.StringProperty()
    mtime = bpy.props.StringProperty()
    blend_count = bpy.props.IntProperty()

class xdPathViewingSession(bpy.types.PropertyGroup):
    def load(self,row):
        n = self.data.add()
        n.rowid,n.name,n.mtime,n.blend_count = row
    data = bpy.props.CollectionProperty(type=xdSessionPath)
    index = bpy.props.IntProperty(min=-1,default=-1)

class xdSessionBlend(bpy.types.PropertyGroup):
    rowid = bpy.props.IntProperty()
    name = bpy.props.StringProperty()
    size = bpy.props.StringProperty()
    mtime = bpy.props.StringProperty()
    asset_count = bpy.props.IntProperty()

class xdBlendViewingSession(bpy.types.PropertyGroup):
    def load(self,row):
        n = self.data.add()
        n.rowid,n.name,n.size,n.mtime,n.asset_count = row
    data = bpy.props.CollectionProperty(type=xdSessionBlend)
    index = bpy.props.IntProperty(min=-1,default=-1,update=updates.blend_index)

class xdSessionAsset(bpy.types.PropertyGroup):
    rowid = bpy.props.IntProperty()
    name = bpy.props.StringProperty()
    category = bpy.props.StringProperty()
    note_count = bpy.props.IntProperty()


class xdAssetViewingSession(bpy.types.PropertyGroup):
    def load(self,row):
        n = self.data.add()
        n.rowid,n.name,n.category,n.note_count = row
    def load_alt(self,row):
        n = self.data.add()
        n.rowid,n.name = row
    data = bpy.props.CollectionProperty(type=xdSessionAsset)
    index = bpy.props.IntProperty(min=-1,default=-1,update=updates.asset_inspector)

class xdSessionNote(bpy.types.PropertyGroup):
    rowid = bpy.props.IntProperty()
    blend = bpy.props.StringProperty()
    asset = bpy.props.StringProperty()
    category = bpy.props.StringProperty()
    note = bpy.props.StringProperty(update=updates.note)

class xdAssetNoteViewingSession(bpy.types.PropertyGroup):
    def load(self,row):
        n = self.data.add()
        n.rowid,n.blend,n.asset,n.category,n.note = row
    data = bpy.props.CollectionProperty(type=xdSessionNote)
    index = bpy.props.IntProperty(min=-1,default=-1)


class xdSessionView(bpy.types.PropertyGroup):
    libraries = bpy.props.PointerProperty(type=xdLibraryViewingSession)
    paths = bpy.props.PointerProperty(type=xdPathViewingSession)
    blends = bpy.props.PointerProperty(type=xdBlendViewingSession)
    assets = bpy.props.PointerProperty(type=xdAssetViewingSession)
    notes = bpy.props.PointerProperty(type=xdAssetNoteViewingSession)

    
class xdViewCategoryFilters(bpy.types.PropertyGroup):
    # return a set of which categories are selected because i didn't know enum_flag back then
    def selection_list(self,context):
        return set(
                filter(
                    lambda _:getattr(self,_),
                    context.window_manager.xd.cx.asset_categories
                    )
                )
    actions = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    armatures = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    brushes = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    cameras = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    curves = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    fonts = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    grease_pencil = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    groups = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    images = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    ipos = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    lamps = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    lattices = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    linestyles = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    masks = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    materials = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    meshes = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    metaballs = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    movieclips = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    node_groups = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    objects = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    scenes = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    sounds = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    speakers = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    texts = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    textures = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)
    worlds = bpy.props.BoolProperty(default=True,update=updates.vm_refresh)

# this section: make the enum items have icons
xdv_cat_enum = [(c,c,c,asset_icons[c],i+1) for i,c in enumerate(cats)]
lpba_excl_filt_enum = (("EXCLUDED","","Excluded","VISIBLE_IPO_OFF",1),("ALL","","All","DISK_DRIVE",2),("INCLUDED","","Included","VISIBLE_IPO_ON",3))
xd_layout_enum = (("LIST","","","LONGDISPLAY",1),("SPLIT","","","SHORTDISPLAY",2),("TILE","","","IMGDISPLAY",3))
xdvm_enum = (("LIBRARY","","","BOOKMARKS",1),("PATH","","","FILE_FOLDER",2),("BLEND","","","FILE_BLEND",3),("ASSET","","","EXTERNAL_DATA",4),("CATEGORY","","","OOPS",5),("BANK","","","HAND",6),("NOTE","","","TEXT",7),("INFO","","","QUESTION",8))
xdlp_order_enum = (("RAW","","paths","LAYER_USED",1),("alpha","","paths by name","SORTALPHA",2),("mtime","","paths by mtime","SORTTIME",3))
xdlb_order_enum = (("RAW","","blends","LAYER_USED",1),("alpha","","blends by name","SORTALPHA",2),("mtime","","blends by mtime","SORTTIME",3),("size","","blends by size","SORTSIZE",4),)
xdla_order_enum = (("RAW","","assets","LAYER_USED",1),("alpha","","assets by name","SORTALPHA",2),("category","","assets by type","SORTBYEXT",3))


class xdViewFilters(bpy.types.PropertyGroup):
    category = bpy.props.EnumProperty(items=xdv_cat_enum,default="objects",update=updates.vm_refresh)
    categories = bpy.props.PointerProperty(type=xdViewCategoryFilters)
    libraries = bpy.props.EnumProperty(items=lpba_excl_filt_enum,default="ALL",update=updates.vm_refresh)
    paths = bpy.props.EnumProperty(items=lpba_excl_filt_enum,default="ALL",update=updates.vm_refresh)
    blends = bpy.props.EnumProperty(items=lpba_excl_filt_enum,default="ALL",update=updates.vm_refresh)
    assets = bpy.props.EnumProperty(items=lpba_excl_filt_enum,default="ALL",update=updates.vm_refresh)


class xdLayout(bpy.types.PropertyGroup):
    libraries = bpy.props.EnumProperty(items=xd_layout_enum,default="SPLIT")
    paths = bpy.props.EnumProperty(items=xd_layout_enum,default="SPLIT")
    blends = bpy.props.EnumProperty(items=xd_layout_enum,default="SPLIT")
    assets = bpy.props.EnumProperty(items=xd_layout_enum,default="SPLIT")

class xdPathSorts(bpy.types.PropertyGroup):
    alpha = bpy.props.BoolProperty()
    mtime = bpy.props.BoolProperty()

class xdBlendSorts(bpy.types.PropertyGroup):
    alpha = bpy.props.BoolProperty()
    mtime = bpy.props.BoolProperty()
    size = bpy.props.BoolProperty()

class xdAssetSorts(bpy.types.PropertyGroup):
    alpha = bpy.props.BoolProperty()
    category = bpy.props.BoolProperty()

class xdReverseSorts(bpy.types.PropertyGroup):
    paths = bpy.props.PointerProperty(type=xdPathSorts)
    blends = bpy.props.PointerProperty(type=xdBlendSorts)
    assets = bpy.props.PointerProperty(type=xdAssetSorts)

class xdLastSort(bpy.types.PropertyGroup):
    path = bpy.props.StringProperty()
    blend = bpy.props.StringProperty()
    asset = bpy.props.StringProperty()
    
class xdLoadOrdering(bpy.types.PropertyGroup):
    paths = bpy.props.EnumProperty(items=xdlp_order_enum,default="RAW",update=updates.ord_chk_p)
    blends = bpy.props.EnumProperty(items=xdlb_order_enum,default="RAW",update=updates.ord_chk_b)
    assets = bpy.props.EnumProperty(items=xdla_order_enum,default="RAW",update=updates.ord_chk_a)
    last = bpy.props.PointerProperty(type=xdLastSort)
    reverse = bpy.props.PointerProperty(type=xdReverseSorts)
    
class xdAssetNote(bpy.types.PropertyGroup):
    rowid = bpy.props.IntProperty()
    note = bpy.props.StringProperty(update=updates.note)

class xdAssetNotesView(bpy.types.PropertyGroup):
    def load(self,row):
        n = self.data.add()
        n.rowid,n.note = row
    data = bpy.props.CollectionProperty(type=xdAssetNote)
    index = bpy.props.IntProperty(min=-1,default=-1)

class xdSession(bpy.types.PropertyGroup,xddb.connector):
    bank = bpy.props.IntProperty()
    putbank = bpy.props.IntProperty()
    putslot = bpy.props.IntProperty()
    activate = bpy.props.BoolProperty(update=ui_toggle)
    view_mode = bpy.props.EnumProperty(items=xdvm_enum,default="LIBRARY",update=updates.view_mode)
    show = bpy.props.PointerProperty(type=xdViewFilters)
    layout = bpy.props.PointerProperty(type=xdLayout)
    views = bpy.props.CollectionProperty(type=xdSessionView)
    order = bpy.props.PointerProperty(type=xdLoadOrdering)
    noteviews = bpy.props.CollectionProperty(type=xdAssetNotesView)

    def clearnotes(self):
        for n in reversed(range(len(self.noteviews))):
            self.noteviews.remove(n)

    @property
    def noteview(self):
        return self.noteviews[0] if len(self.noteviews) else self.noteviews.add()

    @property
    def view(self):
        return self.views[0] if len(self.views) else self.views.add()

    def clear(self):
        self.views.remove(0) if len(self.views) else None

