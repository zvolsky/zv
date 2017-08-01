# -*- coding: utf-8 -*-

def main():
    loc = None
    if auth.user_id:
        loc = db((db.user_loc.auth_user_id == auth.user_id) & (db.user_loc.weather == True)).select(
            db.loc.w24, db.loc.yr,
            join=db.loc.on(db.loc.id == db.user_loc.loc_id)
        ).first()
    return dict(loc=loc)
