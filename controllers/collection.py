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
    #If user doesn't have an Unfiled box, create one
    #This ideally would be triggered after registration
    if (db((db.box.owner_id == auth.user.id) & (db.box.name == 'Unfiled')).count()==0):
        db.box.insert(name='Unfiled',
        is_public='False',
        owner_id=auth.user.id,
        created_on = datetime.datetime.now())
        db.commit
    #Display any necessary message
    if (session.message):
        response.flash = session.message
        session.message = None
    return dict(public_boxes=db((db.box.owner_id==auth.user.id) & (db.box.is_public == True)).select(), private_boxes=db((db.box.owner_id==auth.user.id) & ((db.box.is_public == False) | (db.box.is_public == None))).select())

@auth.requires_login()
def all():
    boxes = db((db.box.owner_id == auth.user.id) & (auth.user.id == db.auth_user.id)).select()
    if len(boxes)>0:
        comics = {}
        for box in boxes:
            comics[box.box.id] = db((db.comic_in_box.box_id == box.box.id) & (db.comic_in_box.comic_id == db.comic.id) & (db.comic.owner_id == db.auth_user.id)).select()
        return dict(boxes = boxes, comics = comics)
    return dict()

@auth.requires_login()
def search():
    form = FORM(DIV(LABEL('Title:', _for='title', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "form-control string", _name='title', _type="text"), _class="col-sm-3"),
                _class="form-group"),
                DIV(LABEL('Writer:', _for='writer', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "form-control string", _name='writer', _type="text"), _class="col-sm-3"),
                _class="form-group"),
                DIV(LABEL('Artist:', _for='artist', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "form-control string", _name='artist', _type="text"), _class="col-sm-3"),
                _class="form-group"),
                DIV(LABEL('Publisher:', _for='publisher', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "form-control string", _name='publisher', _type="text"), _class="col-sm-3"),
                _class="form-group"),
                DIV(DIV(INPUT(_class = "btn btn-primary", _value='Search', _type="submit"),
                _class="col-sm-9 col-sm-offset-3"),
                _class="form-group"),
                _class="form-horizontal")

    if form.accepts(request, session):
        search_term = ""
        if (len(request.vars.title) > 0):
            title_term = "%" + request.vars.title + "%"
            search_term = (db.comic.title.like(title_term))
        if (len(request.vars.writer) > 0):
            writer_term = "%" + request.vars.writer + "%"
            if (search_term):
                search_term = search_term & (db.comic.writers.like(writer_term))
            else:
                search_term = (db.comic.writers.like(writer_term))
        if (len(request.vars.artist) > 0):
            artist_term = "%" + request.vars.artist + "%"
            if (search_term):
                search_term = search_term & (db.comic.artists.like(artist_term))
            else:
                search_term = (db.comic.artists.like(artist_term))
        if (len(request.vars.publisher) > 0):
            publisher_term = "%" + request.vars.publisher + "%"
            if (search_term):
                search_term = search_term & (db.comic.publisher.like(publisher_term))
            else:
                search_term = (db.comic.publisher.like(publisher_term))
        #Allow for a blank search to return all comics
        #TODO: Disallow for when this search could overload system, i.e. lots of public comics
        constraint = (db.comic_in_box.box_id == db.box.id) & ((db.box.is_public == True) | (db.box.owner_id == auth.user.id)) & (db.comic_in_box.comic_id == db.comic.id) & (db.comic.owner_id == db.auth_user.id)
        if (search_term):
            search_term =  search_term & constraint
        else:
            search_term = constraint
        results = db(search_term).select()
        #Output success indicated by number of result(s)
        output = "Search complete: " + str(len(results)) + " result"
        if(len(results) != 1): output += "s"
        response.flash = output
    else:
        if form.errors:
            response.flash = 'One or more of the entries is incorrect'
        results = dict()
    return dict(form = form, results = results)
