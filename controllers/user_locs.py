# -*- coding: utf-8 -*-

import geopy


GC_FAILED_MSG = T("Vyhledávání polohy místa (geocoding) selhalo. Zkuste to prosím za krátkou dobu znova.")


@auth.requires_login()
def list():
    locs = db().select(db.user_loc.ALL, db.loc.ALL,
        join=db.loc.on(db.loc.id==db.user_loc.loc_id)
    )
    return dict(locs=locs)


@auth.requires_login()
def new():
    form = SQLFORM.factory(
            db_extra['loc_country_id'],
            db_extra['loc_name'],
            submit_button=T("Dohledat a přidat místo")
    )
    if form.process().accepted:
        loc = db((db.loc.country_id == form.vars.country_id) & (db.loc.name == form.vars.name)).select(
            db.loc.id, db.loc.lat, db.loc.lon).first()
        if loc:
            loc_id = db.loc.id
            lat = loc.lat
            lon = loc.lon
        else:
            code2 = get_code2(form.vars.country_id)
            gc = geopy.geocoders.Nominatim(format_string="%s, " + code2)
            try:
                loc = gc.geocode(form.vars.name)
            except geopy.exc.GeopyError:  # geopy extension base class
                session.flash = GC_FAILED_MSG
                redirect(URL())
            if not loc:
                session.flash = T("Nebylo nalezeno žádné takové místo.")
                redirect(URL())
            loc_id = 0
            lat = loc.latitude
            lon = loc.longitude
        redirect(URL('new2', vars={'id': loc_id, 'lat': lat, 'lon': lon, 'cid': form.vars.country_id, 'name': form.vars.name}))
    return dict(form=form)


@auth.requires_login()
def new2():
    assert (int(request.vars.id) >= 0 and int(request.vars.cid) > 0 and request.vars.name and
            -90.0 <= float(request.vars.lat) <= 90.0 and -180.0 <= float(request.vars.lon) <= 180.0)
    return {'id': request.vars.id, 'lat': request.vars.lat, 'lon': request.vars.lon,
            'cid': request.vars.cid, 'name': request.vars.name}


@auth.requires_login()
def new2_more():
    assert int(request.vars.cid) > 0 and request.vars.name
    code2 = get_code2(request.vars.cid)
    gc = geopy.geocoders.Nominatim(format_string="%s, " + code2)
    try:
        locs = gc.geocode(name, exactly_one=False)
    except geopy.exc.GeopyError:  # geopy extension base class
        session.flash = GC_FAILED_MSG
        redirect(URL('new2_retry', vars={'cid': request.vars.cid, 'name': request.vars.name}))
    return dict(locs=locs)


@auth.requires_login()
def new2_retry():
    assert int(request.vars.cid) > 0 and request.vars.name
    return dict(cid=request.vars.cid, name=request.vars.name)


@auth.requires_login()
def new2_accepted():
    assert (int(request.vars.id) >= 0 and int(request.vars.cid) > 0 and request.vars.name and
            -90.0 <= float(request.vars.lat) <= 90.0 and -180.0 <= float(request.vars.lon) <= 180.0)
    if request.vars.id:
        loc_id = request.vars.id
    else:
        loc_id = db.loc.insert(country_id=request.vars.cid, name=request.vars.name,
                               lat=request.vars.lat, lon=request.vars.lon)
    user_loc_id = db.user_loc.insert(loc_id=loc_id)
    redirect(URL('edit_user_loc', vars={'id': user_loc_id}))


@auth.requires_login()
def edit_user_loc():
    assert request.vars.id > 0
    user_loc_id = request.vars.id
    if my_user_loc(user_loc_id):
        session.flash = "Edit - not implemented yet"
        redirect(URL('list'))
    else:
        redirect(URL('list'))


@auth.requires_login()
def delete():
    assert request.vars.id > 0
    user_loc_id = request.vars.id
    if my_user_loc(user_loc_id):
        del db.user_loc[user_loc_id]
    redirect(URL('list'))


# functions for controllers above

def my_user_loc(loc_id):
    """return ~True """
    return db(db.user_loc.id == loc_id).select(db.user_loc.id).first()


def get_code2(cid):
    return db(db.country.id == cid).select(db.country.code2).first().code2
