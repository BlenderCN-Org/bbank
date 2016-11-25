#only three loader-functions so far... objects, images, materials
#these get called after loading an asset of said type.

def objects(asset,context):
    context.scene.objects.link(asset)
    area = {a.type:a for a in context.screen.areas}.get("VIEW_3D",None)
    if area:
        asset.location = area.spaces[0].cursor_location

def images(asset,context):
    area = {a.type:a for a in context.screen.areas}.get("IMAGE_EDITOR",None)
    if area:
        area.spaces[0].image = asset

def materials(asset,context):
    for ob in context.selected_objects:
        if hasattr(ob.data,"materials"):
            ob.data.materials[0] = asset

# addon preferences could/should allow for choice from more possibilities.

# hoping others provide some brainstorms on this, what to do for each type of asset
