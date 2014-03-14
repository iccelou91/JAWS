#!/usr/bin/env python
import requests
import mechanize
import cookielib
from core import JAWSResource
        
class URIPatternResource(JAWSResource):
    def __init__(self, request_kwargs, uri_format, id_range):
        self.id_range = id_range
        self.uri_format = uri_format
        self.request_kwargs = request_kwargs
        
    def get_uri_set(self):
        for id in self.id_range:
            yield self.uri_format.format(id=id)
            
class AuthURIPatternResource(URIPatternResource):
    def __init__(self, auth_uri, creds, *args, **kwargs):
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # User-Agent
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        br.open(auth_uri)
        br.select_form(name="loginform")
        for key, value in creds.items():
            br.form[key]=value
        auth_response = br.submit()
        if auth_response.code == 200:
            super(AuthURIPatternResource, self).__init__({'cookies':cj,}, *args, **kwargs)
        else:
            raise RuntimeError("Authentication failed!")
