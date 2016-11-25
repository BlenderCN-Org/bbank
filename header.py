#need to move this elsewhere
def draw(self,context):
    xd = context.window_manager.xd
    row = self.layout.row()
    row.separator()
    row.prop(xd,"activate",toggle=True,icon="GO_LEFT",text="")
    row = self.layout.row(align=True)
    row.separator()
    row.prop(xd,"view_mode",expand=True)
    row.prop(xd.show,"category") if xd.view_mode == "CATEGORY" else None
