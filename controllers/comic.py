# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

@auth.requires_login()
def new():
    db.comic.owner_id.readable = db.comic.owner_id.writable = False
    form = SQLFORM(db.comic)
    form.vars.owner_id = auth.user.id
    if form.accepts(request.vars, session):
        query = (db.box.owner_id == auth.user.id) & (db.box.name == 'Unfiled')
        unfiled_id = db.box(query).id
        db.comic_in_box.insert(comic_id = form.vars.id, box_id = unfiled_id)
        db.commit
        response.flash = "New comic '" + form.vars.title + "' successfully created!"
    elif form.errors:
        response.flash = 'One or more of the entries is incorrect:'
    return dict(addform=form)

@auth.requires_login()
def view():
    comic_id = request.args(0)
    if comic_id is not None:
        comics = db((db.comic.id == comic_id) & (db.comic.owner_id == auth.user.id)).select()
        if len(comics)>0:
            return dict(comics = comics)
    return dict()
