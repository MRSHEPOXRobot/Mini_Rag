from enum import Enum

class LLMEnums(Enum):
    #2 providers
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"


# ممكن Providers تانية يفرق معاها ال DocumentType
class DocumentTypeEnum(Enum): # علشان كده علمناها في class لوحدها
    DOCUMENT = "document"
    QUERY = "query"
