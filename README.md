ePANDDA Aggregation
=====================

#### ocr_mine.py
Simple miner script that links PBDB Biblio References to Full Text articles in BHL. Stores the OCR Text in a MongoDB

#### specimen_match.py
Simple script to pull OCR out of MongoDB and attempt string matching of iDigbio DarwinCore Fields against the OCR text body.

#### annotation.py
Simple class to construct OpenAnnotation style JSON-LD objects fed from the matches in specimen_match.py

#### person.py
Discovery script to look into feasability of doing data aggregation by person name.

#### dispatcher.py
API Skeleton
