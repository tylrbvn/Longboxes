# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import datetime
@auth.requires_login()

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def new():
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
            created_on = datetime.datetime.now())
            db.commit
            response.flash = "New box '" + form.vars.name + "' successfully created!"
        else:
            response.flash = "You already have a box called '" + form.vars.name + "', please enter a new name!"
    elif form.errors:
        response.flash = 'One or more of the entries is incorrect:'
    return dict(addform=form)

def view():
    box_id = request.args(0)
    if box_id is not None:
        boxes = db((db.box.id == box_id) & ((db.box.is_public == True) | (db.box.owner_id == auth.user.id))).select()
        if len(boxes)>0:
            comics = db((db.comic_in_box.box_id == box_id) & (db.comic_in_box.comic_id == db.comic.id)).select()
            return dict(boxes = boxes, comics = comics)
    return dict()
