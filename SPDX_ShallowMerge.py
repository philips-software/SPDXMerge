#from spdx.checksum import Algorithm
from spdx.checksum import Checksum
from spdx.creationinfo import Person
from spdx.license import License
from spdx.document import (Document,ExternalDocumentRef)
from spdx.package import Package
from spdx.version import Version




master_doc = Document()

class SPDX_ShallowMerger():
    def __init__(self,doc_list=None,docnamespace=None,name=None,author=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name 
        self.author = author
        self.emailaddr ="dummy@mail.com"

    def get_document(self):
        return master_doc

    def doc_creationinfo(self):
        master_doc.name = self.name
        master_doc.version = Version(2,3)              # TODO Need to check from where to take this. can not hardcode here 
        master_doc.spdx_id = self.docnamespace + "#SPDXRef-DOCUMENT"         
        master_doc.namespace = self.docnamespace
        master_doc.data_license = License.from_identifier("CC0-1.0")           #TODO Can not hardcode it here need to check from where to take it. 
        master_doc.creation_info.add_creator(Person(self.author,self.emailaddr))
        master_doc.creation_info.set_created_now()
   

    def doc_externalDocumentRef(self):        
       # testfile2 = File("TestFile2")
       # testfile2.type = FileType.SOURCE
       # testfile2.spdx_id = "TestFile2#SPDXRef-FILE"
       # testfile2.comment = "This is a test file."
       # testfile2.chk_sum = Algorithm("SHA1", "bb154f28d1cf0646ae21bb0bec6c669a2b90e113")
       # testfile2.conc_lics = License.from_identifier("Apache-2.0")
       # testfile2.add_lics(License.from_identifier("Apache-2.0"))
       # testfile2.copyright = NoAssert()

      #  package = Package()
      #  package.name = self.name
      #  package.version = "1.0"
      #  package.file_name = "twt.jar"
      #  package.spdx_id = 'TestPackage#SPDXRef-PACKAGE'
      #  package.download_location = "http://www.tagwritetest.test/download"
      #  package.check_sum = Algorithm("SHA1", "c537c5d99eca5333f23491d47ededd083fefb7ad")
      #  package.homepage = SPDXNone()
      #  package.verif_code = "4e3211c67a2d28fced849ee1bb76e7391b93feba"
      #  license_set = LicenseConjunction(
      #      License.from_identifier("Apache-2.0"), License.from_identifier("BSD-2-Clause")
      #  )
      #  package.conc_lics = license_set
      #  package.license_declared = license_set
      #  package.add_lics_from_file(License.from_identifier("Apache-2.0"))
      #  package.add_lics_from_file(License.from_identifier("BSD-2-Clause"))
      #  package.cr_text = NoAssert()
      #  package.summary = "Simple package."
      #  package.description = "Really simple package."
      # package.add_file(testfile2)
        package = Package()
        package.name = self.name
        package.version = "1.0"
        package.spdx_id = self.docnamespace + "#SPDXRef-DOCUMENT"  
        package.download_location = NoAssert()

        master_doc.add_package(package)
        for doc in self.doc_list:            
            chek_sum = Checksum('sha1',doc.comment)             
            extDoc = ExternalDocumentRef(doc.spdx_id,doc.namespace,chek_sum)
            master_doc.add_ext_document_reference(extDoc)
    
    