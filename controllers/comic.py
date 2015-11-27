# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def form():
    return dict()

@auth.requires_login()
def add():
    #Retrieve box record using ID
    comic = db.comic(request.args(0))
    #Get list of users boxes
    #TODO: Exclude boxes that comic is already in
    boxes = db(db.box.owner_id == auth.user.id).select()
    #Check if there exists a comic with ID
    if (comic):
        #Check user owns that comic
        if (comic.owner_id == auth.user.id):
            #Form that displays list of comics titles but returns comic ID
            form = FORM(DIV(LABEL('Select a box:', _for='box', _class="control-label col-sm-3"),
                        DIV(SELECT(_name='box', *[OPTION(boxes[i].name, _value=str(boxes[i].id)) for i in range(len(boxes))],
                        _class = "form-control select"), _class="col-sm-4"), _class = "form-group"),
                        DIV(DIV(INPUT(_class = "btn btn-primary", _value='Add to box', _type="submit"),
                        A('Cancel', _href=URL('comic', 'view', args=comic.id), _class = "btn btn-default"),
                        _class="col-sm-9 col-sm-offset-3"),
                        _class="form-group"),
                        _class="form-horizontal")

            if form.accepts(request, session):
                #Ensure comic not already in box
                count = db((db.comic_in_box.box_id == request.vars.box) & (db.comic_in_box.comic_id == comic.id)).count()
                if (count == 0):
                    db.comic_in_box.insert(comic_id = comic.id,
                    box_id = request.vars.box)
                    db.commit
                    #Check if comic in user's Unfiled box
                    unfiled_id = db.box((db.box.owner_id == auth.user.id) & (db.box.name == 'Unfiled')).id
                    link = db.comic_in_box((db.comic_in_box.comic_id == comic.id) & (db.comic_in_box.box_id == unfiled_id))
                    #Delete the link
                    if (link):
                        db(db.comic_in_box.id == link.id).delete()
                    response.flash = "'" + comic.title + "' successfully added to box"
                else:
                    response.flash = "Error: Selected box already contains '" + comic.title + "'"
            elif form.errors:
                response.flash = 'One or more of the entries is incorrect:'
            return dict(form = form, comic = comic)
    return dict()

@auth.requires_login()
def copy():
    comic_id = request.args(0)
    #Ensure that the comic to be copied is in another user's public box
    count = db((db.comic_in_box.comic_id == comic_id) & (db.comic_in_box.box_id == db.box.id) & (db.box.is_public == True) & (db.box.owner_id != auth.user.id)).count()
    if (count > 0):
        #Get the comic to be copied
        comic = db.comic(comic_id)

        #Get list of user's boxes
        boxes = db(db.box.owner_id == auth.user.id).select()
        form = FORM(DIV(LABEL('Select a box:', _for='box', _class="control-label col-sm-3"),
                    DIV(SELECT(_name='box', *[OPTION(boxes[i].name, _value=str(boxes[i].id)) for i in range(len(boxes))],
                    _class = "form-control select"), _class="col-sm-4"), _class = "form-group"),
                    DIV(DIV(INPUT(_class = "btn btn-primary", _value='Add to box', _type="submit"),
                    A('Cancel', _href=URL('comic', 'view', args=comic.id), _class = "btn btn-default"),
                    _class="col-sm-9 col-sm-offset-3"),
                    _class="form-group"),
                    _class="form-horizontal")

        if form.accepts(request, session):
            #Make a copy of the comic and get ID
            comic_id = db.comic.insert(title = comic.title,
            issue = comic.issue,
            writers = comic.writers,
            artists = comic.artists,
            publisher = comic.publisher,
            description = comic.description,
            cover = comic.cover,
            owner_id = auth.user.id)
            #Add to box selected in form
            db.comic_in_box.insert(comic_id = comic_id,
            box_id = request.vars.box)
            db.commit
            response.flash = "'" + comic.title + "' successfully copied to your collection"
        return dict(form=form, comic_title = comic.title)
    return dict()

@auth.requires_login()
def delete():
    comic = db.comic(request.args(0))
    #Check user owns comic with ID
    if (comic):
        if (comic.owner_id == auth.user.id):
            form = FORM(DIV(LABEL('Confirm comic deletion:', _for='submit', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "btn btn-danger", _value='Delete', _type="submit"),
                A('Cancel', _href=URL('comic', 'view', args=comic.id), _class = "btn btn-default"),
                 _class="col-sm-9"),
                _class="form-group"),
                _class="form-horizontal")

            if form.accepts(request):
                #Delete the comic
                db(db.comic.id == comic.id).delete()
                session.message = "Comic '" + comic.title + "' successfully deleted!"
                redirect(URL('collection', 'index'))
            return dict(form = form)
    return dict()

