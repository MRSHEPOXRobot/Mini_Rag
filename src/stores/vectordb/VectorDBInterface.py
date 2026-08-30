from abc import ABC, abstractmethod # ABC==>Abstract Base Class
from typing import List # List for type hinting
#يعني الـ method دي المفروض ترجع List.
from models.db_schemes import RetrievedDocument
from typing import List

class VectorDBInterface(ABC):

    @abstractmethod # معناها ان اي كلاس هيرث مني لازم يوفر implementation لل mehtod دي
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> List:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str,
                          embedding_size: int,
                          do_reset: bool = False):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str, vector: list,
                   metadata: dict = None, #data about data
                   record_id: str = None):
        pass

    @abstractmethod
    #for batch insertion of multiple records into the vector database.
    # It takes a collection name, a list of texts, a list of corresponding vectors, optional metadata for each record, optional record IDs, and a batch size for insertion.
    def insert_many(self, collection_name: str, texts: list,
                    vectors: list, metadata: list = None,
                    record_ids: list = None, batch_size: int = 50):
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int) -> List[RetrievedDocument]: #هاتلي أقرب 5 vectors للـ query vector.
        pass
