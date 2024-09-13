
# RDoLT Prompting Benchmark

This repository provides a framework for benchmarking various prompt techniques on different datasets using large language models (LLMs). The project includes scripts to run benchmarks, load datasets, and evaluate prompt performance.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Running Benchmarks](#running-benchmarks)
  - [Running Custom Tasks](#running-custom-tasks)
  - [Available Prompts](#available-prompts)
  - [Available Datasets](#available-datasets)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/RDoLT_Prompting.git
    cd RDoLT_Prompting
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running Benchmarks

To run benchmarks on a specific dataset using a list of prompts, use the following command:

```bash
python benchmarks/run_benchmark.py --benchmark <dataset_name> --prompts <prompt1> <prompt2> ... --sample-size <number_of_samples>
```

**Arguments**:

- `--benchmark`: Name of the benchmark dataset (other benchmarks can be added in folder).
- `--prompts`: List of prompts to compare.
- `--sample-size`: Number of samples to run from the benchmark dataset (default: 10).

**Example**:

```bash
python benchmarks/run_benchmark.py --benchmark gsmk8 --prompts novel_prompt_v1 cot_sc_prompt --sample-size 5
```

### Running Custom Tasks

To run a custom task using a list of prompts, use the following command:

```bash
python benchmarks/run_benchmark.py --task "<custom_task>" --prompts <prompt1> <prompt2> ...
```

**Arguments**:

- `--task`: Custom task to test the prompts. If provided, `--benchmark` is ignored.
- `--prompts`: List of prompts to compare.

**Example**:

```bash
python benchmarks/run_benchmark.py --task "Solve the equation 2+2" --prompts novel_prompt_v2 cot_sc_prompt
python benchmarks/run_benchmark.py --task "2+2-3/4*8=?" --prompts cot_sc_prompt RDoLT_4Request
python benchmarks/run_benchmark.py --task "If a train travels at 60 miles per hour for 2 hours, and then at 80 miles per hour for another 3 hours, what is the total distance traveled by the train?" --prompts cot_sc_prompt RDoLT_4Request
```

### Available Prompts

The following prompts are available for comparison:

- `RDoLT_4Request` 
- `RDoLT_3Request`
- `RDoLT_Single.py`
- `cot_sc_prompt` (Chain of Thoughts-Self Consistancy)
- `cot_t_prompt` (Chain of Thoughts)
- `least2most_prompt`(Least-to-Most)
- `autocot_prompt` (Auto-CoT) 
- `vanilla_prompt` (Simple Input/Output)

### Available Datasets

The following datasets are available for benchmarking:

- `gsmk8`
- `last_word_concatination`
- `multi_arithmetic`
- `other_datasets`

## Examples

### Running a Benchmark with Custom Sample Size

```bash
python benchmarks/run_benchmark.py --benchmark gsmk8 --prompts novel_prompt_v1 cot_sc_prompt --sample-size 5
```

### Running a Custom Task

```bash
python benchmarks/run_benchmark.py --task "Solve the equation 2+2" --prompts novel_prompt_v2 cot_sc_prompt
```

## Project Structure

```bash
.
├── LICENSE
├── README.md
├── benchmarks
│   └── run_benchmark.py
├── datasets
│   ├── gsmk8
│   │   └── data.csv
│   ├── last_word_concatination
│   │   └── data.csv
│   ├── multi_arithmetic
│   │   └── data.csv
│   └── other_datasets
│       └── data.csv
├── prompts
│   ├── __init__.py
│   ├── autocot_prompt.py
│   ├── cot_sc_prompt.py
│   ├── cot_t_prompt.py
│   ├── least2most_prompt.py
│   ├── novel_prompt_v1.py
│   ├── novel_prompt_v2.py
│   └── vanilla_prompt.py
├── requirements.txt
├── results
│   ├── gsmk8_results
│   ├── last_word_concatination_results
│   ├── multi_arithmetic_results
│   └── other_results
├── scripts
│   ├── __init__.py
│   ├── connect_chatgpt.py
│   ├── connect_google_gemini_pro.py
│   ├── connect_lm_studio.py
│   └── connect_ollama.py
└── setup.py
```

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

