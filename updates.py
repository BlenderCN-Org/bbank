from . import statement as stmt

none = lambda *_:None

def load_libraries(self,context):
    self.clear()
    L = str(stmt.library(self.show.libraries))
    print(L)
    if self.order.paths != "RAW":
        P = str(stmt.path(self.show.paths,self.order.paths,getattr(self.order.reverse.paths,self.order.paths)))
    else:
        P = str(stmt.path(self.show.paths))
    print(P)

    list(map(self.view.libraries.load,self.cx.execute(L))) if self.cx.library_count else None
    list(map(self.view.paths.load,self.cx.execute(P))) if self.cx.path_count else None

def load_paths(self,context):
    self.clear()
    if self.order.paths != "RAW":
        P = str(stmt.path(self.show.paths,self.order.paths,getattr(self.order.reverse.paths,self.order.paths)))
    else:
        P = str(stmt.path(self.show.paths))
    print(P)
    if self.order.blends != "RAW":
        B = str(stmt.blend(self.show.blends,self.order.blends,getattr(self.order.reverse.blends,self.order.blends)))
    else:
        B = str(stmt.blend(self.show.blends))
    print(B)
    list(map(self.view.paths.load,self.cx.execute(P))) if self.cx.path_count else None
    list(map(self.view.blends.load,self.cx.execute(B))) if self.cx.blend_count else None

def load_blends(self,context):
    self.clear()
    if self.order.blends != "RAW":
        B = str(stmt.blend(self.show.blends,self.order.blends,getattr(self.order.reverse.blends,self.order.blends)))
    else:
        B = str(stmt.blend(self.show.blends))
    print(B)
    if self.order.assets != "RAW":
        A = str(stmt.asset(self.show.assets,self.order.assets,getattr(self.order.reverse.assets,self.order.assets)))
    else:
        A = str(stmt.asset(self.show.assets))
    print(A)
    list(map(self.view.blends.load,self.cx.execute(B))) if self.cx.blend_count else None
    list(map(self.view.assets.load,self.cx.execute(A))) if self.cx.asset_count else None

def load_assets(self,context):
    self.clear()
    if self.order.assets != "RAW":
        A = str(stmt.asset(self.show.assets,self.order.assets,getattr(self.order.reverse.assets,self.order.assets)))
    else:
        A = str(stmt.asset(self.show.assets))
    print(A)
    list(map(self.view.assets.load,self.cx.execute(A))) if self.cx.asset_count else None

def load_categories(self,context):
    self.clear()
    list(map(self.view.assets.load_alt,self.cx.execute("select id,name from assets where category=? and exclude=0",(self.show.category,)))) if self.cx.category_count(self.show.category) else None

def load_notes(self,context):
    self.clear()
    print(self)
    list(map(self.view.notes.load,self.cx.execute("select notes.id,blends.display_name,assets.category,assets.name,notes.note from blends join assets on blends.id=assets.blend_id join notes on notes.asset_id=assets.id")))


#based on what the view_mode is, call a loading function
def view_mode(self,context):
    {
            "LIBRARY":load_libraries,
            "PATH":load_paths,
            "BLEND":load_blends,
            "ASSET":load_assets,
            "CATEGORY":load_categories,
            "BANK":none,
            "NOTE":load_notes,
            "INFO":none }[self.view_mode](self,context)


def ord_chk_p(order,context):
    if order.paths == "RAW":
        order.reverse.paths.mtime = False
        order.reverse.paths.alpha = False
    elif order.paths == order.last.path:
        setattr(order.reverse.paths,order.paths,getattr(order.reverse.paths,order.paths) ^ 1)
    order.last.path = order.paths
    context.window_manager.xd.view_mode = context.window_manager.xd.view_mode

def ord_chk_b(order,context):
    if order.blends == "RAW":
        order.reverse.blends.mtime = False
        order.reverse.blends.size = False
        order.reverse.blends.alpha = False
    elif order.blends == order.last.blend:
        setattr(order.reverse.blends,order.blends,getattr(order.reverse.blends,order.blends) ^ 1)
    order.last.blend = order.blends
    context.window_manager.xd.view_mode = context.window_manager.xd.view_mode

def ord_chk_a(order,context):
    if order.assets == "RAW":
        order.reverse.assets.alpha = False
        order.reverse.assets.category = False
    elif order.assets == order.last.asset:
        setattr(order.reverse.assets,order.assets,getattr(order.reverse.assets,order.assets) ^ 1)
    order.last.asset = order.assets
    context.window_manager.xd.view_mode = context.window_manager.xd.view_mode

# explicitly labeling the act of setting state as a refresh
def vm_refresh(self,context):
    context.window_manager.xd.view_mode = context.window_manager.xd.view_mode


#________________________________________________________________________________.
def note(self,context):
    cx = context.window_manager.xd.cx
    cx.execute("update notes set note=? where id=?",(self.note,self.rowid))
    cx.commit()

def asset_inspector(self,context):
    xd = context.window_manager.xd
    xd.clearnotes()
    if self.index > -1:
        asset = self.data[self.index]
        if xd.cx.asset_note_count(asset.rowid):
            print(len(xd.noteviews))
            noteview = xd.noteview
            list(map(noteview.load,xd.cx.execute("select id,note from notes where asset_id=?",(asset.rowid,))))

def blend_index(self,context):
    print(self)
    print(vars(self))
