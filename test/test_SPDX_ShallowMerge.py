from spdxmerge.SPDX_ShallowMerge import SPDX_ShallowMerger

from spdx.creationinfo import Person
from spdx.document import Document
from spdx.license import License
from spdx.utils import NoAssert
from spdx.version import Version


class Test_SPDX_ShallowMerger:
    def setup_method(self):
        doc1 = Document(
                name="Test document 1",
                spdx_id="SPDXRef-DOCUMENT1",
                namespace="http://example.com/spdx",
                data_license=License.from_identifier("CC0-1.0")
            )
        doc1.creation_info.add_creator(Person("John Smith", "john@example.com"))
        doc1.comment = "comment1"
        doc2 =  Document(
                name="Test document 2",
                spdx_id="SPDXRef-DOCUMENT2",
                namespace="http://example.com/spdx",
                data_license=License.from_identifier("CC0-1.0")
            )
        doc2.creation_info.add_creator(Person("John Smith", "john@example.com"))
        doc2.comment = "comment2"
        self.docs = [doc1,doc2]
        self.m = SPDX_ShallowMerger(self.docs, "http://example.com/spdx", "Test document", "John Doe")

    def test_document_creationInfo(self):
        self.m.doc_creationInfo()
        doc = self.m.get_document()

        assert doc.name == "Test document"
        assert doc.version == Version(2,3)
        assert doc.spdx_id == "http://example.com/spdx#SPDXRef-DOCUMENT"
        assert doc.namespace == "http://example.com/spdx"
        assert doc.data_license.identifier == "CC0-1.0"
        assert len(doc.creation_info.creators) == 1
        assert doc.creation_info.creators[0].name == "John Doe"

    def test_document_externalReference(self):
        self.m.doc_creationInfo()
        self.m.doc_externalDocumentRef()
        doc = self.m.get_document()

        assert len(doc.packages) == 1
        package = doc.packages[0]
        assert package.name == "Test document"
        assert package.version == "1.0"
        assert package.spdx_id == "http://example.com/spdx#SPDXRef-DOCUMENT"
        assert isinstance(package.download_location, NoAssert)
        assert len(doc.ext_document_references) == 2
        assert doc.ext_document_references[0].external_document_id == "SPDXRef-DOCUMENT1"
        assert doc.ext_document_references[0].spdx_document_uri == "http://example.com/spdx"
        assert doc.ext_document_references[0].checksum.identifier.name == "SHA1"
        assert doc.ext_document_references[0].checksum.value == "comment1"
        assert doc.ext_document_references[1].external_document_id == "SPDXRef-DOCUMENT2"
        assert doc.ext_document_references[1].spdx_document_uri == "http://example.com/spdx"
        assert doc.ext_document_references[1].checksum.identifier.name == "SHA1"
        assert doc.ext_document_references[1].checksum.value == "comment2"
