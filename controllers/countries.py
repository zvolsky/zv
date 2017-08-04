# -*- coding: utf-8 -*-

import os

@auth.requires_membership('admin')
def import_countries():
    # http://www.countries-list.info : code2:country -> input/countries_eng.txt (english)
    # http://www.countries-list.info : code2:country -> input/countries_cze.txt (czech, ..)
    # translations into table country_lang, then /import_lang/eng, /import_lang/cze, ...
    lang = request.args(0)
    if not lang:
        return "3-chars language string required"
    master = lang == 'eng'
    fn = os.path.join(os.getcwd(), 'applications', 'zv', 'input', 'countries_%s.txt' % lang)
    with open(fn) as f:
        countries = f.readlines()
    old = db(db.country, db.country_lang).select(db.country.id, db.country.code2, db.country.country,
                      db.country_lang.country, db.country_lang.id,
                      left=db.country_lang.on((db.country_lang.country_id == db.country.id)
                                               & (db.country_lang.lang == lang)))
    if not master and not old:
        return "import eng language first"
    old = {old1.country.code2: [old1.country.id, old1.country.country, old1.country_lang.country, old1.country_lang.id, None]
           for old1 in old}
    for country in countries:
        if country and country[2:3] == ':':
            code2 = country[:2]
            name = country[3:].strip()
            if code2 and name:
                if code2 in old:
                    old[code2][4] = name
                elif master:
                    old[code2] = [None, None, None, None, name]
    for code2 in old:
        v = old[code2]
        country = v[4] or v[2] or v[1]   # from import --or-- in target language --or-- english
        if v[0]:
            country_id = v[0]
            if master and v[1] != country:
                db.country[country_id] = {'country': country}
        else:
            country_id = db.country.insert(code2=code2, country=country)
        if not v[2]:
            db.country_lang.insert(country_id=country_id, lang=lang, country=country)
        elif v[2] != country:
            db.country_lang[v[3]] = {'country': country}
    return 'ok'
