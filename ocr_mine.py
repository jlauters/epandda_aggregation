# OCR Miner
#
# @author: Jon Lauters
#
# Script to query PBDB and BHL API's to match PBDB Biblio Reference Records to BHL OCR Text.
# Found OCR Text is stored in a MongoDB collection called `pbdb_ocr`

import requests
import json
import re
import unidecode
import string
import editdistance
from pymongo import MongoClient

# Config to load BHL API Key
config = json.load(open('./config.json'))

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client.test

# Next time search for coleoptera

# Variable inits
pbdb_titles = []
insert_count = 0
base_name    = "coleoptera"
bhl_base = "http://www.biodiversitylibrary.org/api2/httpquery.ashx"
bhl_key = config['bhl_key'] 

#====== Util Functions ==========

def normalize(s):
  for p in string.punctuation:
    if "-" == p:
      s = s.replace(p, ' ')
    else:
      s = s.replace(p, '')

  return s.lower().strip()

def badPBDB( oid ):
  insert_oid = oid.replace('ref:', '')
  result = db.bad_pbdb.insert_one({"oid": insert_oid})

def cleanBadPBDB( pbdb ):
  cleaned = []
  bad = db.bad_pbdb.find()

  for pb in pbdb:
    if pb['oid'] not in bad:
      cleaned.append(pb)

  return cleaned

# ====== End Util Functions =====

# Step One - Get Bib References from PBDB for order
def getPubs( base_name ):
  pbdb = requests.get('https://paleobiodb.org/data1.2/taxa/refs.json?base_name=' + base_name)
  if 200 == pbdb.status_code:
    pbdb_json = json.loads( pbdb.content )
 
    cleaned = cleanBadPBDB(pbdb_json['records'])   

    pbdb_count = len(cleaned)
    print "Returned " + str(pbdb_count) + " records from PBDB"

    return cleaned

# Step Two - Check if Publication is found in BHL
def searchTitle( title, key ):
  bhl = requests.get(bhl_base + "?op=TitleSearchSimple&title=" + title + "&apikey=" + key + "&format=json")
  if 200 == bhl.status_code:
    bhl_json = json.loads( bhl.content )

    bhl_title_count = len(bhl_json['Result'])
    print "Returned " + str(bhl_title_count) + " titles from BHL"

    return bhl_json['Result']

# Step Three - Get title items for matched publication title
def searchTitleItems( title_id, key ):
  title_items = requests.get(bhl_base + "?op=GetTitleItems&titleid=" + str( title_id ) + "&apikey=" + key + "&format=json")
  if 200 == title_items.status_code:
    items_json = json.loads( title_items.content )

    items_count = len(items_json['Result'])
    print "Returned " + str(items_count) + " items from BHL"

    return items_json['Result']

# Step Four - If we found the same volume, get the metadata for that Title Item ( includes pages with OCR Text )
def searchMetadata( item_id, key ):

  params = "&pages=t&parts=t&ocr=t&apikey=" + key + "&format=json"
  meta_items = requests.get(bhl_base + "?op=GetItemMetadata&itemid=" + str(item_id) + params)
  if 200 == meta_items.status_code:
    meta_json = json.loads( meta_items.content )

    meta_count = len(meta_json['Result'])
    print "Returned " + str(meta_count) + " meta from BHL"

    return meta_json['Result']

def scanPage( ocr ):

  if ocr is not None:

    stripped_full = repr( ocr.strip() )
    stripped_full = re.sub(ur"\\n", "", stripped_full)

    return stripped_full

#===================================
#          script start
#=========+=========================

pubs = getPubs(base_name)
for pb in pubs:

  # PBDB Data Objects do not have a consistent return format.
  # Check if PBDB knows the DOI
  doi = pb['doi'] if 'doi' in pb else ""

  # Checking if record has journal title and publication title before making BHL API Call
  if "tit" not in pb or "pbt" not in pb:
      badPBDB(pb['oid'])
  else:

    bhl_titles = searchTitle( pb['pbt'], bhl_key )
    for bhl_title in bhl_titles:

      # Normalize titles, calculate Lev Distance as a second check
      pb_title = normalize(pb['pbt'])
      bhl_full = normalize(bhl_title['FullTitle'])
      dist = editdistance.eval(pb_title, bhl_full)

      if pb_title != bhl_full and dist > 10:
        # Are we missing silly spelling issues -- Yes, Yes we are
        print "PBT: " + pb_title 
        print "BHL Full: " + bhl_full
        print "Lev dist: " + str(dist)

      else:

        # We think these are a match, persue further for article title matching.
        title_items = searchTitleItems( bhl_title['TitleID'], bhl_key )
        for item in title_items:

          # Check if Volume is of type v.xx (yyyy) or just year
          pb_vol = pb['vol'] if 'vol' in pb else ""
          pby = pb['pby'] if 'pby' in pb else ""
          bhl_vol = item['Volume'].replace(" ", "")
          vol_pattern = "v." + pb_vol + "(" + pby + ")"
          year_auth_pattern = pb['al1'] + "." + pby

          if vol_pattern not in bhl_vol and year_auth_pattern not in bhl_vol and pby not in bhl_vol:

            print "ITEMS DONT Match!!!!"
            print "vol pattern: " + vol_pattern + pb['al1']
            print "BHL volume: " + item['Volume']

          else:
            print "Volume match, get item metadata for " + str(item['ItemID'])

            meta = searchMetadata( item['ItemID'], bhl_key)          
            external_url = meta['ExternalUrl']

            if doi is None and external_url is not None:
              doi = external_url

            # Step Five - Iterate through the returned Pages for title item.
            # If page OCR has sufficient content clean it up and look for article title. 
            # If article title is found, stuff all OCR Text into a MongoDB document in the pbdb_ocr collection.

            # TODO: How to improve this? PBDB OID -> Journal OCR is not the best relation to store, but hard to get just article text? 

            add_to_db = False
            ocr_blob = ""
            for page in meta['Pages']:

              stripped = scanPage(page['OcrText'])
              if stripped is not None:
                ocr_blob += "\n" + stripped

                if pb['tit'][5:20].lower() in stripped.lower():
                  print "Found PBDB Title in OCR!!!!!!!"
                  add_to_db = True

            if add_to_db:
              insert_count += 1
              print "Added " + str(insert_count) + " Ocr to MongoDB"

              insert_oid = pb['oid'].replace('ref:', '')
              if "39330" is insert_oid:
                doi = "http://dx.doi.org/10.1155/1917/83242"

              result = db.pbdb_ocr.insert_one({"oid": insert_oid, "title": pb['tit'], "found_by": base_name, "doi": doi,  "ocr_text": ocr_blob})
