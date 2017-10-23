SAVE = "Uložit"
KMB_CENA = 2200  # KMB_CENA duplicitně v portal.py ; také v portal/kmb.py aktualizuj výši slevy [%]


def add():
    form = SQLFORM(db.kmb, submit_text=SAVE)
    if form.process().accepted:
        redirect(URL('portal', 'main'))
    response.view = 'kmb/edit.html'
    response.files.append(URL('static', 'js/bootbox.min.js'))
    return dict(form=form, kmb_id=None, KMB_CENA=KMB_CENA)


def edit():
    next = URL('portal', 'main')
    try:
        kmb_id = int(request.args(0))
    except (TypeError, ValueError):
        kmb_id = None
    if kmb_id is None:
        redirect(next)
    kmb = db(db.kmb.id == kmb_id).select(db.kmb.auth_user_id).first()
    if not kmb or kmb.auth_user_id != auth.user_id:
        redirect(next)

    form = SQLFORM(db.kmb, kmb_id, submit_text=SAVE, showid=False)
    if form.process().accepted:
        redirect(next)
    response.files.append(URL('static', 'js/bootbox.min.js'))
    return dict(form=form, kmb_id=kmb_id, KMB_CENA=KMB_CENA)


def delete():
    next = URL('portal', 'main')
    try:
        kmb_id = int(request.args(0))
    except (TypeError, ValueError):
        kmb_id = None
    if kmb_id is None:
        redirect(next)

    db((db.kmb.id == kmb_id) & (db.kmb.auth_user_id == auth.user_id)).delete()
    redirect(next)
