import codecs
from spdx.writers.json import write_document as write_json_document, InvalidDocumentError as JsonInvalidDocumentError
from spdx.writers.tagvalue import write_document as write_tagvalue_document, InvalidDocumentError as TagvalueInvalidDocumentError
from spdx.parsers.loggers import ErrorMessages
import SPDX_DeepMerge
import SPDX_ShallowMerge

def create_merged_spdx_document(doc_list, docnamespace, name, author, email, merge_type):
    if merge_type == "deep":
        merger = SPDX_DeepMerge.SPDX_DeepMerger(doc_list, docnamespace, name, author, email)
        merger.doc_creationinfo()
        merger.doc_packageinfo()
        merger.doc_fileinfo()
        merger.doc_snippetinfo()
        merger.doc_other_license_info()
        merger.doc_relationship_info()
    elif merge_type == "shallow":
        merger = SPDX_ShallowMerge.SPDX_ShallowMerger(doc_list, docnamespace, name, author, email)
        merger.doc_creationInfo()
        merger.doc_externalDocumentRef()

    return merger.get_document()

def write_file(doc, filetype, merge_type):
    result_filetype = "spdx" if filetype.lower() == "t" else "json"
    file = f"merged-SBoM-{merge_type}.{result_filetype}"
    with codecs.open(file, mode="w", encoding="utf-8") as out:
        try:
            if result_filetype == "spdx":
                write_tagvalue_document(doc, out)
            else:
                write_json_document(doc, out)
        except (TagvalueInvalidDocumentError, JsonInvalidDocumentError) as e:
            print("Document is Invalid:\n\t", end="")
            print("\n\t".join(e.args[0]))
            messages = ErrorMessages()
            doc.validate(messages)
            print("\n".join(messages.messages))
        print("File "+file+" is generated")
