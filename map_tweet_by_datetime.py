# -*- coding: utf-8 -*-

import sys
import couchdb
from couchdb.design import ViewDefinition
import json
from pa_setting import dbname

server = couchdb.Server('http://localhost:5984')
db = server[dbname]

def dateTimeToDocMapper(doc):
  from dateutil.parser import parse
  from datetime import datetime as dt
  if doc.get('created_at'):
    # [year, month, day, hour, min, sec]
    _date = list(dt.timetuple(parse(doc['created_at']))[:-3])  
    yield (_date, doc)

view = ViewDefinition('index', 'by_date_time', dateTimeToDocMapper, language='python')
view.sync(db)
