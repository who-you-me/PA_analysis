# -*- coding: utf-8 -*-

import sys
import oauth2
import json
import urllib
import couchdb
from pa_setting import ckey, csecret, atoken, asecret, dbname

server = couchdb.Server('http://localhost:5984')
db = server.create(dbname)

consumer = oauth2.Consumer(ckey, csecret)
token = oauth2.Token(atoken, asecret)
client = oauth2.Client(consumer, token)

url = 'http://api.twitter.com/1/statuses/user_timeline.json'
params = {'count': 200, 'trim_user': True, 'include_entities': True}

for i in range(1, 17):
  params['page'] = i
  print 'page %s:' % i,
  p = urllib.urlencode(params)
  
  while True:
    response = client.request(url + '?' + p, 'GET')
    status = response[0]['status']
    # status500番台はリトライ，400番台は終了
    if status == '200':
      break
    elif status[0] == '5':
      print 'retry',
    elif status[0] == '4':
      print 'invalid request'
      sys.exit()
    else:
      print 'unexpected status code: ' + status
      sys.exit()
  
  data = json.loads(response[1])
  if data:
    db.update(data, all_or_nothing=True)
    print '%s tweets' % len(data)
  else:
    print 'end'
    break