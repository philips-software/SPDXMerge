from spdx.creationinfo import Person
from spdx.license import License
from spdx.document import Document
from spdx.relationship import Relationship,RelationshipType
from spdx.version import Version

master_doc = Document()

class SPDX_DeepMerger():

    def __init__(self,doc_list=None,docnamespace=None,name=None,author=None,email=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name
        self.author = author
        self.emailaddr = email

    def get_document(self):
        return master_doc

    def doc_creationinfo(self):
        master_doc.name = self.name
        master_doc.version = Version(2,3) # TODO Need to check from where to take this. can not hardcode here
        master_doc.spdx_id = self.docnamespace + "#SPDXRef-DOCUMENT"
        master_doc.namespace = self.docnamespace
        master_doc.data_license = License.from_identifier("CC0-1.0") #TODO Can not hardcode it here need to check from where to take it.
        master_doc.creation_info.add_creator(Person(self.author,self.emailaddr))
        master_doc.creation_info.set_created_now()

    def doc_packageinfo(self):
        """
        Append packges from document list
        """
        for doc in self.doc_list:
            master_doc.packages.extend(doc.packages)

    def doc_fileinfo(self):
        for doc in self.doc_list:
            master_doc.files.extend(doc.files)  #TODO Need to check this its not returning list

    def doc_snippetinfo(self):
        for doc in self.doc_list:
            master_doc.snippet.extend(doc.snippet)

    def doc_other_license_info(self):
        for doc in self.doc_list:
            master_doc.extracted_licenses.extend(doc.extracted_licenses)

    def doc_relationship_info(self):
        for doc in self.doc_list:
            # Add 'DESCRIBES' relationship between master and child documents, then import all relationships in child docs
            relationship = Relationship(master_doc.spdx_id+" "+RelationshipType.DESCRIBES.name+" "+doc.spdx_id)
            master_doc.add_relationship(relationship)
            master_doc.relationships.extend(doc.relationships)

    def doc_annotation_info(self):
        for doc in self.doc_list:
            master_doc.annotations.extend(doc.annotations)

    def doc_review_info(self):
        for doc in self.doc_list:
            master_doc.reviews.extend(doc.reviews)
