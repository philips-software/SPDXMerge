import SPDX_DeepMerge
import SPDX_ShallowMerge
import codecs
import sys
import codecs
from spdx.writers.json import write_document, InvalidDocumentError
from spdx.parsers.loggers import ErrorMessages

def SPDXDeepMerge_list(doc_list,docnamespace,name,author):
    spdxdeepmerge = SPDX_DeepMerge.SPDX_DeepMerger(doc_list,docnamespace,name,author)
    spdxdeepmerge.doc_creationinfo()
    spdxdeepmerge.doc_packageinfo()
    spdxdeepmerge.doc_fileinfo()
    spdxdeepmerge.doc_snippetinfo()
    spdxdeepmerge.doc_other_license_info()
    spdxdeepmerge.doc_relationship_info()
    doc = spdxdeepmerge.get_document()
    

    #Write file 
    file = "C:\\Temp\\MergedSBoM.json"
    with codecs.open(file, mode="w", encoding="utf-8") as out:
        try:
            write_document(doc, out)
        except InvalidDocumentError as e:
            print("Document is Invalid:\n\t", end="")
            print("\n\t".join(e.args[0]))
            messages = ErrorMessages()
            doc.validate(messages)
            print("\n".join(messages.messages))
    

def SPDXShallowMerge_list(doc_list,docnamespace,name,author):
    spdxshallowmerge = SPDX_ShallowMerge.SPDX_ShallowMerger(doc_list,docnamespace,name,author)
    spdxshallowmerge.doc_creationinfo()
    spdxshallowmerge.doc_externalDocumentRef()    
    doc = spdxshallowmerge.get_document()

    #Write file 
    file = "C:\\Temp\\MergedSBoM2.json"
    with codecs.open(file, mode="w", encoding="utf-8") as out:
        try:
            write_document(doc, out)
        except InvalidDocumentError as e:
            print("Document is Invalid:\n\t", end="")
            print("\n\t".join(e.args[0]))
            messages = ErrorMessages()
            doc.validate(messages)
            print("\n".join(messages.messages))