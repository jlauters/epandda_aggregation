# Script to perform a variety of NLP / Fuzzy Matching String 
# actions to determine what's in the OCR and attempt to break
# into articles. 

from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json, requests

# Init idigBio specimen fields
import scoring 

vectorizer = CountVectorizer()
client = MongoClient("mongodb://localhost:27017")
db = client.test

# Get All OCR
#records = db.pbdb_ocr.find({"found_by": "coleoptera"})
records = db.pbdb_ocr.find({"oid":"5172"})
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

#items = getSpecimens()
items = getSpecimen()

train_set = []
#for item in items:
#  specimen = scoring.init_fields(item['data'])
#  values = specimen.values()
#  train_set.append( " ".join(values) )

  # TF / IDF between iDigBio Specimen and OCR Text Body

# Test Set - OCR Documents ( currently Journals, hopefully someday articles ) 
test_set = []
for record in records:
  print "[" + record['oid'] + "] Title: " + record['title']
  test_set.append( record['ocr_text'] )

  for item in items:
    print "Specimen ID: " + str(item['uuid'])
    specimen = scoring.init_fields( item['data'] )
    values = specimen.values()
   
    for val in values:
      train_set.append(val)


    vectorizer.fit(train_set)
    #print "Vocabulary length: "
    #print len(vectorizer.vocabulary_)

    print "Vocabulary: "
    print vectorizer.vocabulary_

    bow = vectorizer.transform(train_set)
    print "BOW:"
    print bow
    print "BOW Shape:"
    print bow.shape

    smatrix = vectorizer.transform(test_set)

    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(smatrix)
    print "IDF: ", tfidf.idf_

    print "Term Breakdown: "
    for key, value in specimen.iteritems():
      if value in vectorizer.vocabulary_:
         print key + " - " + value + " - " + str(tfidf.idf_[vectorizer.vocabulary_[value]])

    print "\n"
  print " ==== End Record ==== \n\n"

