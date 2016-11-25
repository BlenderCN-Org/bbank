# user preferences for the bdnav addon
# what folder the database
# what name the file
# whether auto connect at startup

# and draw the "activate interface" button

import bpy
import os

_suffix = ".xdb"

class xdAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    location = bpy.props.StringProperty(default=bpy.utils.user_resource("DATAFILES",path=__package__,create=True))
    filename = bpy.props.StringProperty(default="default")
    auto = bpy.props.BoolProperty()
    dbfile = property(fget=lambda s:os.path.join(s.location,s.filename+_suffix))
    def draw(self,context):
        xd = context.window_manager.xd
        layout = self.layout
        split = layout.split(percentage=0.25)
        col = split.column()
        box = col.box()
        box.prop(xd,"activate",text="Activate Interface",icon="PLUGIN")
        col = split.column()
        box = col.box()
        box.prop(self,"auto")
        box.separator()
        box.prop(self,"location",icon="FILE_FOLDER")
        box.prop(self,"filename",icon="DISK_DRIVE")
        exists = os.path.isfile(self.dbfile)
        box.label(self.dbfile,icon=["QUESTION","FILE_TICK"][exists])
        box.operator("xd.database_delete",icon="X") if exists else None
