from datetime import datetime
from spdx_tools.spdx.model import (
    Document,
    Relationship,
    RelationshipType,
    CreationInfo,
    Actor,
    ActorType
)

class SPDX_DeepMerger():

    def __init__(self,
                 doc_list=None,
                 docnamespace=None,
                 name=None,
                 author=None,
                 email=None):
        self.doc_list = doc_list
        # data_license is "CC0-1.0" by default
        self.master_doc = Document(CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT",
            name=name,
            document_namespace=docnamespace,
            creators=[Actor(
                actor_type=ActorType.ORGANIZATION,
                name=author
            )],
            created=datetime.utcnow().replace(microsecond=0)
        ))

    def get_document(self):
        return self.master_doc

    def doc_packageinfo(self):
        """
        Append packages from document list
        """
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
                eli for eli in doc.extracted_licensing_info
                if eli.license_id not in master_doc_eli_ids
            ]
            master_doc_eli_ids += [eli.license_id for eli in doc_eli]
            self.master_doc.extracted_licensing_info += doc_eli

    def doc_relationship_info(self):
        for doc in self.doc_list:
            # Add 'DESCRIBES' relationship between master and child documents and
            # then import all relationships in child docs
            relationship = Relationship(
                spdx_element_id=self.master_doc.creation_info.spdx_id,
                relationship_type=RelationshipType.DESCRIBES,
                related_spdx_element_id=doc.creation_info.spdx_id
            )
            #doc.relationships += [relationship]
            #self.master_doc.relationships += doc.relationships
            self.master_doc.relationships += [relationship]

    def doc_annotation_info(self):
        for doc in self.doc_list:
            self.master_doc.annotations += doc.annotations

    def doc_review_info(self):
        for doc in self.doc_list:
            self.master_doc.reviews += doc.reviews
