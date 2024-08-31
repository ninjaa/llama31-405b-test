import logging
import os
import random
from pathlib import Path

import tiktoken
from faker import Faker
from locust import HttpUser, between, events, task


generator = Faker()

AI_MODEL_ID = os.getenv("AI_MODEL_AUTH_TOKEN",
                        "meta-llama/Meta-Llama-3.1-405B-Instruct-FP8")

N_OUTPUT_TOKENS_MEAN = 250
N_OUTPUT_TOKENS_STD = 50
TEMPERATURE = os.getenv("TEMPERATURE", 0)
TOKENIZER_NAME: str = "cl100k_base"


PROMPT_DIR = Path(__file__).parent / "test-prompts"
prompts = []
for file in PROMPT_DIR.glob("*.txt"):
    prompts.append(file.read_text().strip())  # noqa: PERF401


class LlmTestUser(HttpUser):
    wait_time = between(0.05, 2)

    tokenizer = tiktoken.get_encoding(TOKENIZER_NAME)

    @task
    def predict(self) -> None:
        url = "/v1/completions"
        headers = {"Content-Type": "application/json"}

        model_id = AI_MODEL_ID
        text = random.choice(prompts)  # noqa: S311
        self._count_tokens(text, "Input")
        num_chars = len(text)
        max_tokens = int(random.normalvariate(
            N_OUTPUT_TOKENS_MEAN, N_OUTPUT_TOKENS_STD))

        data = {
            "model": model_id,
            "prompt": text,
            "max_tokens": max_tokens,
            "temperature": TEMPERATURE,
        }

        logging.info(
            f"Sending text ({num_chars=}, {max_tokens=}, {model_id=}) to {url}...")
        logging.info(f"Data: {data}")
        response = self.client.post(url, headers=headers, json=data)

        try:
            response.raise_for_status()
            logging.info(f"Success: {response.text[:100]}")
            self._count_tokens(response.text, "Output")
        except Exception:
            logging.exception(f"Error: {response.text}")

    def _count_tokens(self, text: str, token_type: str) -> None:
        token_count = len(self.tokenizer.encode(text))
        events.request.fire(
            request_type="TOKEN_COUNT",
            name=f"{token_type} Tokens",
            response_time=token_count,
            response_length=0,
            exception=None,
            context=self.context(),
        )
