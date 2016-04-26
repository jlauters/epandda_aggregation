# Scoring Module
#
# @author: Jon Lauters
#
# Scoring functions to implement different scoring algorithms

import annotation

def init_fields(specimen):

  ret = {}
  
  ret['sciNameAuth'] = ""
  ret['sciNameAuthDate'] = ""
  ret['specificEpithet'] = ""
  ret['identRemarks'] = ""
  ret['biblioCitation'] = ""
  ret['occurrenceRemark'] = ""
  ret['associatedRef'] = ""
  ret['identBy'] = ""
  ret['identRef'] = ""
  ret['recordedBy'] = ""
  ret['eventDate'] = ""
  ret['dateItentified'] = ""
  ret['scientificName'] = ""
  ret['order'] = ""
  ret['stateProvince'] = ""
  ret['locality'] = ""
  ret['formation'] = ""

  if "dwc:scientificNameAuthorship" in specimen:
    ret['sciNameAuth'] = specimen['dwc:scientificNameAuthorship'].lower()
  
    if ' ' in ret['sciNameAuth']:
      sciNameParts = ret['sciNameAuth'].split()
      ret['sciNameAuth']     = sciNameParts[0]
      ret['scinameAuthDate'] = sciNameParts[1]

  if "dwc:identificationRemarks" in specimen:
    ret['identRemarks'] = specimen['dwc:identificationRemarks'].lower()

  if "dcterms:bibliographicCitation" in specimen:
    ret['biblioCitation'] = specimen['dcterms:bibliographicCitation'].lower()

  if "dwc:occurrenceRemarks" in specimen:
    ret['occurrenceRemark'] = specimen['dwc:occurrenceRemarks'].lower()

  if "dwc:associatedReferences" in specimen:
    ret['associatedRef'] = specimen['dwc:associatedReferences'].lower()

  if "dwc:specificEpithet" in specimen:
    ret['specificEpithet'] = specimen['dwc:specificEpithet'].lower()

  if "dwc:identificationReferences" in specimen:
    ret['identRef'] = specimen['dwc:identificationReferences'].lower()

  if "dwc:recordedBy" in specimen:
    cleaned = specimen['dwc:recordedBy'].lower().split(',')
    ret['recordedBy'] = cleaned[0]

  if "dwc:identifiedBy" in specimen:
    cleaned = specimen['dwc:identifiedBy'].lower().split(',')
    ret['identBy'] = cleaned[0]

  if "dwc:eventDate" in specimen:
    ret['eventDate'] = specimen['dwc:eventDate'].lower()

  if "dwc:dateIdentified" in specimen:
    ret['dateItendified'] = specimen['dwc:dateIdentified'].lower()

  if "dwc:scientificName" in specimen:
    ret['scientificName'] = specimen['dwc:scientificName'].lower()

  if "dwc:order" in specimen:
    ret['order'] = specimen['dwc:order'].lower()

  if "dwc:stateProvince" in specimen:
    ret['stateProvince'] = specimen['dwc:stateProvince'].lower()

  if "dwc:locality" in specimen:
    ret['locality'] = specimen['dwc:locality'].lower()

  if "dwc:formation" in specimen:
    ret['formation'] = specimen['dwc:formation'].lower()

  return ret

def scorePubs(pbdb, idigbio, threshold):

  matches = []
  for idig in idigbio['items']:

    # Prep iDigBio fields for matching - these can be inconsistent
    specimen = init_fields( idig['data'] )
    
    # scoring section
    for obj in pbdb:

     score = 0
     matchedOn = []
     ocr = ""
     if obj['ocr_text'] is not None:
       ocr = obj['ocr_text'].lower()


     # TODO: This might go away in favor if TF/IDF
     # Simple flat weighted
     if specimen['sciNameAuth'] in ocr:
       score += 1
       matchedOn.append(" Scientific Name Authorship")

     if specimen['identRemarks'] in ocr:
       score += 1
       matchedOn.append(" Identification Remarks")

     if specimen['recordedBy'] in ocr:
       score += 1
       matchedOn.append(" Recorded by")

     if specimen['identBy'] in ocr:
       score += 1
       matchedOn.append(" Identified by")

     if specimen['biblioCitation'] in ocr:
       score += 1
       matchedOn.append(" Bibliographic Citation")

     if specimen['eventDate'] in ocr:
       score += 1
       matchedOn.append(" Event Date")

     if specimen['occurrenceRemark'] in ocr:
       score += 1
       matchedOn.append(" Occurrence Remarks")

     if specimen['associatedRef'] in ocr:
       score += 1
       matchedOn.append(" Associated References")

     if specimen['identRef'] in ocr:
       score += 1
       matchedOn.append(" Identification Remarks")
 
     if specimen['scientificName'] in ocr:
       score += 1
       matchedOn.append(" Scientific Name")

     if specimen['order'] in ocr:
       score += 1
       matchedOn.append(" Taxonomic Order")

     if specimen['stateProvince'] in ocr:
       score += 1
       matchedOn.append(" State/Province")

     if specimen['locality'] in ocr:
       score += 1
       matchedOn.append(" Locality")
 

     if threshold <= score:
    
       print specimen['scientificName'] + " matched "
       print '[%s]' % ', '.join(map(str, matchedOn))
      
       oa = annotation.create(idig, obj)
       matches.append(oa)

  return matches
