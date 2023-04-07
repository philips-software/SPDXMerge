from datetime import datetime

from spdxmerge.SPDX_DeepMerge import SPDX_DeepMerger

from spdx.annotation import Annotation
from spdx.creationinfo import Person
from spdx.document import Document
from spdx.file import File
from spdx.license import License
from spdx.package import Package
from spdx.relationship import Relationship
from spdx.review import Review
from spdx.snippet import Snippet
from spdx.version import Version

class TestSPDXDeepMerger:

    def test_document_creation(self):
        doc1 = Document(
                name="Test document 1",
                spdx_id="SPDXRef-DOCUMENT1",
                namespace="http://example.com/spdx",
                data_license=License.from_identifier("CC0-1.0")
            )
        doc1.creation_info.add_creator(Person("John Smith", "john@example.com"))

        merger = SPDX_DeepMerger(doc_list=[doc1], docnamespace="https://example.com", name="Test Document", author="Test Author", email="test@example.com")
        merger.doc_creationinfo()

        doc = merger.get_document()
        assert doc.name == "Test Document"
        assert doc.version == Version(2,3)
        assert doc.spdx_id == "https://example.com#SPDXRef-DOCUMENT"
        assert doc.namespace == "https://example.com"
        assert doc.data_license == License.from_identifier("CC0-1.0")
        assert len(doc.creation_info.creators) == 1
        assert doc.creation_info.creators[0].name == "Test Author"

    def test_package_info(self):
        doc1 = Document()
        package1 = Package(name = "Package 1")
        doc1.add_package(package1)

        doc2 = Document()
        package2 = Package(name = "Package 2")
        doc2.add_package(package2)

        merger = SPDX_DeepMerger(doc_list=[doc1, doc2])
        merger.doc_packageinfo()

        doc = merger.get_document()
        assert len(doc.packages) == 2
        assert doc.packages[0].name == "Package 1"
        assert doc.packages[1].name == "Package 2"

    def test_file_info(self):
        doc1 = Document()
        file1 = File(name="file1")
        doc1.add_file(file1)

        doc2 = Document()
        file2 = File(name="file2")
        doc2.add_file(file2)

        merger = SPDX_DeepMerger(doc_list=[doc1, doc2])
        merger.doc_fileinfo()

        doc = merger.get_document()
        assert len(doc.files) == 2
        assert doc.files[0].name == "file1"
        assert doc.files[1].name == "file2"

    def test_snippet_info(self):
        doc1 = Document()
        snippet1 = Snippet()
        snippet1.comment = "snip1"
        doc1.add_snippet(snippet1)

        doc2 = Document()
        snippet2 = Snippet()
        snippet2.comment = "snip2"
        doc2.add_snippet(snippet2)

        merger = SPDX_DeepMerger(doc_list=[doc1, doc2])
        merger.doc_snippetinfo()

        doc = merger.get_document()
        assert len(doc.snippet) == 2
        assert doc.snippet[0].comment == "snip1"
        assert doc.snippet[1].comment == "snip2"

    def test_other_license_info(self):
        doc1 = Document()
        license1 = License.from_identifier("License1")
        doc1.add_extr_lic(license1)

        doc2 = Document()
        license2 = License.from_identifier("License2")
        doc1.add_extr_lic(license2)

        merger = SPDX_DeepMerger(doc_list=[doc1, doc2])
        merger.doc_other_license_info()

        doc = merger.get_document()
        assert len(doc.extracted_licenses) == 2
        assert doc.extracted_licenses[0].full_name == "License1"
        assert doc.extracted_licenses[0].identifier == "License1"
        assert doc.extracted_licenses[1].full_name == "License2"
        assert doc.extracted_licenses[1].identifier == "License2"

    def test_relationship_info(self):
        # Create two sample SPDX documents
        doc1 = Document()
        doc2 = Document()
        doc1.spdx_id = "SPDXRef-DOCUMENT1"
        doc2.spdx_id = "SPDXRef-DOCUMENT2"

        # Add relationship information to each document
        rel1 = Relationship("SPDXRef-PACKAGE1 DESCRIBES SPDXRef-DOCUMENT1")
        rel2 = Relationship("SPDXRef-PACKAGE2 DEPENDS_ON SPDXRef-PACKAGE1")
        doc1.add_relationship(rel1)
        doc2.add_relationship(rel2)

        # Merge the two documents using SPDX_DeepMerger
        merger = SPDX_DeepMerger([doc1, doc2], "https://example.com/spdx", "Test Document", "John Doe", "john@example.com")
        merger.doc_creationinfo()
        merger.doc_relationship_info()
        merged_doc = merger.get_document()

        # Verify that the merged document contains all the relationship information from both documents
        assert len(merged_doc.relationships) == 4
        assert merged_doc.relationships[0].relationship_type == "DESCRIBES"
        assert merged_doc.relationships[0].related_spdx_element == doc1.spdx_id
        assert merged_doc.relationships[0].spdx_element_id == "https://example.com/spdx#SPDXRef-DOCUMENT"

        assert merged_doc.relationships[1].relationship_type == "DESCRIBES"
        assert merged_doc.relationships[1].related_spdx_element == doc1.spdx_id
        assert merged_doc.relationships[1].spdx_element_id == "SPDXRef-PACKAGE1"

        assert merged_doc.relationships[2].relationship_type == "DESCRIBES"
        assert merged_doc.relationships[2].related_spdx_element == doc2.spdx_id
        assert merged_doc.relationships[2].spdx_element_id == "https://example.com/spdx#SPDXRef-DOCUMENT"

        assert merged_doc.relationships[3].relationship_type == "DEPENDS_ON"
        assert merged_doc.relationships[3].related_spdx_element == "SPDXRef-PACKAGE1"
        assert merged_doc.relationships[3].spdx_element_id == "SPDXRef-PACKAGE2"



    def test_annotation_info(self):
        # Create two sample SPDX documents
        doc1 = Document()
        doc2 = Document()
        doc1.spdx_id = "SPDXRef-DOCUMENT1"
        doc2.spdx_id = "SPDXRef-DOCUMENT2"

        # Add annotation information to each document
        ann1 = Annotation(spdx_id="SPDXRef-PACKAGE1", comment="This is a comment", annotator="John Doe")
        ann2 = Annotation(spdx_id="SPDXRef-PACKAGE2", comment="Another comment", annotator="Jane Smith")
        doc1.annotations.append(ann1)
        doc2.annotations.append(ann2)

        # Merge the two documents using SPDX_DeepMerger
        merger = SPDX_DeepMerger([doc1, doc2], "https://example.com/spdx", "Test Document", "John Doe", "john@example.com")
        merger.doc_creationinfo()
        merger.doc_annotation_info()
        merged_doc = merger.get_document()

        # Verify that the merged document contains all the annotation information from both documents
        assert len(merged_doc.annotations) == 2
        assert merged_doc.annotations[0].comment == "This is a comment"
        assert merged_doc.annotations[0].annotator == "John Doe"
        assert merged_doc.annotations[1].comment == "Another comment"
        assert merged_doc.annotations[1].annotator == "Jane Smith"


    def test_review_info(self):
        # Create two sample SPDX documents
        doc1 = Document()
        doc2 = Document()
        doc1.spdx_id = "SPDXRef-DOCUMENT1"
        doc2.spdx_id = "SPDXRef-DOCUMENT2"

        # Add review information to each document
        rev1 = Review("Reviewer 1", datetime.date, "Looks good to me")
        rev2 = Review("Reviewer 2", datetime.date, "I have some concerns about this file")
        doc1.reviews.append(rev1)
        doc2.reviews.append(rev2)

        # Merge the two documents using SPDX_DeepMerger
        merger = SPDX_DeepMerger([doc1, doc2], "https://example.com/spdx", "Test Document", "John Doe", "john@example.com")
        merger.doc_creationinfo()
        merger.doc_review_info()
        merged_doc = merger.get_document()

        # Verify that the merged document contains all the review information from both documents
        assert len(merged_doc.reviews) == 2
        assert merged_doc.reviews[0].reviewer == "Reviewer 1"
        assert merged_doc.reviews[0].comment == "Looks good to me"
        assert merged_doc.reviews[1].reviewer == "Reviewer 2"
        assert merged_doc.reviews[1].comment == "I have some concerns about this file"
