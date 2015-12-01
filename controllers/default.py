# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import datetime

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    #Get the 5 largest public boxes
    count = db.comic_in_box.box_id.count()  #What we are counting, the number of comics in each box
    #Perform the joint query and get info about owner
    largest_boxes = db((db.box.id==db.comic_in_box.box_id) & (db.box.is_public==True) & (db.box.owner_id == db.auth_user.id)).select(db.box.name, db.box.id, db.auth_user.screen_name, count, groupby=db.comic_in_box.box_id, orderby=~count, limitby=(0,5))
    #Get the 5 newest public boxes and info about owner
    newest_boxes=db((db.box.is_public == True) & (db.box.owner_id == db.auth_user.id)).select(orderby=~db.box.created_on, limitby=(0, 5))
    return dict(newest_boxes=newest_boxes,largest_boxes=largest_boxes)

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
