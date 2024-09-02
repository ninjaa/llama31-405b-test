import logging
import os
import random
import json
from pathlib import Path
from unittest.mock import Mock

import tiktoken
from faker import Faker
from locust import HttpUser, between, events, task
import time

generator = Faker()

AI_MODEL_ID = os.getenv("AI_MODEL_ID",
                        "meta-llama/Meta-Llama-3.1-405B-Instruct-FP8")
TEMPERATURE = os.getenv("TEMPERATURE", 0)
TOKENIZER_NAME: str = "cl100k_base"


PROMPT_DIR = Path(__file__).parent / "test-prompts"
prompts = {}
for file in PROMPT_DIR.glob("*.json"):
    prompts[file.stem] = json.loads(file.read_text())

# Add command-line argument parsing
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"


class LlmTestUser(HttpUser):
    wait_time = between(0.05, 2)

    tokenizer = tiktoken.get_encoding(TOKENIZER_NAME)

    @task
    def predict(self) -> None:
        prompt_name, prompt_data = random.choice(list(prompts.items()))
        text = prompt_data['prompt']
        max_tokens = prompt_data.get('max_tokens')
        prompt_type = prompt_data['type']

        url = "/v1/completions"
        headers = {"Content-Type": "application/json"}

        model_id = AI_MODEL_ID
        self._count_tokens(text, "Input")
        num_chars = len(text)
        data = {
            "model": model_id,
            "prompt": text,
            "max_tokens": max_tokens,
            "temperature": TEMPERATURE,
        }

        logging.info(
            f"Sending text ({num_chars=}, {max_tokens=}, {model_id=}) to {url}...")
        logging.info(f"Data: {data}")
        start_time = time.time()

        if DRY_RUN:
            # Mock the API response
            mock_response = Mock()
            mock_response.text = "This is a mock response from the LLM."
            mock_response.raise_for_status = lambda: None
            response = mock_response
            logging.info("Dry run: Using mock response")
        else:
            response = self.client.post(url, headers=headers, json=data)

        end_time = time.time()
        try:
            response.raise_for_status()
            logging.info(f"Success: {response.text[:100]}")
            output_tokens = self._count_tokens(response.text, "Output")

            # Calculate tokens per second
            elapsed_time = end_time - start_time
            tokens_per_second = output_tokens / elapsed_time

            # Fire custom events for tokens per second and prompt type
            events.request.fire(
                request_type="TOKENS_PER_SECOND",
                name=f"Tokens/s - {prompt_type}",
                response_time=tokens_per_second,
                response_length=0,
                exception=None,
                context=self.context(),
            )
            events.request.fire(
                request_type="PROMPT_TYPE",
                name=f"Prompt Type - {prompt_type}",
                response_time=1,
                response_length=0,
                exception=None,
                context=self.context(),
            )
        except Exception:
            logging.exception(f"Error: {response.text}")

    def _count_tokens(self, text: str, token_type: str) -> int:
        token_count = len(self.tokenizer.encode(text))
        events.request.fire(
            request_type="TOKEN_COUNT",
            name=f"{token_type} Tokens",
            response_time=token_count,
            response_length=0,
            exception=None,
            context=self.context(),
        )
        return token_count
