#display routines used by the interface
from .cats import cats,asset_icons

def category_sidebar(layout,context):
    xd = context.window_manager.xd
    col = layout.column(align=True)
    for cat in cats:
        col.prop_enum(xd.show,"category",cat)

def category(layout,context):
    assets = context.window_manager.xd
    row = layout.row()
    row.template_list("xd_catx","",assets,"data",assets,"index",type="GRID")

def categories(layout,context):
    xd = context.window_manager.xd
    cats = xd.cx.asset_categories
    for cat in cats:
        layout.prop(xd.show.categories,cat,icon=asset_icons[cat])

def ls_libraries(layout,context):
    xd = context.window_manager.xd
    for item in xd.view.libraries.data:
        layout.label(item.name)

def libraries(layout,context):
    xd = context.window_manager.xd
    libs = xd.view.libraries
    row = layout.row()
    row.label("Libraries",icon="BOOKMARKS")
    row.prop(xd.show,"libraries",expand=True)
    box = layout.box()
    box.template_list("xd_libraries","",libs,"data",libs,"index")

def ls_paths(layout,context):
    xd = context.window_manager.xd
    for item in xd.view.paths.data:
        layout.label(item.name)

def paths(layout,context):
    xd = context.window_manager.xd
    row = layout.row()
    row.label("Paths",icon="FILE_FOLDER")
    row.prop(xd.show,"paths",expand=True)
    row.prop(xd.order,"paths",expand=True)
    box = layout.box()
    box.template_list("xd_paths","",xd.view.paths,"data",xd.view.paths,"index")

def ls_blends(layout,context):
    xd = context.window_manager.xd
    for item in xd.view.blends.data:
        layout.label(item.name)

def blends(layout,context):
    xd = context.window_manager.xd
    cx = xd.cx
    row = layout.row()
    row.label("Blends",icon="FILE_BLEND")
    row.prop(xd.show,"blends",expand=True)
    row.prop(xd.order,"blends",expand=True)
    box = layout.box()
    box.template_list("xd_blends","",xd.view.blends,"data",xd.view.blends,"index")
    box = layout.box()
    box.operator("xd.scan_included_blends")
    box.label("%i of %i blends. ( %i excluded. )" % (cx.included_blend_count,cx.blend_count,cx.excluded_blend_count))

def ls_assets(layout,context):
    xd = context.window_manager.xd
    for item in xd.view.assets.data:
        layout.label(item.name)

def assets(layout,context):
    xd = context.window_manager.xd
    row = layout.row()
    row.label("Assets: %i total, %i included, %i excluded"%(xd.cx.asset_count,xd.cx.included_asset_count,xd.cx.excluded_asset_count),icon="LIBRARY_DATA_DIRECT")
    row.prop(xd.show,"assets",expand=True)
    row.prop(xd.order,"assets",expand=True)
    box = layout.box()
    box.template_list("xd_assets","",xd.view.assets,"data",xd.view.assets,"index")
    al = len(xd.view.assets.data)
    if al and xd.view.assets.index < al:
        asset = xd.view.assets.data[xd.view.assets.index]
        box = layout.box()
        box.label(asset.name)
        box.prop(xd,"putbank")
        box.prop(xd,"putslot")
        op = box.operator("xd.bankput")
        op.bank = xd.putbank
        op.slot = xd.putslot
        op.a_id = asset.rowid
        box = layout.box()
        box.operator("xd.annotate_asset",icon="TEXT",text="").index = asset.rowid
        if asset.note_count:
            notes = xd.noteview
            box.template_list("xd_notes","",notes,"data",notes,"index")

def notes(layout,context):
    xd = context.window_manager.xd
    notes = xd.view.notes
    layout.label("Notes",icon="TEXT")
    layout.template_list("xd_notes","",notes,"data",notes,"index")

