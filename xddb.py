import bpy
import sqlite3
import os
import datetime
from math import log

blendfile = __import__("re").compile(r"^.*\.blend$").match

cx = None

def sz_label(b):
    x = int(log(b,1024))
    q = b/pow(1024,x)
    return "%.2f%s"%(q,"bkMGTP"[x])

class connector:
    @property
    def cx(x):
        return cx


class dcx(sqlite3.Connection):

    def __init__(self,dbname,**kwds):
        sqlite3.Connection.__init__(self,dbname,**kwds)
        ddl = open(os.path.join(os.path.dirname(__file__),"xdddl.sql")).read()
        triggers = open(os.path.join(os.path.dirname(__file__),"triggers.sql")).read()
        #views = open(os.path.join(os.path.dirname(__file__),"views.sql")).read()
        if not self.execute("select count(*) from sqlite_master").fetchone()[0]:
            self.executescript(ddl)
            self.executescript(triggers)
            #self.executescript(views)
            for i in range(10):
                for j in range(10):
                    self.execute("insert into banks (bank,slot) values (?,?)",(i,j))
            self.commit()

    def add_library(self,library,recurse):
        library_id = self.execute("insert into libraries (name) values (?)",(library,)).lastrowid
        paths = (r for r,ds,fs in os.walk(library) if any(filter(blendfile,fs))) if recurse else (library,)
        for path in paths:
            displayname = os.path.basename(path) if not path.endswith(os.sep) else os.path.basename(path[:-1])
            stat = os.stat(path)
            mt = datetime.datetime.fromtimestamp(stat.st_mtime)
            path_id = self.execute("insert into paths (name,display_name,mt,mtime,library_id) values (?,?,?,?,?)",(path,displayname,mt,str(mt),library_id)).lastrowid
            for blend_filename in filter(blendfile,os.listdir(path)):
                displayname = blend_filename[:-6]
                blend = os.path.join(path,blend_filename)
                stat = os.stat(blend)
                sz = stat.st_size
                mt = datetime.datetime.fromtimestamp(stat.st_mtime)
                self.execute("insert into blends (name,display_name,sz,filesize,mt,mtime,path_id) values (?,?,?,?,?,?,?)",(blend,displayname,sz,sz_label(sz),mt,str(mt),path_id))
            path_blendcount = self.execute("select count(*) from blends where path_id=?",(path_id,)).fetchone()[0]
            self.execute("update paths set blend_count=? where id=?",(path_blendcount,path_id))
        library_pathcount = self.execute("select count(*) from paths where library_id=?",(library_id,)).fetchone()[0]
        library_blendcount = self.execute("select sum(blend_count) from paths where library_id=?",(library_id,)).fetchone()[0]
        self.execute("update libraries set path_count=?,blend_count=? where id=?",(library_pathcount,library_blendcount,library_id))
        self.commit()

    def remove_library(self,library_id):
        self.execute("delete from libraries where id=?",(library_id,))
        self.commit()

    def scan_blend_for_assets(self,blend_id):
        blend = self.execute("select name from blends where id=?",(blend_id,)).fetchone()[0]
        with bpy.data.libraries.load(blend) as (categories,_):
            for category in dir(categories):
                for name in getattr(categories,category):
                    self.execute("insert into assets (name,category,blend_id) values (?,?,?)",(name,category,blend_id))
        blend_assetcount = self.execute("select count(*) from assets where blend_id=?",(blend_id,)).fetchone()[0]
        self.execute("update blends set asset_count=? where id=?",(blend_assetcount,blend_id))
        self.commit()

    def prune_blendassets(self,blend_id):
        self.execute("delete from assets where blend_id=?",(blend_id,))
        self.execute("update blends set asset_count=0 where id=?",(blend_id,))
        self.commit()

    def library_exclusion(self,library_id):
        return self.execute("select exclude from libraries where id=?",(library_id,)).fetchone()[0]

    def path_exclusion(self,path_id):
        return self.execute("select exclude from paths where id=?",(path_id,)).fetchone()[0]

    def blend_exclusion(self,blend_id):
        return self.execute("select exclude from blends where id=?",(blend_id,)).fetchone()[0]

    def asset_exclusion(self,asset_id):
        return self.execute("select exclude from assets where id=?",(asset_id,)).fetchone()[0]

    def asset_note_count(self,asset_id):
        return self.execute("select count(*) from notes where asset_id=?",(asset_id,)).fetchone()[0]

    def asset_notes(self,asset_id):
        return self.execute("select note from notes where asset_id=?",(asset_id,)).fetchall()

    def asset_info(self,asset_id):
        return self.execute("select blends.name,assets.name,assets.category from assets join blends on assets.blend_id=blends.id where assets.id=?",(asset_id,)).fetchone()

    def category_count(self,category):
        return self.execute("select count(*) from assets where exclude=0 and category=?",(category,)).fetchone()[0]

    @property
    def included_blends(self):
        return [_[0] for _ in self.execute("select id from blends where exclude=0")]

    @property
    def included_library_count(self):
        return self.execute("select count(*) from libraries where exclude=0").fetchone()[0]

    @property
    def included_path_count(self):
        return self.execute("select count(*) from paths where exclude=0").fetchone()[0]

    @property
    def included_blend_count(self):
        return self.execute("select count(*) from blends where exclude=0").fetchone()[0]

    @property
    def included_asset_count(self):
        return self.execute("select count(*) from assets where exclude=0").fetchone()[0]

    @property
    def excluded_library_count(self):
        return self.execute("select count(*) from libraries where exclude=1").fetchone()[0]

    @property
    def excluded_path_count(self):
        return self.execute("select count(*) from paths where exclude=1").fetchone()[0]

    @property
    def excluded_blend_count(self):
        return self.execute("select count(*) from blends where exclude=1").fetchone()[0]

    @property
    def excluded_asset_count(self):
        return self.execute("select count(*) from assets where exclude=1").fetchone()[0]

    @property
    def library_count(self):
        return self.execute("select count(*) from libraries").fetchone()[0]

    @property
    def path_count(self):
        return self.execute("select count(*) from paths").fetchone()[0]

    @property
    def blend_count(self):
        return self.execute("select count(*) from blends").fetchone()[0]

    @property
    def asset_count(self):
        return self.execute("select count(*) from assets").fetchone()[0]

    @property
    def asset_categories(self):
        yield from (_[0] for _ in self.execute("select distinct category from assets"))


def init_on(dbf):
    global cx
    cx = sqlite3.connect(dbf,factory=dcx,detect_types=sqlite3.PARSE_DECLTYPES)
    print("init on")
