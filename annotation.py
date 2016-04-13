# ePANDDA Open Annotation Implementation
#
# @author: Jon Lauters
#
# Simple function to fascilitate construction of annotations for ePANDDA and iDigBio Consumption

import json
import time
import datetime
import uuid

def create(target, body):

  # Timestamp and annotation uuid
  anno_uuid = uuid.uuid4()
  datestamp = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S %Z')

  target_uuid = str(target['uuid'])

  # TODO: Check if body has doi
  # TODO: Allow for body to pass in annotator?
  # TODO: Determine if we need to also push this into a mongoDB? Maybe a flag on the constructor?

  open_annotation = {}
  open_annotation['@context'] = "http://www.w3.org/ns/oa-context-20130208.json" 
  open_annotation['@id'] = str(anno_uuid)
  open_annotation['@type'] = "oa:Annotation"
  open_annotation['annotatedAt'] = str(datestamp)
  open_annotation['annotatedBy'] = {
    "@id": "ePANNDA Annotation Service ID", 
    "@type": "foaf:Person",
    "mbox": { "@id": "mailto:annotation@epandda.org" },
    "name": "ePANDDA Annotation Bot"
  }
 
  open_annotation['hasBody'] = {
    "@id": body['doi'],
    "@type": ["dwc:Occurrence", "dctype:Text"],
    "chars": body['title']
  }

  open_annotation['hasTarget'] = {
    "@id": "urn:uuid:" + target_uuid,
    "@type": "oa:SpecificResource",
    "hasSource": { "@id" : "http://search.idigbio.org/v2/view/records/" + target_uuid }
  }

  return open_annotation
