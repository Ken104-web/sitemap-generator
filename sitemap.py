import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib


class SitemapGenerator:

    def __init__(self, root, filename):
        self.filename = filename
        self.urls = {}
        self.root = root
        self.hostname = urlparse(root).hostname


    def crawl(self, url, level):
        print("Level: " + str(level) + "/Explore" + url)

        page = requests.get(url)

        if page.status_code == 200:
            url =  urllib.parse.urldefrag(url)[0] 

            if url not in self.urls:
                self.urls[url] = level

                soup = BeautifulSoup(page.content, "html.parser")

                # iterate to recover the contents of href attributes which corresponds to the page
                
                for link in soup.find_all('a'):
                    try:
                        href = link.get('href')
                        result = urlparse(href)
                        newurl = None

                        if result.hostname == None and href is not None:
                            # still the same domain
                            newurl = self.root + ("/", "")[href.startswith("/")] + href

                        elif result.hostname == self.hostname:
                            newurl = href

                        if newurl != None:
                            self.crawl(newurl, level + 1)

                    except TypeError:
                        print("Error for link:" + link.get('href'))
            else:
                if self.urls[url] > level:
                    self.urls[url] = level
        else:
            print(url + "unreachable")



                            
 

