from datetime import datetime
from spdx_tools.spdx.model import (
    Document,
    Relationship,
    RelationshipType,
    CreationInfo,
    Actor,
    ActorType,
    Package,
    SpdxNoAssertion,
    Annotation,
    AnnotationType,
)
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdxmerge.SPDX_DeepMerge import SPDX_DeepMerger


def test_document_creation():
    doc1 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT1",
            name="Test Document 1",
            document_namespace="https://example.com/spdx1",
            creators=[Actor(name="John Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    doc2 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT2",
            name="Test Document 2",
            document_namespace="https://example.com/spdx2",
            creators=[Actor(name="Jane Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    merger = SPDX_DeepMerger(
        doc_list=[doc1, doc2],
        docnamespace="https://example.com/spdx",
        name="Merged Document",
        version="1.0",
        author="Yazat Mishra",
        email="yazat@example.com",
    )
    merged_doc = merger.get_document()

    assert merged_doc.creation_info.name == "Merged Document"
    assert merged_doc.creation_info.creators[0].name == "Yazat Mishra"
    assert merged_doc.creation_info.creators[0].email == "yazat@example.com"
    assert merged_doc.creation_info.document_namespace == "https://example.com/spdx"


def test_package_info():
    doc1 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT1",
            name="Test Document 1",
            document_namespace="https://example.com/spdx1",
            creators=[Actor(name="John Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    doc2 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT2",
            name="Test Document 2",
            document_namespace="https://example.com/spdx2",
            creators=[Actor(name="Jane Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    package1 = Package(
        name="Test Package 1",
        version="1.0",
        spdx_id="SPDXRef-PACKAGE1",
        download_location=SpdxNoAssertion(),
    )
    package2 = Package(
        name="Test Package 2",
        version="2.0",
        spdx_id="SPDXRef-PACKAGE2",
        download_location=SpdxNoAssertion(),
    )

    doc1.packages.append(package1)
    doc2.packages.append(package2)

    merger = SPDX_DeepMerger(
        doc_list=[doc1, doc2],
        docnamespace="https://example.com/spdx",
        name="Merged Document",
        version="1.0",
        author="Yazat Mishra",
        email="yazat@example.com",
    )
    merger.doc_packageinfo()
    merged_doc = merger.get_document()

    assert len(merged_doc.packages) == 3  # Includes root package
    assert merged_doc.packages[1].name == "Test Package 1"
    assert merged_doc.packages[2].name == "Test Package 2"


def test_relationships():
    doc1 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT1",
            name="Test Document 1",
            document_namespace="https://example.com/spdx1",
            creators=[Actor(name="John Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    doc2 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT2",
            name="Test Document 2",
            document_namespace="https://example.com/spdx2",
            creators=[Actor(name="Jane Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    rel1 = Relationship(
        spdx_element_id="SPDXRef-PACKAGE1",
        relationship_type=RelationshipType.CONTAINS,
        related_spdx_element_id="SPDXRef-DOCUMENT1",
    )

    rel2 = Relationship(
        spdx_element_id="SPDXRef-PACKAGE2",
        relationship_type=RelationshipType.DEPENDS_ON,
        related_spdx_element_id="SPDXRef-DOCUMENT2",
    )

    doc1.relationships.append(rel1)
    doc2.relationships.append(rel2)

    merger = SPDX_DeepMerger(
        doc_list=[doc1, doc2],
        docnamespace="https://example.com/spdx",
        name="Merged Document",
        version="1.0",
        author="Yazat Mishra",
        email="yazat@example.com",
    )
    merger.doc_packageinfo()
    merger.doc_relationship_info()
    merged_doc = merger.get_document()

    assert len(merged_doc.relationships) == 3  # Includes the DESCRIBES relationship
    assert merged_doc.relationships[1].relationship_type == RelationshipType.CONTAINS
    assert merged_doc.relationships[2].relationship_type == RelationshipType.DEPENDS_ON


def test_annotations():
    doc1 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT1",
            name="Test Document 1",
            document_namespace="https://example.com/spdx1",
            creators=[Actor(name="John Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    doc2 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT2",
            name="Test Document 2",
            document_namespace="https://example.com/spdx2",
            creators=[Actor(name="Jane Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    annotation1 = Annotation(
        spdx_id="SPDXRef-PACKAGE1",
        annotation_type=AnnotationType.OTHER,
        annotator=Actor(name="John Doe", actor_type=ActorType.ORGANIZATION),
        annotation_date=datetime.utcnow(),
        annotation_comment="Test annotation 1",
    )

    annotation2 = Annotation(
        spdx_id="SPDXRef-PACKAGE2",
        annotation_type=AnnotationType.REVIEW,
        annotator=Actor(name="Jane Doe", actor_type=ActorType.ORGANIZATION),
        annotation_date=datetime.utcnow(),
        annotation_comment="Test annotation 2",
    )

    doc1.annotations.append(annotation1)
    doc2.annotations.append(annotation2)

    merger = SPDX_DeepMerger(
        doc_list=[doc1, doc2],
        docnamespace="https://example.com/spdx",
        name="Merged Document",
        version="1.0",
        author="Yazat Mishra",
        email="yazat@example.com",
    )
    merger.doc_annotation_info()
    merged_doc = merger.get_document()

    assert merged_doc.annotations[0].annotation_comment == "Test annotation 1"
    assert merged_doc.annotations[1].annotation_comment == "Test annotation 2"
    assert len(merged_doc.annotations) == 2


def test_spdx_document_validation():
    doc1 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT1",
            name="Test Document 1",
            document_namespace="https://example.com/spdx1",
            creators=[Actor(name="John Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    doc2 = Document(
        CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT2",
            name="Test Document 2",
            document_namespace="https://example.com/spdx2",
            creators=[Actor(name="Jane Doe", actor_type=ActorType.ORGANIZATION)],
            created=datetime.utcnow().replace(microsecond=0),
        )
    )

    merger = SPDX_DeepMerger(
        doc_list=[doc1, doc2],
        docnamespace="https://example.com/spdx",
        name="Merged Document",
        version="1.0",
        author="Yazat Mishra",
        email="yazat@example.com",
    )
    merger.doc_packageinfo()
    merger.doc_fileinfo()
    merger.doc_snippetinfo()
    merger.doc_other_license_info()
    merger.doc_relationship_info()
    merged_doc = merger.get_document()
    validation_errors = validate_full_spdx_document(merged_doc)

    assert len(validation_errors) == 0  # Ensure document is valid SPDX
