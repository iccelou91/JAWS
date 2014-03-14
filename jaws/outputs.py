#!/usr/bin/env python
import csv
from core import JAWSOutput

class CSVOutput(JAWSOutput):
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
        self.writer.writerow(obj)
