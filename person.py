# Person Matching
#
# @author
#
# Look up a Person by last name ( optional location or taxon name parameters ) and return data associated with that person.

import requests
import json

order     = "coleoptera"
person    = "scudder"
idig_base = "https://search.idigbio.org/v2/search/records/?rq="

# Step One - Query iDigBio
idigbio = requests.get(idig_base + '{"order": ' + order + ', "collector":' + person + '}')
if 200 == idigbio.status_code:

  idigbio_json = json.loads( idigbio.content )
  print "iDigBio has " + idigbio_json['itemCount'] + " specimens collected by " + person

# Step Two - Query PBDB
pbdb = aggregatePBDB()








# This is going to be slightly more complicated. PBDB doesn't have a top level search by name functionality,
# so unless context is given ( occurrence, stratigraphy, bibliography ) search all of them and compile a complete PBDB list by name
def aggregatePBDB():

  data = []

  pbdb_occur_author = requests.get('https://paleobiodb.org/data1.2/occs/list.json?base_name=' + order + '&ref_author=' + person)
  if 200 == pbdb_occur_author.status_code:

    pbdb_occur_author = json.loads( pbdb_occur_author.content )
    data.append( pbdb_occur_author['records'] )

  # This doesn't work PBDB has an error in 1.2 occ/refs API ref_author was not supported in 1.1
  pbdb_refs_author = requests.get('https://paleobiodb.org/data1.2/occs/refs.json?base_name=' + order + '&ref_author=' + person + '&textresult')
  if 200 == pbdb_refs_author.status_code:

    pbdb_refs_author = json.loads( pbdb_refs_author.content )
    data.append( pbdb_refs_author['records'] )

  return data
