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
    return dict(public_boxes=db((db.box.owner_id==auth.user.id) & (db.box.is_public == True)).select(), private_boxes=db((db.box.owner_id==auth.user.id) & (db.box.is_public != True)).select())

@auth.requires_login()
def new_comic():
    db.comic.owner_id.readable = db.comic.owner_id.writable = False
    form = SQLFORM(db.comic)
    form.vars.owner_id = auth.user.id
    if form.accepts(request.vars, session):
        query = (db.box.owner_id == auth.user.id) & (db.box.name == 'Unfiled')
        unfiled_id = db.box(query).id
        db.comic_in_box.insert(comic_id = form.vars.id, box_id = unfiled_id)
        db.commit
        response.flash = "New comic '" + form.vars.title + "' succesfully created!"
    elif form.errors:
        response.flash = 'One or more of the entries is incorrect:'
    return dict(addform=form)

@auth.requires_login()
def new_box():
    #Form to create a new box
    form = FORM(DIV(LABEL('Name:', _for='name')),
                DIV(INPUT(_name='name', requires=IS_NOT_EMPTY())),
                DIV(LABEL('Public box:', _for='is_public'), INPUT(_name='is_public', _type='checkbox')),
                DIV(INPUT(_type='submit')))
    if form.accepts(request, session):
        query = ((db.box.owner_id == auth.user.id) & (db.box.name == form.vars.name))
        count = db(query).count()
        if (count == 0):
            db.box.insert(name=request.vars.name,
            is_public=request.vars.is_public,
            owner_id=auth.user.id,
            created_on = datetime.date.today())
            db.commit
            response.flash = "New box '" + form.vars.name + "' succesfully created!"
        else:
            response.flash = "You already have a box called '" + form.vars.name + "', please enter a new name!"
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
