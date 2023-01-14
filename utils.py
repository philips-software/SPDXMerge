import os
import checksum
import spdx.creationinfo
from spdx.parsers import parse_anything
from spdx.parsers.loggers import ErrorMessages


def read_docs(dir):
   doc_list = []
   doc_files = [pos_json for pos_json in os.listdir(dir) if pos_json.endswith('.json')] 
   for file in doc_files: 
      doc, error = parse_anything.parse_file(dir+"\\"+file)      
      chek_sum = checksum.sha1sum(dir+"\\"+file)
      doc.comment = chek_sum
      doc_list.append(doc)
   return doc_list;
   