"""Use rendered link width for MtV's selected-link background.

Original 0x1c8730..0x1c87b0 uses (byte_length//2)*style.pitch. Registration
0x1ce098 is called only by the link drawer, immediately after text drawing;
PEN_ACC therefore contains the width including draw-time name substitutions.
Cache one float for each of the manager's 16 banks x 16 slots. Do not change
its 20-byte records: length, identity, navigation and source text stay intact.
"""
import struct
import eboot

WIDTHS = eboot.BSS_PAGE + 0x1000  # 0x1000..0x13ff, after joined-text scratch
CAVE = 0x78ED00                 # after command data, before President helper
SITES = ((0x1ce18c,0x987c0004,CAVE),      # stb r3,4(r28)
         (0x1c871c,0x7c7d1b78,CAVE+0x80),# mr r29,r3
         (0x1c87b0,0xd01f0008,CAVE+0xc0))# stfs f0,8(r31)
FRAME_WIDTH = 0x88  # free aligned slot in the 0xb0 highlight frame


def stubs():
    P=eboot._ppc()
    a=eboot._Asm()
    a.emit(SITES[0][1])
    # The source allocator bounds both indices to 0..15 before this site.
    a.emit(P['lwz'](9,1,0x70));a.emit(P['mulli'](9,9,64))
    a.emit(P['lwz'](0,1,0x74));a.emit(P['mulli'](0,0,4))
    a.emit(P['add'](9,9,0))
    a.emit(P['lis'](0,WIDTHS>>16));a.emit(P['ori'](0,0,WIDTHS&65535))
    a.emit(P['add'](9,9,0))
    a.emit(P['lis'](0,eboot.PEN_ACC>>16));a.emit(P['ori'](0,0,eboot.PEN_ACC&65535))
    # r0 cannot be a D-form base register (RA=0 denotes zero); use r9 for
    # the accumulator load and r0 for the computed table address instead.
    # Swap the two addresses using volatile r10, which the next call may use.
    a.emit(P['mr'](10,9));a.emit(P['mr'](9,0))
    a.emit(P['lfs'](13,9,0));a.emit(P['stfs'](13,10,0))
    a.emit(0x4e800020)
    capture=a.code()
    a=eboot._Asm()
    a.emit(SITES[1][1])
    # r4 still holds the requested index from 0x1cdbb0. Invalid indices
    # return NULL and never draw; mask them to keep even that read bounded.
    a.emit(P['clrlwi'](9,4,24));a.emit(P['mulli'](9,9,4))
    a.emit(P['lis'](0,WIDTHS>>16));a.emit(P['ori'](0,0,WIDTHS&65535))
    a.emit(P['add'](9,9,0));a.emit(P['lfs'](0,9,0))
    a.emit(P['stfs'](0,1,FRAME_WIDTH));a.emit(0x4e800020)
    select=a.code()
    a=eboot._Asm()
    a.emit(P['lfs'](0,1,FRAME_WIDTH));a.emit(SITES[2][1]);a.emit(0x4e800020)
    draw=a.code()
    assert len(capture)<=0x80 and len(select)<=0x40 and len(draw)<=0x40
    return (capture,select,draw)


def guard_source(b,segs):
    # Boundaries/dataflow needed for using the cached actual drawer width.
    words={0x1ce140:0x81210070,0x1ce148:0x80010074,
           0x1ce178:0x993c0005,0x1ce17c:0xb35c0000,
           0x1ce180:0xb33c0002,
           0x1c870c:0x7fa407b4,0x1c8718:0x2f830000,
           0x1c8720:0x419eff78,0x1c8778:0x7c0041d6}
    for site,want in words.items():
        have=struct.unpack_from('>I',b,eboot._off(segs,site))[0]
        assert have==want,(hex(site),hex(have),hex(want))
    for site,target in ((0x1d1dd8,0x1d11fc),(0x1d1e10,0x1ce098),
                        (0x1ce184,0x554dac),(0x1c8710,0x1cdbb0)):
        want=0x48000001|((target-site)&0x3fffffc)
        assert struct.unpack_from('>I',b,eboot._off(segs,site))[0]==want,hex(site)


def apply(b,segs,dialogue_scene=False):
    import command_layout
    assert command_layout.DATA+8*len(command_layout.LABELS)<=CAVE
    assert WIDTHS+256*4<=eboot.HOOK_JSTATE
    assert SITES[-1][2]+len(stubs()[-1])<0x78F000
    guard_source(b,segs)
    edited=[]
    for (site,original,cave),raw in zip(SITES,stubs()):
        pos=eboot._off(segs,site);dst=eboot._off(segs,cave)
        assert struct.unpack_from('>I',b,pos)[0]==original,hex(site)
        assert not any(b[dst:dst+len(raw)]),hex(cave)
        struct.pack_into('>I',b,pos,0x48000001|((cave-site)&0x3fffffc))
        b[dst:dst+len(raw)]=raw
        edited.extend(((pos,pos+4),(dst,dst+len(raw))))
    import main_link_background_layout as main
    edited.extend(main.apply(b,segs))
    import link_identity_geometry as identity
    edited.extend(identity.apply(b,segs))
    if dialogue_scene:
        import dialogue_link_scene
        edited.extend(dialogue_link_scene.apply(b,segs))
    check(b)
    return edited


def check(b):
    segs=eboot._segments(b)
    guard_source(b,segs)
    for (site,_,cave),raw in zip(SITES,stubs()):
        pos=eboot._off(segs,site);dst=eboot._off(segs,cave)
        assert struct.unpack_from('>I',b,pos)[0]==0x48000001|((cave-site)&0x3fffffc)
        assert b[dst:dst+len(raw)]==raw
    assert segs[1]['va']+segs[1]['memsz']>=WIDTHS+1024
    import main_link_background_layout as main
    main.check(b)
    import link_identity_geometry as identity
    if b[eboot._off(segs,identity.DEAD):eboot._off(segs,identity.DEAD)+4] == identity.lookup()[:4]:
        identity.check(b)
    import dialogue_link_scene as scene
    scene_site=eboot._off(segs,scene.SITE)
    if b[scene_site:scene_site+4] == struct.pack('>I',scene.branch(scene.SITE,scene.CAVE,True)):
        scene.check(b)
    print('PASS: primary/secondary link geometry uses rendered positions and widths; metadata intact.')
