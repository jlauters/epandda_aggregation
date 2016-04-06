# Specimen Match
#
# @author: Jon Lauters
#
# Script to query iDigBio API and perform an array of string matching operations against OCR Text in `pbdb_ocr` collection

import requests
import json
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client.test
ocr = db.pbdb_ocr.find()

# Variable inits
matches = []
order = "coleoptera"
locality = "florissant"
stateprov = "colorado"
idig_base = 'https://search.idigbio.org/v2/search/records/'

# Step One - Get iDigBio Data 
idigbio = requests.get(idig_base + '?rq={"scientificname":"' + order + '","stateprovince":"' + stateprov + '","locality":"' + locality + '"}')
if 200 == idigbio.status_code:

  idigbio_json = json.loads( idigbio.content )
  for idig in idigbio_json['items']:

    # Prep iDigBio fields for matching - iDigBio return object is not consistent. 
    sciNameAuth = ""
    sciNameAuthDate = ""
    if "dwc:scientificNameAuthorship" in idig['data']:
      sciNameAuth = idig['data']['dwc:scientificNameAuthorship'].lower()

      if ' ' in sciNameAuth:
        sciNameParts    = sciNameAuth.split()
        sciNameAuth     = sciNameParts[0]
        sciNameAuthDate = sciNameParts[1]

    identRemarks = ""
    if "dwc:identificationRemarks" in idig['data']:
      identRemarks = idig['data']['dwc:identificationRemarks'].lower()

    biblioCitation = ""
    if "dcterms:bibliographicCitation'" in idig['data']:
      biblioCitation   = idig['data']['dcterms:bibliographicCitation'].lower()

    occurrenceRemark = ""
    if "dwc:occurrenceRemarks" in idig['data']:
      occurrenceRemark = idig['data']['dwc:occurrenceRemarks'].lower()

    associatedRef = ""
    if "dwc:associatedReferences" in idig['data']:
      associatedRef = idig['data']['dwc:associatedReferences'].lower()

    identRef = ""
    if "dwc:identificationReferences" in idig['data']:
      identRef = idig['data']['dwc:identificationReferences'].lower()

    recordedBy = ""
    if "dwc:recordedBy" in idig['data']:
      recordedBy = idig['data']['dwc:recordedBy'].lower()

    eventDate = ""
    if "dwc:eventDate" in idig['data']:
      eventDate = idig['data']['dwc:eventDate'].lower()

    scientificName = ""
    if "dwc:scientificName" in idig['data']:
      scientificName = idig['data']['dwc:scientificName'].lower()

    order = ""
    if "dwc:order" in idig['data']:
      order = idig['data']['dwc:order'].lower()

    stateProvince = ""
    if "dwc:stateProvince" in idig['data']:
      stateProvince = idig['data']['dwc:stateProvince'].lower()

    locality = ""
    if "dwc:locality" in idig['data']:
      locality = idig['data']['dwc:locality'].lower()

    # Begin scoring section
    for text in ocr:

      # for consistency
      ocr_text = text['ocr_text'].lower() 

      # init score keeping 
      score = 0
      matchedOn = []

      # Simple - all fields weighted the same

      if sciNameAuth in ocr_text:
        score += 1
        matchedOn.append(" Scientific Name Authorship")

      if identRemarks in ocr_text:
        score += 1
        matchedOn.append(" Identification Remarks")
  
      if recordedBy in ocr_text:
        score += 1
        matchedOn.append(" Recorded By")

      if biblioCitation in ocr_text:
        score += 1
        matchedOn.append(" Bibliographic Citation")

      if eventDate in ocr_text:
        score += 1
        matchedOn.append(" Event Date")

      if occurrenceRemark in ocr_text:
        score += 1
        matchedOn.append(" Occurrence Remarks")

      if associatedRef in ocr_text:
        score += 1
        matchedOn.append(" Associated References")

      if identRef in ocr_text:
        score += 1
        matchedOn.append(" Identification Remarks")

      if scientificName in ocr_text:
        score += 1
        matchedOn.append(" Scientific Name")

      if order in ocr_text:
        score += 1
        matchedOn.append(" Taxonomic Order")

      if stateProvince in ocr_text:
        score += 1
        matchedOn.append(" State/Province")

      if locality in ocr_text:
        score += 1
        matchedOn.append(" Locality")

      print "Score: " + str(score)
      print '[%s]' % ', '.join(map(str, matchedOn))

