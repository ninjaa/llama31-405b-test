import json
import tiktoken
from pathlib import Path

PROMPT_DIR = Path(__file__).parent / "test-prompts"
TOKENIZER_NAME = "cl100k_base"
BOOK_PATH = PROMPT_DIR / "full-book.txt"

MAX_CONTEXT_LENGTH = 131072  # Maximum context length for the model
RESERVE_TOKENS = 5000  # Reserve some tokens for the prompt and completion

def count_tokens(text):
    tokenizer = tiktoken.get_encoding(TOKENIZER_NAME)
    return len(tokenizer.encode(text))

def main():
    results = []
    tokenizer = tiktoken.get_encoding(TOKENIZER_NAME)
    
    # Read and truncate book content
    book_content = ""
    if BOOK_PATH.exists():
        with open(BOOK_PATH, 'r') as book_file:
            full_book = book_file.read()
        max_book_tokens = MAX_CONTEXT_LENGTH - RESERVE_TOKENS
        book_content = tokenizer.decode(tokenizer.encode(full_book)[:max_book_tokens])

    # Add Tennyson quote to the middle of the book
    sentences = book_content.split('.')
    mid_point = len(sentences) // 2
    sentences.insert(mid_point, "Into the valley of Death rode the six hundred.")
    modified_book_content = '. '.join(sentences)

    for file in PROMPT_DIR.glob("*.json"):
        with open(file, 'r') as f:
            data = json.load(f)

        prompt = data.get('prompt', '')
        max_tokens = data.get('max_tokens', 0)

        # Add book content to relevant prompts
        if file.stem == 'summarize-book' and book_content:
            prompt += f"\n\nBook content:\n{book_content}"
        elif file.stem == 'haystack-needle' and book_content:
            prompt += f"\n\nBook content:\n{modified_book_content}"

        input_tokens = count_tokens(prompt)

        results.append((file.name, input_tokens, max_tokens))

    # Sort results by filename
    results.sort(key=lambda x: x[0])

    # Print results in a neat table
    print(f"{'Prompt Type':<30} {'Input Tokens':>12} {'Output Tokens':>13}")
    print("-" * 57)
    for filename, input_tokens, output_tokens in results:
        print(f"{filename:<30} {input_tokens:>12} {output_tokens:>13}")

if __name__ == "__main__":
    main()
