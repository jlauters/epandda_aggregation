# Script to perform a variety of NLP / Fuzzy Matching String 
# actions to determine what's in the OCR and attempt to break
# into articles. 

from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
import json, requests

# Init idigBio specimen fields
import scoring 

vectorizer = CountVectorizer()
client = MongoClient("mongodb://localhost:27017")
db = client.test

# Get All OCR
records = db.pbdb_ocr.find()
#records = db.pbdb_ocr.find_one()

# Get iDigBio Records
def getSpecimens():
  idigbio = requests.get('https://search.idigbio.org/v2/search/records/?rq={"order":"cetacea"}')
  if 200 == idigbio.status_code:
    idigbio_json = json.loads( idigbio.content )

    return idigbio_json['items']

items = getSpecimens()
for item in items:
  specimen = scoring.init_fields(item['data'])

  # TF / IDF between iDigBio Specimen and OCR Text Body

  # Train Set should include "matchable" darwin core
  train_set = [
    specimen['sciNameAuth'],
    specimen['sciNameAuthDate'],
    specimen['identRemarks'],
    specimen['biblioCitation'],
    specimen['occurrenceRemark'],
    specimen['associatedRef'],
    specimen['identBy'],
    specimen['recordedBy'],
    specimen['eventDate'],
    specimen['scientificName'],
    specimen['order'],
    specimen['stateProvince'],
    specimen['locality']
  ]

  # Test Set - OCR Documents ( currently Journals, hopefully someday articles ) 
  test_set = []
  for record in records:
    print "[" + record['oid'] + "] Title: " + record['title']
    test_set.append( record['ocr_text'] )

  vectorizer.fit_transform(train_set)

  print "Vocabulary: "
  print vectorizer.vocabulary

  smatrix = vectorizer.transform(test_set)
  print "smatrixline: "
  print smatrix

