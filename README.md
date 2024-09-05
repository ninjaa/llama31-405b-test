# Llama3.1 405B Load Test

## Instructions

1. Install dependencies:

- Python 3.11 or later

```bash
pip install locust faker tiktoken
```

- vllm and model weights for Llama 3.1 405B FP8 ("meta-llama/Meta-Llama-3.1-405B-Instruct-FP8" and "neuralmagic/Meta-Llama-3.1-405B-Instruct-FP8")

Instructions in this [post](https://medium.com/@aditya-advani/evaluating-self-hosted-llama-3-1-405b-fp8-performance-a0a494a2021a).

1. Run the load test:

```bash
./benchmark_llm.sh
```

## Options

You can customize the load test behavior using the following environment variables:

- `RUN_SHORT_PROMPTS_ONLY`: Set to "true" to run only short prompts (default: false)
- `SHORT_PROMPT_THRESHOLD`: Token threshold for short prompts (default: 5000)
- `RUN_LONG_PROMPTS_ONLY`: Set to "true" to run only long prompts (default: false)
- `LONG_PROMPT_THRESHOLD`: Token threshold for long prompts (default: 5000)
- `AI_MODEL_ID`: Specify the model ID to use (default: "meta-llama/Meta-Llama-3.1-405B-Instruct-FP8", alternate is "neuralmagic/Meta-Llama-3.1-405B-Instruct-FP8")
- `USE_SYSTEM_PROMPT`: Set to "true" to use a system prompt (default: false)
- `SYSTEM_PROMPT`: Specify the system prompt to use (default: "I am a helpful assistant")
- `TEMPERATURE`: Set the temperature for the model's output (default: 0)
- `DRY_RUN`: Set to "true" to run without making actual API calls (default: false)


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

Run with custom model, system prompt, and temperature:

```bash
AI_MODEL_ID=neuralmagic/Meta-Llama-3.1-405B-Instruct-FP8 USE_SYSTEM_PROMPT=true TEMPERATURE=0.0 ./benchmark_llm.sh classify short-haiku happy-dog-simple rag-recommendation
```

Run a dry run without making API calls:

```bash
DRY_RUN=true ./benchmark_llm.sh
```

Customize prompt thresholds:

```bash
SHORT_PROMPT_THRESHOLD=100 RUN_SHORT_PROMPTS_ONLY=true ./benchmark_llm.sh
```

```bash
LONG_PROMPT_THRESHOLD=10000 RUN_LONG_PROMPTS_ONLY=true ./benchmark_llm.sh
```


## Notes

There's a variety of prompts in the test-prompts folder. Each file has a different prompt that tests a different common input / output scenario. The locust report will report tokens per second for each test type, as well as a combined tokens per second stat. It's important to note that tokens per second varies depending on the number of input and output tokens.

Those results are presented in the article [Evaluating Self-Hosted Llama 3.1 405B (FP8) Performance](https://medium.com/@aditya-advani/evaluating-self-hosted-llama-3-1-405b-fp8-performance-a0a494a2021a).

Here's a table of prompts as of this writing, found by running `python count_prompt_tokens.py`

The summarize-book prompt and haystack-needle prompt have an entire book's worth of input appended to them. Those are no

```
Prompt Type                    Input Tokens Output Tokens
---------------------------------------------------------
classify-hard.json                      155             1
classify.json                           155             1
happy-dog-complex.json                   17           100
happy-dog-simple.json                    17           100
haystack-needle.json                 127504            50
rag-recommendation.json                 292           200
short-haiku.json                          7            50
summarize-book.json                  126087           500
thousand-word-essay.json                  7          1000
```

Raw results are available in the [results](./results) folder. Specifically look to the [combined-results.csv](./results/combined-results.csv) file.