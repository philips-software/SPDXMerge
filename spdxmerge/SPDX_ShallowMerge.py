from datetime import datetime
from spdx_tools.spdx.model import (
    Checksum,
    ChecksumAlgorithm,
    Actor,
    ActorType,
    Document,
    ExternalDocumentRef,
    Package,
    SpdxNoAssertion,
    CreationInfo
)
class SPDX_ShallowMerger():
    def __init__(self,
                 doc_list=None,
                 docnamespace=None,
                 name=None,
                 version=None,
                 author=None,
                 email=None):
        self.doc_list = doc_list
        self.version = version
        # data_license is "CC0-1.0" by default
        self.master_doc = Document(CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT",
            name=name,
            document_namespace=docnamespace,
            creators=[Actor(
                actor_type=ActorType.ORGANIZATION,
                name=author,
                email=email
            )],
            created=datetime.utcnow().replace(microsecond=0)
        ))

    def get_document(self):
        return self.master_doc

    def doc_externalDocumentRef(self):
        package = Package(
            name=self.master_doc.creation_info.name,
            version=self.version,
            spdx_id="SPDXRef-" + str(0),
            download_location=SpdxNoAssertion()
        )

        self.master_doc.packages.append(package)

        # for doc in self.doc_list:
        #     check_sum = Checksum(ChecksumAlgorithm.SHA1, doc.creation_info.document_comment)
        #     doc_ref_id = "DocumentRef-" + doc.creation_info.spdx_id #is this how we want it?
        #     extDoc = ExternalDocumentRef(doc_ref_id, doc.creation_info.document_namespace, check_sum)
        #     self.master_doc.creation_info.external_document_refs.append(extDoc)
        for doc in self.doc_list:
            print(doc.comment)
            check_sum = Checksum(ChecksumAlgorithm.SHA1, doc.comment)
            doc_ref_id = "DocumentRef-" + doc.creation_info.spdx_id
            extDoc = ExternalDocumentRef(doc_ref_id, doc.creation_info.document_namespace, check_sum)
            self.master_doc.creation_info.external_document_refs.append(extDoc)
