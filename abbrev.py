#!/usr/bin/env python2.7

import sys , ssl
import urllib2
from HTMLParser import HTMLParser

####################### SETTING ########################

if len(sys.argv) != 2:
    print "give me Only ONE parameter"
    quit()

word = sys.argv[1]

site = "https://www.allacronyms.com/" + word + "/abbreviated"

####################### ABBREV PAESER ##################
class abbParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.stopParse = False
        self.getDef = False
        self.getRank = False
        self.lastTag = ""
    def handle_starttag(self , tag , attrs):
        self.lastTag = tag
        if not self.stopParse:
            for(attr , value) in attrs:
                if attr == 'class' and value == 'pairDef':
                    self.getDef = True
                if attr == 'class' and value == 'n':
                    self.getRank = True
                if attr == 'title' and self.getRank == True:
                    print "Rank:" , "%3s " %value.split(' ')[0] ,
                    self.getRank = False
            if tag == "a" and self.getDef == True:
                for(attr , value) in attrs:
                    if attr == 'href':
                        if len(value.split('/')) > 1:
                            print "%-7s" %value.split('/')[1] , " " ,
                        if len(value.split('/')) > 2:
                            print "%-15s" %value.split('/')[2]
                        self.getDef = False
#######################    MAIN   ######################

if __name__ == '__main__':
    req = urllib2.Request(site)
    #sol 1
    context = ssl._create_unverified_context()
    response = urllib2.urlopen(req , context = context)

    #sol 2
    #ssl._create_default_https_context = ssl._create_unverified_context
    #response = urllib2.urlopen(req)

    page = response.read() #Get html file
    RSP = abbParser()
    RSP.feed(page)
