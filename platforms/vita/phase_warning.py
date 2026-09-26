"""Whole draw-time keys for the native unacted-team count confirmation."""
from category_port import require,digest,encoded
from inspect_vwf import segment

MESSAGE='issue_hook:r_065443f6ddfcf0d7'
PREFIX='行動終了していないチームが'
SUFFIX='チームあります。'
DIGITS='０１２３４５６７８９'
START=0x8100A060
END=0x8100A16C
SOURCE_SHA='12070497405e2cc56f42c9793acf7d92fd16cefa33d3c9400ae75ee467ce368c'


def hooks(port,executable,info):
    import ui_text
    text,base=segment(executable,info,0)
    require(digest(text[START-base:END-base])==SOURCE_SHA,
            'Native remaining-team formatter changed')
    for address,value in ((0x812578A4,DIGITS),(0x812578BC,PREFIX),
                          (0x812578D8,SUFFIX),(0x812578EC,'フェイズを終了しますか？')):
        raw=value.encode('cp932')+b'\0'
        require(text[address-base:address-base+len(raw)]==raw,
                'Native remaining-team source changed')
    definition=port.catalog.document('localization/messages/issue_hook.json')['messages'][MESSAGE]
    require(definition['source']==PREFIX+'{count}'+SUFFIX,'Team warning template changed')
    template=port.catalog.text(MESSAGE);rows={}
    # The source routine formats positive counts modulo 100 with one or two
    # full-width digits. Zero/negative counts take the existing plain prompt.
    # Include zero because a positive multiple of 100 displays ０.
    for count in range(100):
        digits=str(count).translate(str.maketrans('0123456789',DIGITS))
        jp=PREFIX+digits+SUFFIX
        en=port.text(template.format(count=count))
        require('\n' not in en and '{' not in en and '}' not in en,'Invalid team warning line')
        require(sum(port.widths[c] for c in en)<=1000,'Team warning exceeds dialog width')
        payload=encoded(en,port.mapping)
        # CP932 is the native constructor path. Also retain UTF-8's original
        # centering key and converted drawer key for the shared UI entry point.
        for key in (jp.encode('cp932'),jp.encode('utf-8'),ui_text.converted_key(jp,executable,info)):
            require(key not in rows or rows[key]==payload,'Conflicting team count')
            rows[key]=payload
    return rows
