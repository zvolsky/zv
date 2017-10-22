SAVE = "Uložit"


def add():
    form = SQLFORM(db.kmb, submit_text=SAVE)
    if form.process().accepted:
        redirect(URL('portal', 'main'))
    response.view = 'kmb/edit.html'
    return dict(form=form, kmb_id=None)


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
    return dict(form=form, kmb_id=kmb_id)


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
