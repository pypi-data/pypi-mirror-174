from paises.countries import Countries

ctrs = Countries()
ctrs.load_wb()

def get_alias(elements):
    aliases = []
    for c in elements:
        if ctrs.search(c):
            aliases += [x for i in ctrs.search(c) for x in i['alias']]
            aliases += [c]
        else:
            aliases.append(c)
        
    return aliases