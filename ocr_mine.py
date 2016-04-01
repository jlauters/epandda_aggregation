import requests
import json
import re
import unidecode
from pymongo import MongoClient

config = json.load(open('./config.json'))


# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client.test

pbdb_titles = []

state    = "colorado"
locality = "florissant"
order    = "coleoptera"

bhl_base = "http://www.biodiversitylibrary.org/api2/httpquery.ashx"
bhl_key = config.bhl_key 

pbdb = requests.get('https://paleobiodb.org/data1.2/taxa/refs.json?base_name=' + order + '&textresult')
if 200 == pbdb.status_code:

  pbdb_json = json.loads( pbdb.content )
  for pb in pbdb_json['records']:

    if pb.has_key("tit"):

      if state in pb['tit'].lower() and locality in pb['tit'].lower():
        print "[" + pb['oid'] + "] Publication: " + pb['pbt']
        print "[" + pb['oid'] + "] Article Title: " + pb['tit'] + " matches search terms" 
        print "[" + pb['oid'] + "] Author: " + pb['al1']
        print "[" + pb['oid'] + "] Year: " + pb['pby']

        print "https://paleobiodb.org/data1.1/refs/single.json?id=" + pb['oid'].replace('ref:', '') + "&show=both"

        # Hardcoded List of Families from BHL 
        families = []
        if pb['oid'].replace('ref:', '') == "5139":
          families.append("Carabidae")
          families.append("Dytiscidae")
          families.append("Hydrophilidae")
          families.append("Silphidae")
          families.append("Staphylinidae")
          families.append("Coccinellidae")
          families.append("Erotylidae")
          families.append("Cucujidae")
          families.append("Dermestidae")
          families.append("Cryptophagidae")
          families.append("Nitidulidae")
          families.append("Trogositidae")
          families.append("Byrrhidae")
          families.append("Parnidae")
          families.append("Elateridae")
          families.append("Buprestidae")
          families.append("Lampyridae")
          families.append("Ptinidae")
          families.append("Scarabaeidae")
          families.append("Cerambyciade")
          families.append("Chrysomelidae")
          families.append("Bruchidae")
          families.append("Tenebrionidae")
          families.append("Cistelidae")
          families.append("Meloidea")
          families.append("Rhipiphoridae")


          bhl = requests.get(bhl_base + "?op=TitleSearchSimple&title=" + pb['pbt'] + "&apikey=" + bhl_key + "&format=json")
          if 200 == bhl.status_code:
            bhl_json = json.loads( bhl.content )

            for bhl_title in bhl_json['Result']:
              if pb['pbt'] in bhl_title['FullTitle']:

                title_items = requests.get(bhl_base + "?op=GetTitleItems&titleid=" + str( bhl_title['TitleID'] ) + "&apikey=" + bhl_key + "&format=json")
                if 200 == title_items.status_code:
                  items_json = json.loads( title_items.content )
         
                  for item in items_json['Result']:
                    if "v." + pb['vol'] + " (" + pb['pby'] + ")" in item['Volume']:
                      print "Volume match, get item metadata for " + str(item['ItemID'])

                      params = "&pages=t&parts=t&ocr=t&apikey=" + bhl_key + "&format=json"
                      meta_items = requests.get(bhl_base + "?op=GetItemMetadata&itemid=" + str(item['ItemID']) + params)
                      if 200 == meta_items.status_code:
                        meta_json = json.loads( meta_items.content )

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
