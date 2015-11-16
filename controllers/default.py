# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

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

def old_comic():
    #Form too create a new comic
    addform = FORM(DIV(LABEL('Title:', _for='comic_title')),
                   DIV(INPUT(_name='comic_title', requires=IS_NOT_EMPTY())),
                   DIV(LABEL('Issue Number:', _for='comic_issue')),
                   DIV(INPUT(_name='comic_issue',requires=IS_NOT_EMPTY())),
                   DIV(LABEL('Writers:', _for='comic_writers')),
                   DIV(INPUT(_name='comic_writers',requires=IS_NOT_EMPTY())),
                   DIV(LABEL('Artists:', _for='comic_artists')),
                   DIV(INPUT(_name='comic_artists',requires=IS_NOT_EMPTY())),
                   DIV(LABEL('Publisher:', _for='comic_publisher')),
                   DIV(INPUT(_name='comic_publisher',requires=IS_NOT_EMPTY())),
                   DIV(LABEL('Description:', _for='comic_description')),
                   DIV(TEXTAREA(_name='comic_description', requires=IS_NOT_EMPTY())),
                   DIV(LABEL('Cover Art:', _for='comic_art')),
                   DIV(INPUT(_name='comic_art', _type='file', requires=IS_NOT_EMPTY())),
                   DIV('No larger than 400 x 300 pixels (to be implemented)'),
                   DIV(INPUT(_type='submit')),
                   DIV(LABEL()))

    if addform.accepts(request, session):
        db.comic.insert(title=request.vars.comic_title,
        issue=request.vars.comic_issue,
        writers=request.vars.comic_writers,
        artists=request.vars.comic_artists,
        publisher=request.vars.comic_publisher,
        description=request.vars.comic_description,
        cover=request.vars.comic_art,
        owner_id=auth.user.id)
        db.commit
        response.flash = 'New comic succesfully added.'
    elif addform.errors:
        response.flash = 'One or more of the entries is incorrect:'
    #else:
        #response.flash = 'Please complete the form below to add a new comic.'
    return dict(addform=addform)

@auth.requires_login()
def new_comic():
    db.comic.owner_id.readable = db.comic.owner_id.writable = False
    form = SQLFORM(db.comic)
    form.vars.owner_id = auth.user.id
    if form.accepts(request.vars, session):
        response.flash = 'New comic succesfully added.'
    elif form.errors:
        response.flash = 'One or more of the entries is incorrect:'
    return dict(addform=form)

def new_box():
    return dict()

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
