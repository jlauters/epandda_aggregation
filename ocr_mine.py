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
from pymongo import MongoClient

# Config to load BHL API Key
config = json.load(open('./config.json'))

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client.test

# Variable inits
pbdb_titles = []
order    = "coleoptera"
bhl_base = "http://www.biodiversitylibrary.org/api2/httpquery.ashx"
bhl_key = config['bhl_key'] 

# Step One - Get Bib References from PBDB for order
pbdb = requests.get('https://paleobiodb.org/data1.2/taxa/refs.json?base_name=' + order + '&textresult')
if 200 == pbdb.status_code:

  pbdb_json = json.loads( pbdb.content )
  for pb in pbdb_json['records']:

    # PBDB Data Objects do not have a consistent return format.
    # Checking if record has journal title and publication title before making BHL API Call
    if pb.has_key("tit") and pb.has_key("pbt"):

          # Step Two - Check if Publication is found in BHL
          bhl = requests.get(bhl_base + "?op=TitleSearchSimple&title=" + pb['pbt'] + "&apikey=" + bhl_key + "&format=json")
          if 200 == bhl.status_code:
            bhl_json = json.loads( bhl.content )

            for bhl_title in bhl_json['Result']:
              if pb['pbt'] in bhl_title['FullTitle']:

                # Step Three - Get title items for matched publication title
                title_items = requests.get(bhl_base + "?op=GetTitleItems&titleid=" + str( bhl_title['TitleID'] ) + "&apikey=" + bhl_key + "&format=json")
                if 200 == title_items.status_code:
                  items_json = json.loads( title_items.content )
         
                  for item in items_json['Result']:
                    if "v." + pb['vol'] + " (" + pb['pby'] + ")" in item['Volume']:
                      print "Volume match, get item metadata for " + str(item['ItemID'])

                      # Step Four - If we found the same volume, get the metadata for that Title Item ( includes pages with OCR Text )
                      params = "&pages=t&parts=t&ocr=t&apikey=" + bhl_key + "&format=json"
                      meta_items = requests.get(bhl_base + "?op=GetItemMetadata&itemid=" + str(item['ItemID']) + params)
                      if 200 == meta_items.status_code:
                        meta_json = json.loads( meta_items.content )



                        # Step Five - Iterate through the returned Pages for title item.
                        # If page OCR has sufficient content clean it up and look for article title. 
                        # If article title is found, stuff all OCR Text into a MongoDB document in the pbdb_ocr collection.

                        add_to_db = False
                        ocr_blob = ""
                        for page in meta_json['Result']['Pages']:
                          if page['OcrText'] and page['OcrText'] is not None:

                            stripped = repr( page['OcrText'][:800].strip() )
                            stripped = re.sub(ur"\\n", "", stripped)

                            stripped_full = repr( page['OcrText'].strip() )
                            stripped_full = re.sub(ur"\\n", "", stripped_full)

                            ocr_blob += "\n" + stripped_full

                            if stripped is not None:
                              print "Found OCR"

                              if pb['tit'][:20].lower() in stripped.lower():
                                print "Found PBDB Title in OCR!!!!!!!"
                                add_to_db = True

                        if add_to_db:
                           print "Added Ocr to MongoDB"
                           insert_oid = pb['oid'].replace('ref:', '')
                           result = db.pbdb_ocr.insert_one({"oid": insert_oid, "ocr_text": ocr_blob})
