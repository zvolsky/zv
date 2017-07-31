# -*- coding: utf-8 -*-

db.define_table('country',
    Field('country', 'string', length=50),
    Field('code2', 'string', length=2),
    Field('code3', 'string', length=3),
    Field('codenum', 'string', length=3),
    )

db.define_table('country_lang',
    Field('country_id', db.country),
    Field('lang', 'string', length=3),
    Field('country', 'string', length=50),
    )

auth.lang = session.lang or 'eng'
countries = db(db.country_lang.lang == auth.lang).select(db.country.id, db.country_lang.country,
                    join=db.country.on(db.country.id == db.country_lang.country_id),
                    orderby=db.country_lang.country)
countries = [(country.country.id, country.country_lang.country) for country in countries]
db.define_table('loc',
    Field('country_id', db.country, requires=IS_IN_SET(countries)),
    #Field('state', 'string', length=2),
    Field('name', 'string', length=50),
    Field('w24', 'string', length=40),
    Field('yr', 'string', length=50),
    )

'''
db.define_table('loc_als',
    Field('name', 'string', length=40),
    Field('lang', 'string', length=3),
    )
'''

db.define_table('user_loc',
    Field('auth_user_id', db.auth_user),
    Field('loc_id', db.loc),
    #Field('loc_als_id', db.loc_als),
    Field('name', 'string', length=30),
    Field('weather', 'boolean', default=True),
    common_filter=lambda query: db.user_loc.auth_user_id == auth.user_id
    )
