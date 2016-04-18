ePANDDA Aggregation
=====================

#### ocr_mine.py
Simple miner script that links PBDB Biblio References to Full Text articles in BHL. Stores the OCR Text in a MongoDB

#### specimen_match.py
Simple script to pull OCR out of MongoDB and attempt string matching of iDigbio DarwinCore Fields against the OCR text body.

#### annotation.py
Simple module to construct OpenAnnotation style JSON-LD objects.

#### person.py
Discovery script to look into feasability of doing data aggregation by person name.

#### dispatcher.py
API Skeleton

#### process_ocr.py
Attemp to run Ocr Text through TF/IDF compared to terms in iDigBio Data ( DWC )

Example Output:
```
IDF:  [ 1.30918828  3.93385687  1.          1.          1.01069529  1.01069529
  1.32378708  1.80562516  1.22580667  1.43242092  1.46575734  5.54329478
  1.90570862  1.17384693  1.33860216  2.24745792  1.          3.59738463
  4.44468249  1.19948936  3.75153531  1.29479954  1.73663229  1.22580667
  4.15700042]
```
