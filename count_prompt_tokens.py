import json
import tiktoken
from pathlib import Path

PROMPT_DIR = Path(__file__).parent / "test-prompts"
TOKENIZER_NAME = "cl100k_base"


def count_tokens(text):
    tokenizer = tiktoken.get_encoding(TOKENIZER_NAME)
    return len(tokenizer.encode(text))


def main():
    for file in PROMPT_DIR.glob("*.json"):
        with open(file, 'r') as f:
            data = json.load(f)

        prompt = data.get('prompt', '')
        token_count = count_tokens(prompt)

        print(f"{file.name}: {token_count} tokens")


if __name__ == "__main__":
    main()
