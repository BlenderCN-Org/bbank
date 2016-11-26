# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
"name":"BlendData Navigator",
"author":"dustractor",
"location":"User Preferences > here > activate interface",
"category":"Asset Manager"
}


import bpy

from . import pref,sess,ui,ops

def register():
    bpy.utils.register_module(__package__)
    bpy.types.WindowManager.xd = bpy.props.PointerProperty(type=sess.xdSession)

    bpy.types.VIEW3D_HT_header.prepend(
            ui.button.for_splitting_the_viewport_with_an_img_editor)
    bpy.types.TIME_HT_header.prepend(
            ui.button.for_changing_the_timeline_into_userprefs)
    kc = bpy.context.window_manager.keyconfigs.active
    km = kc.keymaps['3D View'].keymap_items.new
    km('xd.bank',type='NUMPAD_ASTERIX',value='PRESS')

def unregister():
    del bpy.types.WindowManager.xd
    bpy.utils.unregister_module(__package__)

