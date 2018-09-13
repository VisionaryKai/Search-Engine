badcounter=0
maxlink=""
maxlinknum=0
subdomaindict={}
def _init():
    global maxlinknum
    global badcounter
    global maxlink
    global subdomaindict

def setcounter(counter):
    global badcounter
    badcounter=counter
def setmaxlink(link):
    global maxlink
    maxlink=link
def setmaxlinknum(linknum):
    global maxlinknum
    maxlinknum=linknum
def setsubdomainnum(url,num):
    global subdomaindict
    subdomaindict[url]=num
def getcounter():
    return badcounter
def getmaxlink():
    return maxlink
def getmaxlinknum():
    return maxlinknum
def getsubdomainnum(subdomain):
    return subdomaindict[subdomain]