from spdx.checksum import Checksum,ChecksumAlgorithm
from spdx.utils import NoAssert
from spdx.creationinfo import Person
from spdx.license import License
from spdx.document import (Document,ExternalDocumentRef)
from spdx.package import Package
from spdx.version import Version

master_doc = Document()

class SPDX_ShallowMerger():
    def __init__(self,doc_list=None,docnamespace=None,name=None,author=None,email=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name
        self.author = author
        self.emailaddr = email

    def get_document(self):
        return master_doc

    def doc_creationInfo(self):
        master_doc.name = self.name
        master_doc.version = Version(2,3) # TODO Need to check from where to take this. can not hardcode here
        master_doc.spdx_id = self.docnamespace + "#SPDXRef-DOCUMENT"
        master_doc.namespace = self.docnamespace
        master_doc.data_license = License.from_identifier("CC0-1.0") #TODO Can not hardcode it here need to check from where to take it.
        master_doc.creation_info.add_creator(Person(self.author,self.emailaddr))
        master_doc.creation_info.set_created_now()

    def doc_externalDocumentRef(self):
        package = Package()
        package.name = self.name
        package.version = "1.0"
        package.spdx_id = self.docnamespace + "#SPDXRef-DOCUMENT"
        package.download_location = NoAssert()

        master_doc.add_package(package)
        for doc in self.doc_list:
            check_sum = Checksum(ChecksumAlgorithm.SHA1,doc.comment)
            extDoc = ExternalDocumentRef(doc.spdx_id,doc.namespace,check_sum)
            master_doc.add_ext_document_reference(extDoc)
