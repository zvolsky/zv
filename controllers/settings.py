# coding: utf8

@auth.requires_login()
def main():
    redirect(URL('user_locs', 'list'))
