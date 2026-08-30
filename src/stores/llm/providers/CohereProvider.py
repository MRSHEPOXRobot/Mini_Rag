from ..LLMInterface import LLMInterface
import cohere
import logging
from ..LLMEnums import CoHereEnums, DocumentTypeEnum


class CohereProvider(LLMInterface):# هنا هو بيتبع الlogic بتاع ال LLMInterface لكنه مش بيورثه

    def __init__(self, api_key: str,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        # api_url هيحول الريكويستات بدل ما تروح على Openai هتروح مثلاً على Ollama

        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        #read cohere docs to know how to use:
        self.client = cohere.Client(
            api_key=self.api_key
        )

        self.logger = logging.getLogger(__name__) #Define logger instance

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    # الفانكشن دي مش موجوده في ال interface علشان ممكن provider يستخدمها وأخر لا.
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip() #شيل المسافات او /n


    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None):
        if not self.client:
            self.logger.error("CoHere client was not set")# مفيش client
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for CoHere was not set")# مفيش generation model id
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message = self.process_text(prompt),

            max_tokens=max_output_tokens,
            temperature=temperature
        )


        if not response or not response.text:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message["content"]


    def embed_text(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error("CoHere client was not set")#logger error message
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for CoHere was not set")
            return None

        input_type = CoHereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CoHereEnums.QUERY.value

        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=['float']
        )
        #validate the response
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None

        return response.embeddings.float[0] #return embedding text vector of CoHere



    def construct_prompt(self, prompt: str, role: str):
        return {
                "role": role,
                "text": self.process_text(prompt)
            }
