import urllib2
import json

WANIKANI_DOMAIN = 'www.wanikani.com'


class Wanikani(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def __getattr__(self, item):
        def wrapper(arg=None):
            path = "http://{domain}/api/user/{api_key}/{resource}".format(
                domain=WANIKANI_DOMAIN,
                api_key=self.api_key,
                resource=item)

            if arg:
                path = "{path}/{arg}".format(path, arg)

            return json.loads(urllib2.urlopen(path).read())


        return wrapper



