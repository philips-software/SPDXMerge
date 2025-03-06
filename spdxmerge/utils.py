import os
from spdx_tools.spdx.parser import parse_anything
from spdxmerge.checksum import sha1sum

def read_docs(dir, root_doc_path):
    doc_list = []
    root_doc = None
    doc_files = [f for f in os.listdir(dir) if f.endswith(('.json', '.spdx'))]
    
    # Check if root document is present in the directory
    if root_doc_path and root_doc_path in doc_files:
        root_doc = parse_anything.parse_file(dir+"/"+root_doc_path)
        root_doc.comment = sha1sum(dir+"/"+root_doc_path)
    else:
        if root_doc_path != '':
            # Raise error if --rootdocpath is defined but given root document is not found
            raise FileNotFoundError(f"Root document {root_doc_path} not found in directory {dir}.")
    for file in doc_files:
        doc = parse_anything.parse_file(dir+"/"+file)
        check_sum = sha1sum(dir+"/"+file)
        doc.comment = check_sum
        doc_list.append(doc)
        
    return doc_list, root_doc
