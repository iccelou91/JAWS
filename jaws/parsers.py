#!/usr/bin/env python
from core import JAWSParser
from HTMLParser import HTMLParser

class JAWSHTMLParser(JAWSParser, HTMLParser):
    '''
    JAWSHTMLParser is a utility base class that can be used to easily
    implement a parser for HTML documents using pythons HTMLParser class. The
    JAWSHTMLParser already inherits from both the JAWSParser and the
    HTMLParser. A correct implementation for an HTML parser class will
    implement some or all of the methods used by the HTMLParser class in such a
    way that when self.feed() returns, the field self._data contains a
    a dictionary with all data to be returned by parse_document.
    '''
    def __init__(self)
        # initialize the base class
        HTMLParser.__init__(self)
        
    def _clear_state(self):
        # don't use data from previous documents
        self._data = dict()
        
    def parse_document(self, document):
        # clear out old data
        self._clear_state()
        # Pass document into self for parsing
        self.feed(document)
        # Return data obtained by feed
        return self._data()

class HTMLFormParser(JAWSHTMLParser):
    '''
    HTMLFormParser is a quick and dirty implementation of a parser for HTML
    forms. It extends the JAWSHTMLParser to add methods for parsing the value
    of value attributes in form text fields and the content of textarea tags.
    '''
    class InnerHTMLFormParser(HTMLParser):
        def _clear_state(self):
            # Clear all inherited state
            super(HTMLFormParser, self)._clear_state()
            # Clear variables used for scraping textareas
            self._last_tag = None
            self._last_tag_name = None

        def handle_starttag(self, tag, attrs):
            name = ''
            value = ''
            for attr_name, attr_value in attrs:
                if attr_name == 'value':
                    value = attr_value
                elif attr_name == 'name':
                    name = attr_value
            self.last_tag = tag
            self.last_tag_name = name
            self.current_tag_name = name
            if tag == 'input' and ('type', 'text') in attrs:
                self._data[name]=value
                
        def handle_endtag(self, tag):
            if self.last_tag == tag:
                self.last_tag = None
                self.last_tag_name = None
                    
        def handle_data(self, data):
            if self.last_tag == 'textarea':
                self._data[self.last_tag_name]=data
            
class JSONParser(JAWSParser):
    '''
    This incredibly straightforward class feeds its data directly into python's
    json.JSONDecoder class. It can be initialized with any of the aruments that
    json.JSONDecoder can take.
    '''
    def __init__(self, **decoder_args):
        import json
        self.parser = json.JSONDecoder(**decoder_args)
        
    def parse_document(self, document):
        return self.parser.decode(document)
