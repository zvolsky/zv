# -*- coding: utf-8 -*-

import datetime


T.force('cs')   # vynucujeme datum bez ohledu na nastavení prohlížeče

class IS_IN_SET_(IS_IN_SET):
    def __init__(self, s):
        super(IS_IN_SET_, self).__init__(s, error_message=T("Prosím vyberte některou možnost: %s.") % s)

class IS_INT_IN_RANGE_(IS_INT_IN_RANGE):
    def __init__(self, a, b):
        super(IS_INT_IN_RANGE_, self).__init__(a, b, error_message=T("Prosím zadejte číslo od %s do %s.") % (a, b))

class IS_DATE_(IS_DATE):
    def __init__(self, format=None):
        super(IS_DATE_, self).__init__(format, error_message=T("Prosím zadejte datum, např. %s.") % datetime.date.today().strftime(str(format)))

class IS_NOT_EMPTY_(IS_NOT_EMPTY):
    def __init__(self):
        super(IS_NOT_EMPTY_, self).__init__(error_message=T("Prosím zadejte tento údaj."))

class IS_FLOAT_IN_RANGE_(IS_FLOAT_IN_RANGE):
    def __init__(self, a, b):
        super(IS_FLOAT_IN_RANGE_, self).__init__(a, b, error_message=T("Prosím zadejte číslo od %s do %s.") % (a, b))


db.define_table('kmb',
    Field('auth_user_id', db.auth_user, default=auth.user_id, ondelete='CASCADE', readable=False, writable=False),
    Field('km', 'integer', requires=IS_INT_IN_RANGE_(1, 2001)),
    Field('cena', 'integer', requires=IS_INT_IN_RANGE_(1, 3000)),
    Field('platnost', 'date', requires=IS_DATE_(format=T('%Y-%m-%d'))),
    Field('predani', 'string', length=192, requires=IS_NOT_EMPTY_()),
    Field('kontakt', 'string', length=192, requires=IS_NOT_EMPTY_()),
    )

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
