# coding: utf8

@auth.requires_login()
def locations():
    locs = db(db.user_loc).select()
    grid = SQLFORM.grid(
        db.user_loc,
        showbuttontext=False,
        paginate=100,
        searchable=False,
        )
    return dict(grid=grid)
