#!/usr/bin/env python
from core import JAWSParser

class HTMLFormParser(JAWSParser):
    from HTMLParser import HTMLParser
    class InnerHTMLFormParser(HTMLParser):
        def __init__(self):
            from HTMLParser import HTMLParser
            # initialize the base class
            HTMLParser.__init__(self)
            self.data = dict()
            self.last_tag = None
            self.last_tag_name = None
            
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
                    value = attr_value
                elif attr_name == 'name':
                    name = attr_value
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
                self.data[self.last_tag_name]=data
            
    def parse_document(self, document):
        # Make a new parser for this document
        parser = self.InnerHTMLFormParser()
        # Pass document into self for parsing
        parser.feed(document)
        return parser.data
            
class JSONParser(JAWSParser):
    def __init__(self, **decoder_args):
        import json
        self.parser = json.JSONDecoder(**decoder_args)
        
    def parse_document(self, document):
        return self.parser.decode(document)
