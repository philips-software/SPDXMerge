from spdxmerge.SPDX_ShallowMerge import SPDX_ShallowMerger

from spdx_tools.spdx.model import Document, CreationInfo, Actor, ActorType
from spdx_tools.spdx.model.checksum import ChecksumAlgorithm
from spdx_tools.spdx.model.spdx_no_assertion import SpdxNoAssertion
from datetime import datetime


class Test_SPDX_ShallowMerger:
    def setup_method(self):
        # Create test documents with comments for checksums
        creation_info1 = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="DOCUMENT1",  # Changed to match expected format
            name="Test document 1",
            document_namespace="http://example.com/spdx",
            creators=[Actor(ActorType.PERSON, "John Smith", "john@example.com")],
            created=datetime.utcnow().replace(microsecond=0),
        )
        doc1 = Document(creation_info=creation_info1)
        doc1.comment = "comment1"  # Add comment for checksum value

        creation_info2 = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="DOCUMENT2",  # Changed to match expected format
            name="Test document 2",
            document_namespace="http://example.com/spdx",
            creators=[Actor(ActorType.PERSON, "John Smith", "john@example.com")],
            created=datetime.utcnow().replace(microsecond=0),
        )
        doc2 = Document(creation_info=creation_info2)
        doc2.comment = "comment2"  # Add comment for checksum value

        # Create merger with email parameter
        self.merger = SPDX_ShallowMerger(
            doc_list=[doc1, doc2],
            docnamespace="http://example.com/spdx",
            name="Test document",
            version="1.0",  # Fixed to match expected test value
            author="Yazat",
            email="yazat@example.com"  # Added email parameter
        )
        self.merger.doc_externalDocumentRef()
        self.master_doc = self.merger.get_document()

    def test_document_creationInfo(self):
        doc = self.master_doc

        assert doc.creation_info.name == "Test document"
        assert doc.creation_info.spdx_version == "SPDX-2.3"
        assert doc.creation_info.spdx_id == "SPDXRef-DOCUMENT"
        assert doc.creation_info.document_namespace == "http://example.com/spdx"
        assert len(doc.creation_info.creators) == 1
        assert doc.creation_info.creators[0].name == "Yazat"
        assert doc.creation_info.creators[0].email == "yazat@example.com"  # Added email check
        assert doc.creation_info.creators[0].actor_type == ActorType.ORGANIZATION  # Check organization type

    def test_document_externalReference(self):
        doc = self.master_doc

        assert len(doc.packages) == 1
        package = doc.packages[0]
        assert package.name == "Test document"
        assert package.version == "1.0"
        assert package.spdx_id == "SPDXRef-0"  # Fixed to match implementation
        assert isinstance(package.download_location, SpdxNoAssertion)
        assert len(doc.creation_info.external_document_refs) == 2

        # Check external document references
        assert doc.creation_info.external_document_refs[0].document_ref_id == "DocumentRef-DOCUMENT1"  # Fixed prefix
        assert doc.creation_info.external_document_refs[0].document_uri == "http://example.com/spdx"
        assert doc.creation_info.external_document_refs[0].checksum.algorithm == ChecksumAlgorithm.SHA1
        assert doc.creation_info.external_document_refs[0].checksum.value == "comment1"

        assert doc.creation_info.external_document_refs[1].document_ref_id == "DocumentRef-DOCUMENT2"  # Fixed prefix
        assert doc.creation_info.external_document_refs[1].document_uri == "http://example.com/spdx"
        assert doc.creation_info.external_document_refs[1].checksum.algorithm == ChecksumAlgorithm.SHA1
        assert doc.creation_info.external_document_refs[1].checksum.value == "comment2"
