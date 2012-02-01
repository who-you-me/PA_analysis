# -*- coding: utf-8 -*-

import sys
import couchdb
from couchdb.design import ViewDefinition
import json
from pa_setting import dbname

server = couchdb.Server('http://localhost:5984')
db = server[dbname]

def retweetCountToDocMapper(doc):
  if doc.get('retweet_count'):
    _count = int(doc['retweet_count'])  
    yield (_count, doc)

view = ViewDefinition('index', 'by_retweet_count', retweetCountToDocMapper, language='python')
view.sync(db)
