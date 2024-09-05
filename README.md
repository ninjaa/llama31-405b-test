# Llama3.1 405B Load Test

## Instructions

1. Install dependencies:

- Python 3.11 or later

```bash
pip install locust faker tiktoken
```

2. Run the load test:

```bash
./benchmark_llm.sh
```

## Options

You can customize the load test behavior using the following environment variables:

- `RUN_SHORT_PROMPTS_ONLY`: Set to "true" to run only short prompts (default: false)
- `SHORT_PROMPT_THRESHOLD`: Token threshold for short prompts (default: 5000)
- `RUN_LONG_PROMPTS_ONLY`: Set to "true" to run only long prompts (default: false)
- `LONG_PROMPT_THRESHOLD`: Token threshold for long prompts (default: 5000)

To run specific prompts, pass their names as arguments to the script:

```bash
./benchmark_llm.sh happy-dog-simple happy-dog-complex
```

## Examples

Run only short prompts:

```bash
RUN_SHORT_PROMPTS_ONLY=true ./benchmark_llm.sh
```

Run only long prompts:

```bash
RUN_LONG_PROMPTS_ONLY=true ./benchmark_llm.sh
```

Run specific prompts:

```bash
./benchmark_llm.sh happy-dog-simple happy-dog-complex
```

## Notes

There's a variety of prompts in the test-prompts folder. Each file has a different prompt that tests a different common input / output scenario. The locust report will report tokens per second for each test type, as well as a combined tokens per second stat. It's important to note that tokens per second varies depending on the number of input and output tokens.



