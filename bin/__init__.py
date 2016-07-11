#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import argparse
from topogram_client import TopogramAPIClient, set_debugging

def parse_CSV_data(filename):
    """Parse CSV data from file"""
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    print "Data: %s rows to export"%len(data)
    return data

def main() :
    parser = argparse.ArgumentParser(description='import CSV data into Topogram')
    parser.add_argument('filename', action="store", default=None, help='CSV file path' )
    parser.add_argument('--base-url', default='http://localhost:3000', help='Base URL for Topogram API endpoint')
    parser.add_argument('--user', default=None, help='Username')
    parser.add_argument('--password', default=None, help='Password' )
    parser.add_argument('--title', default="Test", help='Title of the document' )
    parser.add_argument('--verbose', default=False, help='Log' )

    args = parser.parse_args()


    print args.base_url
    client = TopogramAPIClient(args.base_url, args.user, args.password, debug=args.verbose)

    #check if the file exists
    if not os.path.isfile(args.filename) : raise ValueError("CSV File '%s' doesn't exist"%args.filename)

    # parse data
    data = parse_data(args.filename)

if __name__ == '__main__':
    main()
