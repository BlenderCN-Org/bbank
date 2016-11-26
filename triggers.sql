create trigger if not exists library_exclusion_update after update of exclude on libraries
    begin
        update paths set exclude=NEW.exclude where library_id=NEW.id;
    end;

create trigger if not exists path_exclusion_update after update of exclude on paths
    begin
        update blends set exclude=NEW.exclude where path_id=NEW.id;
    end;

create trigger if not exists blend_exclusion_update after update of exclude on blends
    begin
        update assets set exclude=NEW.exclude where blend_id=NEW.id;
    end;

