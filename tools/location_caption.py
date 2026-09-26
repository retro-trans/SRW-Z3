"""Build EFFPS3 title assets and the complete map-location caption family."""
from pathlib import Path
from cpk import CPK
import cpkpatch

NAME = 'EFFPS3.CPK'
SOURCE = Path('work/orig') / NAME
MEMBER = 96

def apply(blob, font_path):
    import map_locations
    return map_locations.apply(blob,font_path,MEMBER)

def verify(original, built, font_path):
    import map_locations
    map_locations.verify(original,built,font_path,MEMBER)

def build(out, font_path, title_version=None):
    if not SOURCE.exists():
        import shutil
        source = Path('E:/SRWZ3/PS3_GAME/USRDIR/DATA/ANIME') / NAME
        k = CPK(str(source))
        apply(k.read(next(f for f in k.files if f['id']==MEMBER)),font_path)
        SOURCE.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,SOURCE)
    k = CPK(str(SOURCE))
    import map_locations
    replacements={}
    for ident in map_locations.ROWS:
        original=k.read(next(f for f in k.files if f['id']==ident))
        built=map_locations.apply(original,font_path,ident)
        map_locations.verify(original,built,font_path,ident)
        temp=Path(out)/('map_caption_%d.member'%ident)
        temp.write_bytes(built);replacements[ident]=str(temp)
    import scenario_title
    title_originals = {i:k.read(next(f for f in k.files if f['id']==i))
                       for i in scenario_title.EFFECTS}
    import title_footer
    footer_original = k.read(next(f for f in k.files if f['id']==title_footer.MEMBER))
    import berserk_banner
    berserk_original = k.read(next(f for f in k.files if f['id']==berserk_banner.MEMBER))
    del k
    berserk_built = berserk_banner.apply(berserk_original,font_path)
    berserk_banner.verify(berserk_original,berserk_built,font_path)
    berserk_temp = Path(out)/'berserk_banner.member'
    berserk_temp.write_bytes(berserk_built)
    replacements[berserk_banner.MEMBER] = str(berserk_temp)
    for ident,title_original in title_originals.items():
        title_built = scenario_title.effect_apply(title_original,font_path,ident)
        scenario_title.verify_effect(title_original,title_built,font_path,ident)
        title_temp = Path(out)/f'scenario_title_{ident}.member'
        title_temp.write_bytes(title_built)
        replacements[ident]=str(title_temp)
    if footer_original is not None:
        import title_library_buttons
        footer_built = title_library_buttons.apply(footer_original, font_path, title_version)
        title_library_buttons.verify(footer_original, footer_built, font_path, title_version)
        import title_logo
        logo_base=footer_built
        footer_built=title_logo.apply(logo_base)
        title_logo.verify(logo_base,footer_built)
        footer_temp = Path(out)/'title_footer.member'
        footer_temp.write_bytes(footer_built)
        replacements[title_footer.MEMBER] = str(footer_temp)
        title_footer.background(footer_built).save(Path(out)/'title_footer_background.png')
        title_library_buttons.atlas(footer_built).save(Path(out)/'title_library_atlas.png')
        title_logo.atlas(footer_built).save(Path(out)/'title_logo_atlas.png')
    cpkpatch.build(str(SOURCE),str(Path(out)/NAME),replacements)
    for path in replacements.values():Path(path).unlink()
    print('[map] All 83 Japan/world/space captions translated; only caption pixels changed.')
