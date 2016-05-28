import base64
import json
import os
import pickle
import urllib2


# Pending

def extract_data():
    username = 'amobile:uoPh1Ni4'
    password = ''

    request = urllib2.Request("https://kudago.com/export/whole/events.json")
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    data = json.loads(result.read())

    path = os.path.dirname(os.path.abspath(__file__)) + "/data/"
    path += 'events.pkl'
    pickle.dump(data, open(path, 'w'))

    # extract_data()
