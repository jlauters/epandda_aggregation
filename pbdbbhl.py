# PBDB BHL Merged Data Class
#
# @author: Jon Lauters
#
# This will serve as an API Wrapper for PBDB and BHL as well as attempt real time data merging

import json, requests, re, unidecode

class PBDBBHL(object):

  def __init__(self):
    self.config = json.load(open('./config.json'))
    self.bhl_base_url = "http://www.biodiversitylibrary.org/api2/httpquery.ashx"
    self.records = []

  # Search for Taxonomic References by scientific/taxonomic name
  def taxa_references(self, base_name):
    pbdb = requests.get('https://paleobiodb.org/data1.2/taxa/refs.json?base_name=' + order)
    if 200 == pbdb.status_code:
    
      pbdb_json = json.loads( pbdb.contents )
      self.records = pbdb_json['records']
      return pbdb_json['records']

  # Get BHL titles 
  def bhl_title(self, title):
   bhl = requests.get(self.bhl_base_url + "?op=TitleSearchSimple&title=" + title + "&apikey=" + self.config['bhl_key'] + "&format=json")
   if 200 == bhl.status_code:
     bhl_json = json.loads( bhl.content )

     for bhl_title in bhl_json['Result']:
       if title in bhl_title['FullTitle']:
         return bhl_title
        
  # Get BHL Title Items
  def bhl_items(self, title_id, vol, pub_year):

    items = []
    title_items = requests.get(self.bhl_base_url + "?op=GetTitleItems&titleid=" + title_id + "&apikey=" + self.config['bhl_key'] + "&format=json")
    if 200 == title_items.status_code:
      items_json = json.loads( title_items.content )
      for item in items_json['Result']:
        if "v." + vol + " (" + pub_year + ")" in item['Volume']:
          items.append( str(item['itemID']) )

      return items

  # Get OCR
  def bhl_ocr(self, items, title):
    matched = False
    ocr_blob = ""
    for itemID in items:
      params = "&pages=t&parts=t&ocr=t&apikey=" + self.config['bhl_key'] + "&format=json"
      meta = requests.get(self.bhl_base_url + "?op=GetItemMetadata&itemid=" + itemID + params)
      if 200 == meta.status_code:
        meta_json = json.loads( meta.content )

        for page in meta_json['Result']['Pages']:
          if page['OcrText'] and page['OcrText'] is not None:

            # Clean up unicode weird formatting
            stripped = repr( page['OcrText'][:800].strip() )
            stripped = re.sub(ur"\\n", "", stripped)
 
            stripped_full = repr( page['OcrText'].strip() )
            stripped_full = re.sub(ur"\\n", "", stripped_full)

            ocr_blob += "\n" + stripped_full

            if stripped is not None:
              if title[:20].lower() in stripped.lower():
                matched = True

        if matched:
          return ocr_blob
        else:
          return ""

  # Link Taxonomic References to BHL  
  def references_bhl(self):
  
    pb_ocr = []

    for pb in self.records:
      if pb.has_key("tit") and pb.has_key("pbt"):

        volume = ""
        if "vol" in pb:
          volume = pb['vol']

        pub_year = ""
        if "pby" in pb:
          pub_year = pb['pby']

        bhl_title = self.bhl_title( pb['pbt'] ) 
        bhl_items = self.bhl_items( str(bhl_title['TitleID']), volume, pub_year ) 
        bhl_ocr   = self.bhl_ocr( bhl_items, pb['tit'])

        pb_ocr.append({"pb": pb, "ocr": bhl_ocr})
    
    return pb_ocr
