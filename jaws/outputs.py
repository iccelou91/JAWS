#!/usr/bin/env python
import csv
from core import JAWSOutput

class CSVOutput(JAWSOutput):
    '''
    CSVOutput is a basic output class that outputs all data given (with a field
    whose name is in the schema) to a csv file using Python's built-in
    csv.DictWriter class. The dialect can be specified on initialization, but
    will default to excel. The filename can also be specified but will default to
    output.csv. By default, the first line of the file will be a title line with
    the names of parameters. If this is not the desired behavior, specify
    title=False on initialization.
    '''
    def _clean_string(self, value):
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

    def __init__(self, schema=None, filename='output.csv', dialect='excel', title=True):
        if schema is not None:
            self.schema = schema
        else:
            raise TypeError("CSVOutput requires schema!")
        csvfile = open(filename, 'wb')
        if title:
            temp_writer = csv.writer(csvfile, dialect=dialect)
            temp_writer.writerow(self.schema)
        self.writer = csv.DictWriter(csvfile, schema, restval='', extrasaction='ignore', dialect=dialect)

    def store_object(self, obj):
        cleaned_obj = dict()
        print "storing object: {obj}".format(obj=obj)
        for key, value in dict(obj).items():
            cleaned_obj[key]=self._clean_string(value)
        self.writer.writerow(cleaned_obj)
