#!python2

import argparse
import datetime
#import requests
import json
import urllib
import sys

def main(query):
    api_key = "AIzaSyD6noA17xsrGSHWuqC-TOGWMvlEPPKJ91E"
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

    params = {
        'query': query,
        'limit': 5,
        'indent': True,
        'key': api_key,
    }

    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    print('Displaying results...' + ' (limit: ' + str(params['limit']) + ')\n')
    for element in response['itemListElement']:
        """try:
            types = str(", ".join([n for n in element['result']['@type']]))
        except KeyError:
            types = "N/A"
		"""

        try:
            desc = str(element['result']['description']).encode('utf8')
        except KeyError:
            desc = "N/A"

        """try:
            detail_desc = str(element['result']['detailedDescription']['articleBody']).encode('utf8')[0:1000]
        except KeyError:
            detail_desc = "N/A"

        try:
            mid = str(element['result']['@id'])
        except KeyError:
            mid = "N/A"

        try:
            url = str(element['result']['url'])
        except KeyError:
            url = "N/A" """

        try:
            score = str(element['resultScore'])
        except KeyError:
            score = "N/A"

        #print(element['result']['name'] \
         #     + '\n' + ' - entity_types: ' + types \
          #    + '\n' + ' - description: ' + desc \
           #   + '\n' + ' - detailed_description: ' + detail_desc \
            #  + '\n' + ' - identifier: ' + mid \
             # + '\n' + ' - url: ' + url \
              #+ '\n' + ' - resultScore: ' + score \
              #+ '\n')
        print(element['result']['name'] \
              + '\n' + ' - resultScore: ' + score \
			  + '\n' + ' - description: ' + desc \
              + '\n')



if __name__ == '__main__':
    """parser = argparse.ArgumentParser()
    parser.add_argument('query', help='The search term to query')
    args = parser.parse_args()
    main(args.query)"""
    #print (sys.argv[1])
    main(sys.argv[1])
    #main("Artificial Intelligence")