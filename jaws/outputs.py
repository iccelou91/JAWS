#!/usr/bin/env python
import csv
from core import JAWSOutput

class CSVOutput(JAWSOutput):
    def clean_string(self, value):
        try:
            value = str(value)
            try:
                value = value.encode('utf-8')
            except UnicodeError:
                value = ''.join(i for i in value if ord(i)<128)
                return value.encode('utf-8')
            else:
                # value was valid ASCII data
                return value
        except:
            # Couldn't parse object correctly
            return ''

    def __init__(self, schema=None, filename='output.csv'):
        if schema is not None:
            self.schema = schema
        else:
            raise TypeError("CSVOutput requires schema!")
        csvfile = open(filename, 'wb')
        self.writer = csv.writer(csvfile, dialect='excel')
        self.writer.writerow(self.schema)
        self.writer = csv.DictWriter(csvfile, schema, restval='', extrasaction='ignore', dialect='excel')

    def store_object(self, obj):
        cleaned_obj = dict()
        for key, value in dict(obj).items():
            cleaned_obj[key]=self.clean_string(value)
        self.writer.writerow(cleaned_obj)
