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
    return dict(public_boxes=db((db.box.owner_id==auth.user.id) & (db.box.is_public == True)).select(), private_boxes=db((db.box.owner_id==auth.user.id) & ((db.box.is_public == False) | (db.box.is_public == None))).select())
