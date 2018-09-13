import logging

from datamodel.search.ShijinlKye7JiehuizHongxins_datamodel import ShijinlKye7JiehuizHongxinsLink, OneShijinlKye7JiehuizHongxinsUnProcessedLink, add_server_copy, get_downloaded_content
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, ServerTriggers
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4
import urllib2
import lxml
from bs4 import BeautifulSoup
from urlparse import urljoin

from urlparse import urlparse, parse_qs
from uuid import uuid4

import tldextract
import globalinit as gb


logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

@Producer(ShijinlKye7JiehuizHongxinsLink)
@GetterSetter(OneShijinlKye7JiehuizHongxinsUnProcessedLink)
@ServerTriggers(add_server_copy, get_downloaded_content)
class CrawlerFrame(IApplication):




    def __init__(self, frame):
        gb._init()
        self.starttime = time()
        self.app_id = "ShijinlKye7JiehuizHongxins"
        self.frame = frame


    def initialize(self):
        self.count = 0
        l = ShijinlKye7JiehuizHongxinsLink("http://www.ics.uci.edu/")
        print l.full_url
        self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get(OneShijinlKye7JiehuizHongxinsUnProcessedLink)

        if unprocessed_links:
            link = unprocessed_links[0]
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(ShijinlKye7JiehuizHongxinsLink(l))
            with open("frontier_summary.txt", "a") as f:
                f.write("Now the number of bad links is: ")
                f.write("%d\n" % (gb.getcounter()))
                f.write("Now the page with most links out is: ")
                f.write("%s\n" % (gb.getmaxlink()))


    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")



# We track the number of bad links, the page with most links out and the subdomain pages dynamicly, you can find the information at frontier_summary.txt

def extract_next_links(rawDataObj):
    outputLinks = []
    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.
    
    Suggested library: lxml
    '''
    f = None
    try:  # open with try
        f = urllib2.urlopen(rawDataObj.url.encode('utf-8'))
    except urllib2.HTTPError and urllib2.URLError and Exception:
        print "Got a bad link!"  # check the return code
        gb.setcounter(gb.getcounter()+1)
        return ["bad link"]


    htmlsource = f.read()
    baseurl = rawDataObj.url
    soup = BeautifulSoup(htmlsource, 'lxml')

    for item in soup.find_all('a', href=True):
        # print "###:"+ str(type(item))+"content:"+str(item)
        l=urljoin(baseurl, item['href'])
        print l
        outputLinks.append(l)

    if(len(outputLinks)>gb.getmaxlinknum()):
       gb.setmaxlink(rawDataObj.url)
    ext = tldextract.extract(baseurl)
    if ext.domain == "uci":
        difflinknum = set(outputLinks)
        gb.setsubdomainnum(baseurl,len(difflinknum))

    else:
        gb.setsubdomainnum(baseurl,0)

    with open("frontier_summary.txt", "a") as f:
        f.write("If the number isn't 0, then it's the number of links from this subdomain :%d\n"%(gb.getsubdomainnum(baseurl)))



    return outputLinks


    # f = urllib2.urlopen(rawDataObj.url)
    # htmlsource = f.read()
    # baseurl = rawDataObj.url
    # soup = BeautifulSoup(htmlsource, 'lxml')
    #
    # for item in soup:
    #     for link in item.find_all('a'):
    #         # avoid empty
    #         if link:
    #             # u
    #
    #             l = urljoin(baseurl, link.get('href'))
    #             print l
    #             outputLinks.append(l)
    #         else: continue
    #
    # return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse(url)
    path = parsed.path
    if parsed.scheme not in set(["http", "https"]):
        return False
    if not (path.__contains__('.php') or path.__contains__('.html') or path.__contains__('.xml')):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(calendar|css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False