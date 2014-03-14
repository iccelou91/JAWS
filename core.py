#!/usr/bin/env python
import time
import requests

class JAWSResource(object):
    def __init__(self, uris, request_kwargs):
        self.uris = uris
        self.request_kwargs = request_kwargs

    def get_uri_set(self):
        for uri in self.uris:
            yield uri
            
    def __iter__(self):
        for uri in self.get_uri_set():
            response = requests.get(uri, **self.request_kwargs)
            yield response
            
class JAWSParser(object):
    def parse_document(self, document):
        raise RuntimeError("parse_document method not implemented for JAWSParser!")
        
class JAWSOutput(object):
    def store_object(self, obj):
        raise RuntimeError("store_object must be defined for valid JAWSOutput")

    def handle_data(self, data):
        for obj in data:
            self.store_object(obj)

class Scraper(object):
    def __init__(self, resource=None, parser=None, output=None, delay=0):
        if isinstance(resource, JAWSResource):
            self.resource = resource
        else:
            raise TypeError('Scraper resource must be JAWSResource!')

        if isinstance(parser, JAWSParser):
            self.parser = parser
        else:
            raise TypeError('Scraper parser must be JAWSParser!')

        if isinstance(output, JAWSOutput):
            self.output = output
        else:
            raise TypeError('Scraper output must be JAWSOutput!')
        
        self.delay = delay

    def parse_document(self, document):
        return self.parser.parse_document(document)
        
    def scrape_data(self):
        '''
        scrape_data is used to fetch all data from a specified
        resource. Its default implementation returns a generator
        for the objects returned by parse_document for get requests
        to each URI from the URI generator.
        '''
        for response in self.resource:
            time.sleep(self.delay)
            yield self.parse_document(response.text)
            
    def scrape_to_output(self):
        self.output.handle_data(self.scrape_data())