@auth.requires_login()
def edit():
    #Retrieve comic record using ID
    record = db.comic(request.args(0))
    db.comic.id.readable = db.comic.id.writable = False
    db.comic.owner_id.readable = db.comic.owner_id.writable = False
    #Check if there exists a comic with ID
    if(record):
        #Check user owns that comic
        if (record.owner_id == auth.user.id):
            edit=SQLFORM(db.comic, record, deletable=True)
            if edit.accepts(request,session):
                response.flash = 'Comic has been successfully updated.'
            elif edit.errors:
                response.flash = 'One or more of the entries is incorrect:'
            return dict(editform=edit)
    return dict()

@auth.requires_login()
def new():
    #Get list of users boxes
    boxes = db(db.box.owner_id == auth.user.id).select()
    form = FORM(DIV(LABEL('Title:', _for='title', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "form-control string", _name='title', _type="text", requires=IS_NOT_EMPTY()), _class="col-sm-9"), _class="form-group"),
                DIV(LABEL('Issue:', _for='issue', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "integer form-control", _name='issue', _type="text", requires=IS_NOT_EMPTY()), _class="col-sm-9"), _class="form-group"),
                DIV(LABEL('Writers:', _for='writers', _class="control-label col-sm-3"),
                DIV(UL(LI(INPUT(_name="writers", _type="text", _class="form-control string", requires=IS_NOT_EMPTY())), _class="w2p_list", _style="list-style:none"), _class="col-sm-9"), _class="form-group"),
                DIV(LABEL('Artists:', _for='artists', _class="control-label col-sm-3"),
                DIV(UL(LI(INPUT(_name="artists", _type="text", _class="form-control string", requires=IS_NOT_EMPTY())), _class="w2p_list", _style="list-style:none"), _class="col-sm-9"), _class="form-group"),
                DIV(LABEL('Publisher:', _for='title', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "form-control string", _name='publisher', _type="text", requires=IS_NOT_EMPTY()), _class="col-sm-9"), _class="form-group"),
                DIV(LABEL('Description:', _for='description', _class="control-label col-sm-3"),
                DIV(TEXTAREA(_class = "text form-control", _name='description', _rows="5", requires=IS_EXPR('len(value.split())<=300', error_message='Description too long, maximum of 300 words')), _class="col-sm-9"), _class="form-group"),
                DIV(LABEL('Cover:', _for='cover', _class="control-label col-sm-3"),
                DIV(INPUT(_class = "upload input-file", _name='cover', _type="file", requires=IS_EMPTY_OR(IS_IMAGE(maxsize=(300,400), error_message="Choose an image of 300 x 400 pixels max"))), _class="col-sm-9"), _class="form-group"),
                DIV(LABEL('Destination:', _for='box', _class="control-label col-sm-3"),
                DIV(SELECT(_name='box', *[OPTION(boxes[i].name, _value=str(boxes[i].id)) for i in range(len(boxes))], _type="select", _class = "form-control select"), _class="col-sm-9"), _class="form-group"),
                DIV(DIV(INPUT(_class = "btn btn-primary", _value='Submit', _type="submit"),
                A('Cancel', _onclick="history.back(-1)", _class = "btn btn-default"),
                _class="col-sm-9 col-sm-offset-3"), _class="form-group"),
                _class="form-horizontal")

    if form.accepts(request.vars, session):
        #Insert comic and get ID
        comic_id = db.comic.insert(title = request.vars.title,
        issue = request.vars.issue,
        writers = request.vars.writers,
        artists = request.vars.artists,
        publisher = request.vars.publisher,
        description = request.vars.description,
        cover = request.vars.cover,
        owner_id = auth.user_id)
        db.commit
        #Link comic to selected box
        db.comic_in_box.insert(comic_id = comic_id, box_id = form.vars.box)
        db.commit
        response.flash = "New comic '" + form.vars.title + "' has been successfuly created."
    elif form.errors:
        response.flash = 'One or more of the entries is incorrect:'
    return dict(form=form)

def view():
    comic_id = request.args(0)
    if comic_id is not None:
        #If own comic
        if auth.is_logged_in():
            comics = db((db.comic.id == comic_id) & (db.comic.owner_id == auth.user.id) & (db.comic.owner_id == db.auth_user.id)).select()
            if len(comics)>0:
                return dict(comics = comics)
        #If a comic from another user's public box
        public = db((db.comic_in_box.comic_id == comic_id) & (db.comic_in_box.box_id == db.box.id) & (db.box.is_public == True)).select()
        if len(public)>0:
            comics = db((db.comic.id == comic_id) & (db.comic.owner_id == db.auth_user.id)).select()
            return dict(comics = comics)
    return dict()
