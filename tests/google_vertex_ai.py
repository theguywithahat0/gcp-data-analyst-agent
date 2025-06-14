# From: https://atamel.dev/posts/2024/08-12_deepeval_vertexai/
from typing import List
from deepeval.models.base_model import DeepEvalBaseLLM
from vertexai.generative_models import GenerationResponse, GenerativeModel

class GoogleVertexAI(DeepEvalBaseLLM):
    def __init__(
        self,
        model_name: str,
        project: str,
        location: str,
    ):
        self.model_name = model_name
        self.project = project
        self.location = location
        self.model = GenerativeModel(self.model_name)

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": 0}
        )
        return response.text

    async def a_generate(self, prompt: str) -> str:
        response = await self.model.generate_content_async(
            prompt,
            generation_config={"temperature": 0}
        )
        return response.text

    def get_model_name(self):
        return self.model_name 