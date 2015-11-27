# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = "Longboxes"
response.logo = A(B(response.title),
                  _class="navbar-brand",_href=URL('default', 'index'),
                  _id="web2py-logo")


## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Y1469492'
response.meta.description = "A comic collector's favourite tool."

## your http://google.com/analytics id
#response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

if auth.is_logged_in():
    response.menu = [
        (T('Collection'), False, URL('collection', 'index'), []),
        (T('Comics'), False, None, [
            (T('Search'), False, URL('collection', 'search')),
            (T('View All'), False, URL('collection', 'all'))
            ]),
        (T('New'), False, None, [
            (T('Box'), False, URL('box', 'new')),
            (T('Comic'), False, URL('comic', 'new'))
            ]),
    ]

if "auth" in locals(): auth.wikimenu()
