ePANDDA Aggregation
=====================

#### ocr_mine.py
Simple miner script that links PBDB Biblio References to Full Text articles in BHL. Stores the OCR Text in a MongoDB

#### specimen_match.py
Simple script to pull OCR out of MongoDB and attempt string matching of iDigbio DarwinCore Fields against the OCR text body.

#### annotation.py
Simple module to construct OpenAnnotation style JSON-LD objects.

Example Output:
http://grab.by/PIic

http://json-ld.org/playground/#startTab=tab-expanded&json-ld=%7B%22%40context%22%3A%22https%3A%2F%2Fwww.w3.org%2Fns%2Foa.jsonld%22%2C%22%40id%22%3A%22https%3A%2F%2Fepandda.org%2Fannotations%2F44f2fe5e-044f-4644-ab9e-2b263350f42d%22%2C%22%40type%22%3A%22oa%3AAnnotation%22%2C%22annotatedBy%22%3A%7B%22mbox%22%3A%7B%22%40id%22%3A%22mailto%3Aannotation%40epandda.org%22%7D%2C%22%40id%22%3A%22http%3A%2F%2Fgrab.by%2FPuPq%22%2C%22%40type%22%3A%22foaf%3AProject%22%2C%22name%22%3A%22ePANDDA%20Annotation%20Bot%22%7D%2C%22annotatedAt%22%3A%222016-04-25%2009%3A15%3A42%20%22%2C%22hasTarget%22%3A%7B%22%40id%22%3A%22urn%3Auuid%3Ad3c579c1-8f41-4158-8580-45c6c9d6656c%22%2C%22%40type%22%3A%22oa%3ASpecificResource%22%2C%22hasSource%22%3A%7B%22%40id%22%3A%22http%3A%2F%2Fsearch.idigbio.org%2Fv2%2Fview%2Frecords%2Fd3c579c1-8f41-4158-8580-45c6c9d6656c%22%7D%7D%2C%22hasBody%22%3A%7B%22chars%22%3A%22Insects%20in%20Burmese%20amber%22%2C%22%40id%22%3A%22%22%2C%22%40type%22%3A%5B%22dwc%3AOccurrence%22%2C%22dctype%3AText%22%5D%7D%7D&frame=%7B%7D&context=%7B%7D


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

