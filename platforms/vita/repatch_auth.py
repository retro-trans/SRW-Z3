"""Offline rePatch auth validation/sanitization; never print or emit raw secrets."""
import hashlib
import struct


def require(ok, message):
    if not ok:
        raise ValueError(message)


def validate_auth(data, authid):
    require(len(data) == 0x90, 'self_auth.bin must be exactly 144 bytes')
    require(struct.unpack_from('<Q', data)[0] == authid,
            'self_auth.bin authority ID does not match this game executable')
    require(any(data[0x10:0x50]), 'self_auth.bin has empty capability data')
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                validation='length, matching authority ID, nonempty capabilities; '
                           'user must supply an original PCSG00264 v01.00 console dump')


def sanitize_auth(data, authid):
    """Only upstream rePatch 3.0's authority/capability/attribute fields survive.

    rePatch auth hook copies [0x10, 0x50), after comparing the authority ID.
    VitaSDK SceSelfAuthInfo stores shared secrets at 0x50, klicensee at 0x60.
    https://github.com/dots-tb/rePatch-reDux0/blob/master/repatch.c
    https://github.com/vitasdk/vita-headers/blob/master/include/psp2kern/types.h
    """
    validate_auth(data, authid)
    sanitized = data[:8] + bytes(8) + data[0x10:0x50] + bytes(0x40)
    row = validate_auth(sanitized, authid)
    row['sanitization'] = ('Preserved authority ID and capability/attribute bytes; '
                           'zeroed padding 0x08:0x10 and shared secrets 0x50:0x90')
    row['raw_auth_included'] = False
    return sanitized, row
