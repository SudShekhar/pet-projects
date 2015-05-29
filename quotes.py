# Created by Sudhanshu Shekhar<SudShekhar>
# Purpose: A simple script to get daily quotes.
# Usage : `python quotes.py [category name]`  --> category name is optional
# I have added the above line to my .bashrc, so that I get the quote each time I start my terminal
# The script only gets 1 unique quote per day. To get a different quote you need to supply a category name.

import urllib2
import json
import sys
import os.path
from datetime import date

FILENAME = ".dailyQuote.txt"

def show_quote(quote):
    l = len(quote)
    print (l+4)*"="
    print "| "+l*" "+" |"
    print "| "+quote+" |"
    print "| "+l*" "+" |"
    print (l+4)*"="


def get_json(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
    except:
        show_quote("Internet doesn't seem to be working. Sorry")
        sys.exit(1)
    json_data = json.loads(html)
    return json_data

def save_to_file(text):
    f = open(FILENAME,"r")
    f.write(text)
    f.close()

def main():
    if(os.path.isfile(FILENAME)):
        f = open(FILENAME,"r")
        old_data = json.load(f)
        f.close()
    else:
        old_data = {}

    if (len(sys.argv)) > 1:
        category = sys.argv[1]
        url = "http://api.theysaidso.com/qod.json?category="+category
    else:
        if old_data != {}:
            if old_data['date'] == str(date.today()):
                show_quote(old_data['quotes'])
                sys.exit(0)
        url = "http://api.theysaidso.com/qod.json"
    d = {}
    try:
        json_data = get_json(url)
        d['quotes'] = json_data['contents']['quote']

    except:
        url = "http://quotesondesign.com/api/3.0/api-3.0.json"
        json_data = get_json(url)
        d['quotes'] = json_data['quote']

    show_quote(d['quotes'])
    d['date'] = str(date.today())
    json_data = json.dumps(d)
    f = open(FILENAME, "w")
    f.write(json_data)
    f.close()

if __name__ == "__main__":
    main()
