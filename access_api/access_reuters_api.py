import urllib.request
import urllib
import urllib.parse
import requests
from lxml import etree
from PIL import Image



USERNAME = "Hack-API+3"
PASSWORD = "hJPfKPafRQoWiMX"
AUTH_URL = "https://commerce.reuters.com/rmd/rest/xml/"
SERVICE_URL = "http://rmb.reuters.com/rmd/rest/xml/"
TOKEN = '3SDnXO+c5NfW+TGfzyKVhKfE3xRhYxnD81kIX5wuiTI'

IMAGE_LIST= []



class ReutersDatasource:
    def __init__(self, username=USERNAME, password=PASSWORD):
        self.authToken = None
        print("Getting auth token")
        # get a new auth token every time, expires after a week
        tree = self._call('login', {'username': username, 'password': password}, True)
        if tree.tag == 'authToken':
            self.authToken = tree.text
        else:
            raise Exception('unable to obtain authToken')

    def _call(self, method, args={}, auth=False):
        if auth:
            root_url = AUTH_URL
        else:
            root_url = SERVICE_URL
            print("self.authToken: ", self.authToken)
            args['token'] = self.authToken
        return self.base_call(method, root_url, args)

    def base_call(self, method, root_url, args={}):
        url = root_url + method + '?' + urllib.parse.urlencode(args)
        resp = urllib.request.urlopen(url, timeout=10)
        rawd = resp.read()
        print(rawd)
        parsed = etree.fromstring(rawd)
        return etree.fromstring(rawd)

    def authenticate_url(self, url):
        authUrl = url + "?token=" + self.authToken
        return authUrl

    def call(self, method, args={}):
        return self._call(method, args, False)

    def open_Image(self, url):
        authUrl = self.authenticate_url(url)
        print("URL:", authUrl, sep='')
        if not authUrl in IMAGE_LIST:
            im = Image.open(requests.get(authUrl, stream=True).raw)
            im.show()
            IMAGE_LIST.append(authUrl)




ReutersDatasource().__init__(username=USERNAME, password=PASSWORD)
ReutersDatasource()._call('GET', {'username':USERNAME, 'password':PASSWORD})
#ReutersDatasource()._call(username=USERNAME, password=PASSWORD)


#def _call(self, method, args={}, auth=False):
ReutersDatasource().base_call(method, root_url, args={})
