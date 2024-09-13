import argparse
import random
import importlib
import pandas as pd
import os
import json
from rich.console import Console
from rich.table import Table

from scripts.connect_lm_studio import connect_lm_studio
import sys
import os


console = Console()

def load_dataset(dataset_name):
    """
    Load the specified dataset from the datasets directory.

    Parameters:
    dataset_name (str): Name of the dataset to load.

    Returns:
    list[dict]: List of data records.
    """
    dataset_path = os.path.join('datasets', dataset_name)
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")

    # Try loading different file formats
    file_formats = ['csv', 'parquet', 'json', 'xlsx', 'html']
    for file_format in file_formats:
        file_path = os.path.join(dataset_path, f'data.{file_format}')
        if os.path.exists(file_path):
            if file_format == 'csv':
                dataset = pd.read_csv(file_path)
            elif file_format == 'parquet':
                dataset = pd.read_parquet(file_path)
            elif file_format == 'json':
                dataset = read_json_file(file_path)
            elif file_format == 'xlsx':
                dataset = pd.read_excel(file_path)
            elif file_format == 'html':
                dataset = pd.read_html(file_path)[0]  # read_html returns a list of dataframes
            return dataset.to_dict(orient='records')

    raise FileNotFoundError(f"No suitable data file found in {dataset_path}")

def read_json_file(file_path):
    """
    Reads a JSON file with improved error handling.

    Parameters:
    file_path (str): Path to the JSON file.

    Returns:
    pd.DataFrame: DataFrame containing the JSON data.
    """
    data = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    console.print(f"[bold yellow]Skipping invalid JSON line in {file_path}[/bold yellow]")
        return pd.DataFrame(data)
    except Exception as e:
        console.print(f"[bold red]Error reading {file_path}: {e}[/bold red]")
        return None

def run_benchmark(benchmark_name, prompts, sample_size):
    """
    Run benchmark on the specified dataset using given prompts.

    Parameters:
    benchmark_name (str): Name of the benchmark dataset.
    prompts (list[str]): List of prompts to compare.
    sample_size (int): Number of samples to run from the benchmark dataset.
    """
    system_prompt = "You are an expert problem solver with a focus on reasoning, math, and logical problems. Your task is to provide clear and accurate solutions, step by step, ensuring logical consistency and correctness."
    
    dataset = load_dataset(benchmark_name)
    sample_data = random.sample(dataset, sample_size)
    results = {}
    
    for prompt in prompts:
        prompt_module = importlib.import_module(f'prompts.{prompt}')
        prompt_function = getattr(prompt_module, 'run_prompt')
        prompt_results = []
        
        for data in sample_data:
            result = connect_lm_studio(system_prompt, data['question'])
            prompt_results.append(result)
        
        results[prompt] = prompt_results
    
    results_dir = os.path.join('results', f'{benchmark_name}_results')
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = os.path.join(results_dir, f'{benchmark_name}_results.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    console.print(f"[bold green]Results saved to {results_file}[/bold green]")

def run_task(task, prompts):
    """
    Run a custom task using the given prompts.

    Parameters:
    task (str): Custom task to test the prompts.
    prompts (list[str]): List of prompts to compare.
    """
    results = {}
    
    for prompt in prompts:
        prompt_module = importlib.import_module(f'prompts.{prompt}')
        prompt_function = getattr(prompt_module, 'run_prompt')
        result = prompt_function(task)
        results[prompt] = result
    
    table = Table(title="Custom Task Results")
    table.add_column("Prompt", justify="left", style="cyan", no_wrap=True)
    table.add_column("Result", justify="left", style="magenta")

    for prompt, result in results.items():
        table.add_row(prompt, result)
    
    console.print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run benchmarks on different prompts or test prompts with a custom task",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--benchmark', type=str,
        help='Name of the benchmark dataset.\nAvailable datasets: gsmk8, last_word_concatination, multi_arithmetic, other_datasets'
    )
    parser.add_argument(
        '--prompts', type=str, nargs='+', required=True,
        help='List of prompts to compare.\nAvailable prompts: novel_prompt, cot_sc_prompt, cot_t_prompt, least2most_prompt, autocot_prompt, vanilla_prompt'
    )
    parser.add_argument(
        '--sample-size', type=int, default=10,
        help='Number of samples to run from the benchmark dataset (default: 10)'
    )
    parser.add_argument(
        '--task', type=str,
        help='Custom task to test the prompts. If provided, --benchmark is ignored.'
    )

    args = parser.parse_args()
    
    if args.task:
        run_task(args.task, args.prompts)
    elif args.benchmark:
        run_benchmark(args.benchmark, args.prompts, args.sample_size)
    else:
        parser.print_help()
        console.print("\n[bold red]Error: Either --benchmark or --task must be specified.[/bold red]")
