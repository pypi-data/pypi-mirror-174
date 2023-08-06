from pathlib import Path

import click
from stochasticx.datasets.datasets import Datasets, Dataset
from stochasticx.utils.parse_utils import print_table

@click.group(name="datasets")
def datasets():
    pass


@click.command(name="ls")
def ls_datasets():
    click.secho("\n[+] Collecting all datasets\n", fg='blue', bold=True)
    
    columns, values = Datasets.get_datasets(fmt="table")
    print_table(columns, values)


@click.command(name="inspect")
@click.option('--id', required=True, help='Dataset ID')
def dataset_inspect(id):
    click.secho("\n[+] Collecting information from the dataset\n", fg='blue', bold=True)
    
    dataset = Datasets.get_dataset(id)
    click.echo(dataset.get_dataset_info())
    
    
@click.command(name="columns")
@click.option('--id', required=True, help='Dataset ID')
def dataset_columns(id):
    click.secho("\n[+] Collecting columns from the dataset\n", fg='blue', bold=True)
    
    dataset = Datasets.get_dataset(id)
    click.echo(dataset.get_column_names())
    
    
@click.command(name="download")
@click.option('--id', required=True, help='Dataset ID')
@click.option('--path', required=True, help='Path where the downloaded dataset will be saved')
def dataset_download(id, path):
    click.secho("\n[+] Downloading dataset\n", fg='blue', bold=True)
    dataset = Datasets.get_dataset(id)
    dataset.download(path)


@click.command(name="upload")
@click.option('--name', required=True, help='Path where the dataset to upload is located')
@click.option('--dir_path', required=True, help='Directory where the dataset to upload is located')
@click.option('--type', required=True, help='Dataset type. It should be hf, csv or json')
def dataset_upload(name, dir_path, type):
    type = type.strip()
    assert type in ["hf", "csv", "json"], "Dataset type should be hf, csv or json"
    dir_path = Path(dir_path)
    assert dir_path.exists(), "The directory path does not exist"
    
    dataset = Dataset(
        name=name,
        directory_path=dir_path,
        dataset_type=type
    )
    
    click.secho("\n[+] Uploading dataset...\n", fg='blue', bold=True)  
    dataset.upload()
    click.secho("\n[+] Dataset uploaded\n", fg='green', bold=True)


datasets.add_command(ls_datasets)
datasets.add_command(dataset_inspect)
datasets.add_command(dataset_download)
datasets.add_command(dataset_upload)
datasets.add_command(dataset_columns)