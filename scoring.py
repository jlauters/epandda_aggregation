# Scoring Module
#
# @author: Jon Lauters
#
# Scoring functions to implement different scoring algorithms

import annotation

def scorePubs(pbdb, idigbio, threshold):

  for idig in idigbio['items']:
  
    # Prep iDigBio fields for matching - these can be inconsistent
    sciNameAuth     = ""
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
    if "dcterms:bibliographicCitation" in idig['data']:
      biblioCitation = idig['data']['dcterms:bibliographicCitation'].lower()

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

    
    # scoring seciton
    for pb in pbdb:

     score = 0
     ocr = pb['ocr'].lower()
     matchedOn = []

     # Simple flat weighted
     if sciNameAuth in ocr:
       score += 1
       matchedOn.append(" Scientific Name Authorship")

     if identRemarks in ocr:
       score += 1
       matchedOn.append(" Identification Remarks")

     if recordedBy in ocr:
       score += 1
       matchedOn.append(" Recorded by")

     if biblioCitation in ocr:
       score += 1
       matchedOn.append(" Bibliographic Citation")

     if eventDate in ocr:
       score += 1
       matchedOn.append(" Event Date")

     if occurrenceRemark in ocr:
       score += 1
       matchedOn.append(" Occurrence Remarks")

     if associatedRef in ocr:
       score += 1
       matchedOn.append(" Associated References")

     if identRef in ocr:
       score += 1
       matchedOn.append(" Identification Remarks")
 
     if scientificName in ocr:
       score += 1
       matchedOn.append(" Scientific Name")

     if order in ocr:
       score += 1
       matchedOn.append(" Taxonomic Order")

     if stateProvince in ocr:
       score += 1
       matchedOn.append(" State/Province")

     if locality in ocr:
       score += 1
       matchedOn.append(" Locality")
 

     if threshold <= score:
    
       print scientificName + " matched " + pb['tit']
       print '[%s]' % ', '.join(map(str, matchedOn))
       # Send off to Make annotations of matches
      
       oa = annotation(idig, pb)
