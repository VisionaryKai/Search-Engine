import urllib2
import lxml
import bs4
from bs4 import BeautifulSoup
from urlparse import urljoin
from urllib2 import URLError



def a(baseurl):
    f = None
    try:  # need to open with try
        f = urllib2.urlopen(baseurl.encode('utf-8'))
    except urllib2.HTTPError and urllib2.URLError and Exception:
        print "yeah!"
        return  # check the return code
        # raise # if other than 404, raise the error

    htmlsource = f.read()

    soup = BeautifulSoup(htmlsource, 'lxml')

    for item in soup.find_all('a', href=True):
        # print "###:"+ str(type(item))+"content:"+str(item)
        print urljoin(baseurl, item['href'])



baseurl = "arXiv_Mjolsness_1212.0582.pdf"

a(baseurl)


# baseurl = "http://www.ics.uci.edu/"
#
# print type(baseurl.encode('utf-8'))
# print type(baseurl)
# a(baseurl)
# f = urllib2.urlopen(baseurl)

    # f = urllib2.urlopen(rawDataObj.url)
    # htmlsource = f.read()
    # baseurl = rawDataObj.url
    # soup = BeautifulSoup(htmlsource, 'lxml')
    #
    # for item in soup.find_all('a', href=True):
    #     # print "###:"+ str(type(item))+"content:"+str(item)
    #     l=urljoin(baseurl, item['href'])
    #     print l
    #     outputLinks.append(l)
    #
    # return outputLinks
