import time
from typing import Any
import json
import random

import openai
from openai import OpenAI

from ..types import MessageList, SamplerBase, SamplerResponse


class GroqChatCompletionSampler(SamplerBase):
    """
    Sample from OpenAI's chat completion API for o series models
    """

    def __init__(
        self,
        *,
        reasoning_effort: str | None = None,
        model: str = "o1-mini",
    ):
        self.api_key_name = "OPENAI_API_KEY"
        # self.client = OpenAI(base_url="http://10.66.1.238:8000/openai/v1")
        # self.client = OpenAI(base_url="http://10.66.1.237:8000/openai/v1")
        # self.client = OpenAI(base_url="http://10.66.219.209:8000/openai/v1")
        self.client = OpenAI(base_url="https://api.groq.com/openai/v1")
        # self.client = OpenAI(base_url="https://api.fireworks.ai/inference/v1")
        # using api_key=os.environ.get("OPENAI_API_KEY")  # please set your API_KEY
        self.model = model
        self.image_format = "url"
        self.reasoning_effort = reasoning_effort

    def _handle_image(
        self,
        image: str,
        encoding: str = "base64",
        format: str = "png",
        fovea: int = 768,
    ):
        new_image = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{format};{encoding},{image}",
            },
        }
        return new_image

    def _handle_text(self, text: str):
        return {"type": "text", "text": text}

    def _pack_message(self, role: str, content: Any):
        return {"role": str(role), "content": content}

    def __call__(self, message_list: MessageList) -> SamplerResponse:
        trial = 0
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=message_list,
                    reasoning_effort=self.reasoning_effort,
                    temperature=1.0,
                    top_p=1.0,
                    seed=random.randint(0, (1 << 31) - 1),
                    max_tokens=131072,
                )
                content = response.choices[0].message.content
                print('RESPONSE', json.dumps(content))
                return SamplerResponse(
                    response_text=content,
                    response_metadata={"usage": response.usage},
                    actual_queried_message_list=message_list,
                )
            # NOTE: BadRequestError is triggered once for MMMU, please uncomment if you are reruning MMMU
            except openai.BadRequestError as e:
                print("Bad Request Error", e)
                return SamplerResponse(
                    response_text="",
                    response_metadata={"usage": None},
                    actual_queried_message_list=message_list,
                )
            except Exception as e:
                exception_backoff = 2**trial  # expontial back off
                print(
                    f"Rate limit exception so wait and retry {trial} after {exception_backoff} sec",
                    e,
                )
                time.sleep(exception_backoff)
                trial += 1
            # unknown error shall throw exception
