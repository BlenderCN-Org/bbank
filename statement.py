
sel = "select {cols} from {table}"

class select_statement:
    xcl = None
    rdr = None
    rev = False
    def __init__(self,exclusion,order=None,reverse=False):
        self.xcl = {"ALL":None,"INCLUDED":0,"EXCLUDED":1}[exclusion]
        self.rdr = {"alpha":"name","size":"sz"}.get(order,order)
        self.rev = reverse
    def __str__(self):
        cols = ",".join(self.cols)
        ret = sel.format(cols=cols,table=self.table)
        if self.xcl != None:
            ret += " where exclude=%i"%self.xcl
        if self.rdr != None:
            ret += " order by %s %s" % (self.rdr,["ASC","DESC"][self.rev])
        return ret


class library(select_statement):
    cols = "id","name","path_count","blend_count"
    table = "libraries"


class path(select_statement):
    cols = "id","display_name","mtime","blend_count"
    table = "paths"


class blend(select_statement):
    cols = "id","display_name","filesize","mtime","asset_count"
    table = "blends"


class asset(select_statement):
    cols = "id","name","category","note_count"
    table = "assets"


