# -*- coding: utf-8 -*-

class IS_IN_SET_(IS_IN_SET):
    def __init__(self, s):
        super(IS_IN_SET_, self).__init__(s, error_message=T("Prosím vyberte některou možnost."))

class IS_NOT_EMPTY_(IS_NOT_EMPTY):
    def __init__(self):
        super(IS_NOT_EMPTY_, self).__init__(error_message=T("Prosím zadejte."))

class IS_FLOAT_IN_RANGE_(IS_FLOAT_IN_RANGE):
    def __init__(self, a, b):
        super(IS_FLOAT_IN_RANGE_, self).__init__(a, b, error_message=T("Není ve správném rozmezí."))


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
db_extra = {
    'loc_country_id': Field('country_id', db.country, requires=IS_IN_SET_(countries),
                            label=T("Stát")),
    'loc_name': Field('name', 'string', length=50, requires=IS_NOT_EMPTY_(),
                            label=T("Místo")),
}
db.define_table('loc',
    db_extra['loc_country_id'],
    #Field('state', 'string', length=2),
    db_extra['loc_name'],
    Field('lat', 'double', requires=IS_FLOAT_IN_RANGE_(-90.0, 90.0)),
    Field('lon', 'double', requires=IS_FLOAT_IN_RANGE_(-180.0, 180.0)),
    Field('w24', 'string', length=40),
    Field('yr', 'string', length=50),
    format='%(name)s'
    )

'''
db.define_table('loc_als',
    Field('name', 'string', length=40),
    Field('lang', 'string', length=3),
    )
'''

db.define_table('user_loc',
    Field('auth_user_id', db.auth_user, default=auth.user_id),
    Field('loc_id', db.loc),
    #Field('loc_als_id', db.loc_als),
    Field('name', 'string', length=30),
    Field('weather', 'boolean'),
    common_filter=lambda query: db.user_loc.auth_user_id == auth.user_id,
    format='user %(auth_user_id)s loc %(loc_id)s'
    )
