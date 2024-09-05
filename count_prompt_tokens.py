import json
import tiktoken
from pathlib import Path

PROMPT_DIR = Path(__file__).parent / "test-prompts"
TOKENIZER_NAME = "cl100k_base"


def count_tokens(text):
    tokenizer = tiktoken.get_encoding(TOKENIZER_NAME)
    return len(tokenizer.encode(text))


def main():
    results = []
    for file in PROMPT_DIR.glob("*.json"):
        with open(file, 'r') as f:
            data = json.load(f)

        prompt = data.get('prompt', '')
        max_tokens = data.get('max_tokens', 0)

        input_tokens = count_tokens(prompt)

        results.append((file.name, input_tokens, max_tokens))

    # Sort results by filename
    results.sort(key=lambda x: x[0])

    # Print results in a neat table
    print(f"{'Filename':<30} {'Input Tokens':>12} {'Output Tokens':>13}")
    print("-" * 57)
    for filename, input_tokens, output_tokens in results:
        print(f"{filename:<30} {input_tokens:>12} {output_tokens:>13}")


if __name__ == "__main__":
    main()
