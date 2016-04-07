# ePANDDA Open Annotation Implementation
#
# @author: Jon Lauters
#
# Simple class to fascilitate construction of annotations for ePANDDA and iDigBio Consumption
# 
# Constructor takes target and body JSON objects of iDigBio specimen and PBDB biblio reference ( with added fields for DOI, person ident etc ) 

import json
import time
import datetime
import uuid

class Annotation(object):

  def __init__(self, target, body):

    # Timestamp and annotation uuid
    uuid = uuid.uuid4()
    datestamp = datetime.datetime.fromtimestamp( time.gmtime() ).strftime('%Y-%m-%d %H:%M:%S %Z')

    # TODO: Check if body has doi
    # TODO: Allow for body to pass in annotator?
    # TODO: Determine if we need to also push this into a mongoDB? Maybe a flag on the constructor?

    return json.dumps({
      "@context": "http://www.w3.org/ns/oa-context-20130208.json",
      "@id": uuid,
      "@type": "oa:Annotation",
      "annotatedAt": datestamp,
      "annotatedBy": {
        "@id": "ePANNDA Annotation Service ID",
        "@type": "foaf:Person",
        "mbox": { "@id": "mailto:annotation@epandda.org" },
        "name": "ePANDDA Annotation Bot"
      },
      "hasBody": {
        "@id": body['doi'],
        "@type": ["dwc:Occurrence", "dctype:Text"],
        "chars": body['tit'],
      },
      "hasTarget": {
          "@id": "urn:uuid:" + target.uuid,
          "@type": "oa:SpecificResource",
          "hasSource": {
            "@id": "http://search.idigbio.org/v2/view/records/" + target.uuid
          }
      }
    })
