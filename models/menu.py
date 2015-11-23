# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = "Longboxes"
response.logo = A(B(response.title + ' 📦'),
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
        (T('My Collection'), False, URL('collection', 'index'), []),
        (T('Search'), False, URL('collection', 'search'), []),
        (T('New Item'), False, None, [
            (T('Comic'), False, URL('comic', 'new')),
            (T('Box'), False, URL('box', 'new'))
            ]),
    ]

if "auth" in locals(): auth.wikimenu()
