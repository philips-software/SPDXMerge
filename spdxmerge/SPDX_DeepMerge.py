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
)


class SPDX_DeepMerger:
    def __init__(
        self,
        doc_list=None,
        docnamespace=None,
        name=None,
        version=None,
        author=None,
        email=None,
        root_doc=None,
    ):
        self.doc_list = doc_list
        self.version = version
        self.root_doc = root_doc
        # data_license is "CC0-1.0" by default
        self.master_doc = Document(
            CreationInfo(
                spdx_version="SPDX-2.3",
                spdx_id="SPDXRef-DOCUMENT",
                name=name,
                document_namespace=docnamespace,
                creators=[
                    Actor(actor_type=ActorType.ORGANIZATION, name=author, email=email)
                ],
                created=datetime.utcnow().replace(microsecond=0),
            )
        )

    def get_document(self):
        return self.master_doc

    def doc_packageinfo(self):
        """
        Append packages from document list
        """
        if self.root_doc is None:
            Main_Package = Package(
                name=self.master_doc.creation_info.name,
                version=self.version,
                spdx_id="SPDXRef-" + str(0),
                download_location=SpdxNoAssertion(),
            )

            self.master_doc.packages.append(Main_Package)
        for doc in self.doc_list:
            self.master_doc.packages += doc.packages

    def doc_fileinfo(self):
        for doc in self.doc_list:
            self.master_doc.files += doc.files

    def doc_snippetinfo(self):
        for doc in self.doc_list:
            self.master_doc.snippets += doc.snippets

    def doc_other_license_info(self):
        """
        Append unique licenses to hasExtractedLicensingInfo
        """
        master_doc_eli_ids = []
        for doc in self.doc_list:
            doc_eli = [
                eli
                for eli in doc.extracted_licensing_info
                if eli.license_id not in master_doc_eli_ids
            ]
            master_doc_eli_ids += [eli.license_id for eli in doc_eli]
            self.master_doc.extracted_licensing_info += doc_eli

    def doc_relationship_info(self):
        if self.root_doc is None:
            Main_Package = self.master_doc.packages[0]
            # The document should DESCRIBE the root package with name as input name and version as input version
            relationship = Relationship(
                spdx_element_id=self.master_doc.creation_info.spdx_id,
                relationship_type=RelationshipType.DESCRIBES,
                related_spdx_element_id=Main_Package.spdx_id,
            )

        else:
            found = False
            # Find the SPDX element ID with the DESCRIBES relationship
            for rel in self.root_doc.relationships:
                if rel.relationship_type == RelationshipType.DESCRIBES:
                    related_spdx_element_id = rel.related_spdx_element_id
                    found = True
                    break

            # If no DESCRIBES relationship is found, raise an error
            if not found:
                raise ValueError("Root document has no relationship of type DESCRIBES")

            relationship = Relationship(
                spdx_element_id=self.master_doc.creation_info.spdx_id,
                relationship_type=RelationshipType.DESCRIBES,
                related_spdx_element_id=related_spdx_element_id,
            )

        self.master_doc.relationships.append(relationship)

        # Also add relationships from the imported documents
        valid_relationships = []
        for doc in self.doc_list:
            for rel in doc.relationships:
                # Since we need a unique DESCIRBES, skip the other DESCRIBES relationships
                if rel.relationship_type == RelationshipType.DESCRIBES:
                    continue

                valid_relationships.append(rel)

        # Append only valid relationships
        self.master_doc.relationships += valid_relationships

    # Since Reviews have been deprecated in SPDX 2.3, we will not include this and instead use Annotations
    def doc_annotation_info(self):
        for doc in self.doc_list:
            self.master_doc.annotations += doc.annotations
