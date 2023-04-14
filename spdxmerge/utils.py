import os
from spdx.parsers import parse_anything
from spdxmerge.checksum import sha1sum

def read_docs(dir):
    doc_list = []
    doc_files = [f for f in os.listdir(dir) if f.endswith(('.json', '.spdx'))]
    for file in doc_files:
        doc, _error = parse_anything.parse_file(dir+"/"+file)
        check_sum = sha1sum(dir+"/"+file)
        doc.comment = check_sum
        doc_list.append(doc)
    return doc_list
