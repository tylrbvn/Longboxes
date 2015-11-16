# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import datetime

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    return dict(message=T('Welcome to Longboxes!'))

@auth.requires_login()
def new_comic():
    db.comic.owner_id.readable = db.comic.owner_id.writable = False
    form = SQLFORM(db.comic)
    form.vars.owner_id = auth.user.id
    if form.accepts(request.vars, session):
        #Get the ID of the users unfiled box and insert the new comic
        query = (db.box.owner_id == form.vars.owner_id) & (db.box.name == 'Unfiled')
        unfiled_id = db.box(query).id
        db.comic_in_box.insert(comic_id = form.vars.id, box_id = unfiled_id)
        db.commit
        response.flash = 'New comic succesfully added to your unfiled box.'
    elif form.errors:
        response.flash = 'One or more of the entries is incorrect:'
    return dict(addform=form)

@auth.requires_login()
def new_box():
    db.box.owner_id.readable = db.box.owner_id.writable = False
    db.box.created_on.readable = db.box.created_on.writable = False
    form = SQLFORM(db.box)
    form.vars.owner_id = auth.user.id
    form.vars.created_on = datetime.date.today()
    if form.accepts(request.vars, session):
        response.flash = 'New box succesfully created.'
    elif form.errors:
        response.flash = 'One or more of the entries is incorrect:'
    return dict(addform=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
