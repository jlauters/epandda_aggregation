# ePANNDA Matching Module
#
# @author: Jon Lauters
#

from pbdbbhl import PBDBBHL
from pbdbbhl import taxa_by_ref
import idigbio
import scoring

def matchName( scientific_name ):

  # PBDB with BHL OCR Text query
  pbdb = PBDBBHL( scientific_name )

  # Python client for iDigBio
  api = idigbio.json()
  record_list = api.search_records(rq={"scientificname": scientific_name})

  if not record_list:
    # try order level
    record_list = api.search_records(rq={"order": scientific_name})

  # Run through scoring algorithm
  return scoring.scorePubs(pbdb.records, record_list, 3) 

def matchFull( search_name ):

  print "in matchFull: search_name = " + search_name

  # PBDB Taxa By Refs with Joined Reference info
  pbdb = taxa_by_ref( search_name ) 

  return pbdb

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
