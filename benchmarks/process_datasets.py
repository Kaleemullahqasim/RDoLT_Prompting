import pandas as pd
import os
import json
from rich.console import Console

console = Console()

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

def read_dataset(file_path):
    """
    Reads a dataset from various formats.

    Parameters:
    file_path (str): Path to the dataset file.

    Returns:
    pd.DataFrame: Dataset.
    """
    file_extension = os.path.splitext(file_path)[1]

    try:
        if file_extension == '.csv':
            dataset = pd.read_csv(file_path)
        elif file_extension == '.parquet':
            dataset = pd.read_parquet(file_path)
        elif file_extension == '.json':
            dataset = read_json_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        return dataset

    except Exception as e:
        console.print(f"[bold red]Error reading {file_path}: {e}[/bold red]")
        return None

def standardize_dataset(dataset):
    """
    Standardizes the dataset to ensure it has 'question' and 'answer' columns.

    Parameters:
    dataset (pd.DataFrame): Dataset to standardize.

    Returns:
    pd.DataFrame: Standardized dataset.
    """
    if 'question' not in dataset.columns:
        if 'Body' in dataset.columns:
            dataset.rename(columns={'Body': 'question'}, inplace=True)
        elif 'source' in dataset.columns:
            dataset.rename(columns={'source': 'question'}, inplace=True)
        else:
            dataset['question'] = 'Unknown Question'
    
    if 'answer' not in dataset.columns:
        if 'Answer' in dataset.columns:
            dataset.rename(columns={'Answer': 'answer'}, inplace=True)
        elif 'final_ans' in dataset.columns:
            dataset.rename(columns={'final_ans': 'answer'}, inplace=True)
        elif 'choices' in dataset.columns:
            dataset.rename(columns={'choices': 'answer'}, inplace=True)
        else:
            dataset['answer'] = 'Unknown Answer'

    return dataset[['question', 'answer']]

def read_and_standardize_datasets(directory):
    """
    Reads and standardizes datasets from a specified directory and its subdirectories.

    Parameters:
    directory (str): Path to the directory containing dataset files.
    """
    if not os.path.exists(directory):
        console.print(f"[bold red]Directory not found: {directory}[/bold red]")
        return

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.startswith('.'):
                continue  # Skip hidden files like .DS_Store

            file_path = os.path.join(root, file_name)
            dataset = read_dataset(file_path)
            if dataset is not None:
                console.print(f"\n[bold green]File: {file_path}[/bold green]")
                standardized_dataset = standardize_dataset(dataset)
                console.print(standardized_dataset.head())



# Example usage
if __name__ == "__main__":
    datasets_directory = '/Users/kaleemullahqasim/Desktop/RDoLT_Prompting/datasets'  # Update this with your actual datasets directory path
    read_and_standardize_datasets(datasets_directory)
