# ePANNDA Matching Module
#
# @author: Jon Lauters
#

from pbdbbhl import PBDBBHL
import idigbio

def matchName( scientific_name ):

  # PBDB with BHL OCR Text query
  pbdb = PBDBBHL()
  pbdb.taxa_references( scientific_name )
  ocr_matches = pbdb.references_bhl()

  # Python client for iDigBio
  api = idigbio.json()
  record_list = api.search_records(rq={"scientificname": scientific_name})

  if not record_list:
    # try order level
    record_list = api.search_records(rq={"order": scientific_name})

  # Run through scoring algorithm


def matchJournal( journal ):
  # Kick Off Search to PBDB+BHL
  # Intermediate Step - Parse above response for list of specimen names
  # Kick Off Search to iDigBio
  pass

def matchArticle( article ):
  # Kick Off Search to PBDB
  # Get Journal Name for Article then call matchJournal() 
  pass

def matchPerson( name ):
  # Kick Off Search to PBDB+BHL
  # Kick Off Search to iDigBio ( "Collected By", "Idendified By" )
  pass