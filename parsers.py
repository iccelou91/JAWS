#!/usr/bin/env python
import HTMLParser
from core import JAWSParser

def clean_string(value):
    try:
        value = value.encode('utf-8')
    except UnicodeError:
        value = ''.join(i for i in value if ord(i)<128)
        return value.encode('utf-8')
    else:
        # value was valid ASCII data
        return value

class HTMLFormParser(HTMLParser.HTMLParser, JAWSParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.HTMLParser.__init__(self)
        self.data = dict()
        self.last_tag = None
        self.last_tag_name = None

    def parse_document(self, document):
        self.feed(document)
        return self.data
        
    def read(self, data):
        # clear the current output before re-use
        self._lines = []
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return ''.join(self._lines)

    def handle_data(self, d):
        self._lines.append(d)

    def handle_starttag(self, tag, attrs):
        name = ''
        value = ''
        for attr_name, attr_value in attrs:
            if attr_name == 'value':
                value = clean_string(attr_value)
            elif attr_name == 'name':
                name = clean_string(attr_value)
        self.last_tag = tag
        self.last_tag_name = name
        self.current_tag_name = name
        if tag == 'input' and ('type', 'text') in attrs:
            self.data[name]=value
            
    def handle_endtag(self, tag):
        if self.last_tag == tag:
            self.last_tag = None
            self.last_tag_name = None
                
    def handle_data(self, data):
        if self.last_tag == 'textarea':
            self.data[self.last_tag_name]=clean_string(data)
