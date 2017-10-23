# -*- coding: utf-8 -*-

def main():
    loc = None
    if auth.user_id:
        loc = db((db.user_loc.auth_user_id == auth.user_id) & (db.user_loc.weather == True)).select(
            db.loc.w24, db.loc.yr,
            join=db.loc.on(db.loc.id == db.user_loc.loc_id)
        ).first()

    # KMB
    kmb = db((db.kmb.km > 0) & (db.kmb.platnost >= datetime.date.today())).select(db.kmb.ALL, orderby=db.kmb.km)
    response.files.append(URL('static', 'css/no-more-tables.css'))

    return dict(loc=loc, kmb=kmb, KMB_CENA=2200)  # KMB_CENA duplicitně v kmb.py
