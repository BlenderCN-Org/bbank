PRAGMA FOREIGN_KEYS=ON;
PRAGMA RECURSIVE_TRIGGERS=ON;

create table if not exists libraries(
        id integer primary key,
        name text,
        path_count integer default 0,
        blend_count integer default 0,
        exclude integer default 0,
        tag integer default 0,
    unique(name) on conflict ignore);

create table if not exists paths(
        id integer primary key,
        library_id integer,
        name text,
        display_name text,
        mt timestamp,
        mtime text,
        blend_count integer default 0,
        exclude integer default 0,
        tag integer default 0,

    foreign key (library_id) references libraries(id) on delete cascade,
    unique(name) on conflict ignore);

create table if not exists blends(
        id integer primary key,
        path_id integer,
        name text,
        display_name text,
        sz integer,
        filesize integer,
        mt timestamp,
        mtime text,
        asset_count integer default 0,
        exclude integer default 0,
        tag integer default 0,

    foreign key(path_id) references paths(id) on delete cascade,
    unique(name) on conflict ignore);

create table if not exists assets(
        id integer primary key,
        blend_id integer,
        name text,
        category text,
        note_count integer default 0,
        exclude integer default 0,
        tag integer default 0,

    foreign key (blend_id) references blends(id) on delete cascade,
    unique(name,category,blend_id) on conflict ignore);

create table if not exists banks (bank integer,slot integer,asset_id integer default -1,unique(slot,bank) on conflict replace);

create table if not exists notes (id integer primary key,asset_id integer,note text,foreign key (asset_id) references assets(id) on delete cascade);

