import os
import json
from spdxmerge.SPDX_DeepMerge import SPDX_DeepMerger
from spdxmerge.SPDX_ShallowMerge import SPDX_ShallowMerger
from spdx_tools.spdx.writer.json.json_writer import (
    write_document_to_file as write_json_document,
)
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer import (
    write_document_to_file as write_tagvalue_document
)

def create_merged_spdx_document(doc_list, docnamespace, name, version, author, email, merge_type, root_doc):
    if merge_type == "deep":
        merger = SPDX_DeepMerger(doc_list, docnamespace, name, version, author, email, root_doc)
        merger.doc_packageinfo()
        merger.doc_fileinfo()
        merger.doc_snippetinfo()
        merger.doc_other_license_info()
        merger.doc_relationship_info()
    elif merge_type == "shallow":
        merger = SPDX_ShallowMerger(doc_list, docnamespace, name, version, author, email)
        merger.doc_externalDocumentRef()

    return merger.get_document()

def write_file(doc, filetype, merge_type, outpath=None):
    result_filetype = "spdx" if filetype.lower() == "t" else "json"
    file = f"merged-SBoM-{merge_type}.{result_filetype}"
    if outpath:
        file = os.path.join(outpath, file)
    try:
        if result_filetype == "spdx":
            write_tagvalue_document(doc, file, validate=False)
        else:
            write_json_document(doc, file, validate=False)
            with open(file, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                print(json.dumps(json_content, indent=2))
    except (ValueError) as e:
        print("Document is Invalid:", end="")
        print((e.args[0]))
    print("File "+file+" is generated")
