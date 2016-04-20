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

Run on known hand verified match

http://search.idigbio.org/v2/view/records/c32288e2-cfba-447e-8491-5b82288a51f2
https://paleobiodb.org/data1.1/refs/single.json?id=5172&show=both

```
[5172] Title: New Miocene Coleoptera from Florissant
Specimen ID: c32288e2-cfba-447e-8491-5b82288a51f2

Vocabulary: 
{u'florissant': 7, u'cockerell': 4, u'colorado': 6, u'17': 0, u'abyssa': 2, u'coleoptera': 5, u'wickham': 8, u'acmaeodera': 3, u'1912': 1}

BOW:
  (1, 0)	1
  (1, 4)	1
  (2, 2)	1
  (3, 6)	1
  (5, 7)	1
  (6, 8)	1
  (9, 2)	1
  (9, 3)	1
  (10, 1)	1
  (12, 4)	1
  (13, 5)	1

BOW Shape:
(17, 9)

IDF:  [ 1.  1.  1.  1.  1.  1.  1.  1.  1.]

Term Breakdown: 
specificEpithet - abyssa - 1.0
stateProvince - colorado - 1.0
formation - florissant - 1.0
identBy - wickham - 1.0
dateItendified - 1912 - 1.0
recordedBy - cockerell - 1.0
order - coleoptera - 1.0


 ==== End Record ==== 


```

