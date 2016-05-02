# Script to perform a variety of NLP / Fuzzy Matching String 
# actions to determine what's in the OCR and attempt to break
# into articles. 

from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json, requests
import string
import editdistance

# Init idigBio specimen fields
import scoring 

def normalize(s):
  for p in string.punctuation:
    if "-" == p:
      s = s.replace(p, ' ')
    else:
      s = s.replace(p, '')

  return s.lower().strip()

vectorizer = CountVectorizer()
client = MongoClient("mongodb://localhost:27017")
db = client.test

# Get All OCR
records = db.pbdb_ocr.find({"found_by": "coleoptera"})
#records = db.pbdb_ocr.find({"oid":"5172"})
#records = db.pbdb_ocr.find_one()

def getSpecimen():
  idigbio = requests.get('http://search.idigbio.org/v2/view/records/c32288e2-cfba-447e-8491-5b82288a51f2')
  if 200 == idigbio.status_code:
    idigbio_json = json.loads( idigbio.content )

    ret = []
    ret.append( idigbio_json )
    return ret


# Get iDigBio Records
def getSpecimens():
  idigbio = requests.get('https://search.idigbio.org/v2/search/records/?rq={"order":"coleoptera","stateprovince": "colorado"}')
  if 200 == idigbio.status_code:
    idigbio_json = json.loads( idigbio.content )

    return idigbio_json['items']

items = getSpecimens()
#items = getSpecimen()

# Test Set - OCR Documents ( currently Journals, hopefully someday articles ) 
train_set = []
test_set = []
for record in records:
  print "[" + record['oid'] + "] Title: " + record['title']
  train_set.append( record['ocr_text'] )
  test_set.append( record['ocr_text'] )

  #for item in items:
  #  print "Specimen ID: " + str(item['uuid'])
  #  specimen = scoring.init_fields( item['data'] )
  #  values = specimen.values()
   
  #  for val in values:
  #    train_set.append(val)


  vectorizer.fit(train_set)
  #print "Vocabulary length: "
  #print len(vectorizer.vocabulary_)

  #print "Vocabulary: "
  #print vectorizer.vocabulary_

  for test in test_set:
    bow = vectorizer.transform(test)
    #print "BOW:"
    #print bow
    #print "BOW Shape:"
    #print bow.shape

    smatrix = vectorizer.transform(test)

    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(smatrix)
    print "IDF: ", tfidf.idf_

    for item in items:
      specimen = scoring.init_fields(item['data'])

      spec_count = len( specimen )
      term_match = 0
      matched_on = []

      print "Term Breakdown for specimen (" + str(item['uuid']) + "): "
      for term in vectorizer.vocabulary_:

        for key, value in specimen.iteritems():

          clean_term  = normalize(term)
          clean_value = normalize(value)
          dist = editdistance.eval(clean_term, clean_value)

          if term == value or dist < 5:
            term_match += 1
            if key not in matched_on:
              matched_on.append( key )

    if term_match >= 10:
      print "Specimen matches!"
      print ", ".join(matched_on)

      result = db.epandda_match.insert_one({"oid": record['oid'], "uuid": item['uuid']})
