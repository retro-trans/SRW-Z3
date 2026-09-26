"""Display-only exact default names for native $n/$f/$l/$F fields.

No writes to player/save buffers. Custom and partly customized full names
pass through unchanged. Each destination field holds 41 bytes including NUL.
"""
from category_port import encoded,require


def rows(port):
    first=port.text(port.catalog.text('ui.runtime_names:r_fd402c2be1949899'))
    nick=port.text(port.catalog.text('ui.runtime_names:r_5160e365ddd750eb'))
    last=port.text(port.catalog.text('ui.runtime_names:r_8d15b248973dfcec'))
    require(first==nick,'Native default first/nickname identities need distinct adapters')
    text={'ヒビキ':first,'カミシロ':last,
          'カミシロヒビキ':last+' '+nick,'ヒビキ・カミシロ':nick+' '+last}
    result={jp.encode('cp932'):encoded(en,port.mapping) for jp,en in text.items()}
    require(all(len(value)<41 for value in result.values()),'Runtime name exceeds 41-byte field')
    return result
