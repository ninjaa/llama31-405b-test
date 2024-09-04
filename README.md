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

## Notes

There's a variety of prompts in the test-prompts folder. Each file has a different prompt that tests a different common input / output scenario. The locust report will report tokens per second for each test type, as well as a combined tokens per second stat. It's important to note that tokens per second varies depending on the number of input and output tokens.



