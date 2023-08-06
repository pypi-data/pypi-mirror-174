from pathlib import Path
from typing_extensions import Required

import click
from stochasticx.models.models import Models, Model
from stochasticx.utils.parse_utils import print_table


@click.group(name="models")
def models():
    pass


@click.command(name="ls")
@click.option('--optimized', is_flag=True, help='Show only optimized models')
@click.option('--all', is_flag=True, help='Show all models')
def ls_models(optimized, all):
    if not optimized or all:
        if all:
            click.secho("\n[+] Collecting all models\n", fg='blue', bold=True)
        else:
            click.secho("\n[+] Collecting uploaded models\n", fg='blue', bold=True)
            
        columns, values = Models.get_models(fmt="table")
        print_table(columns, values)
    
    if optimized or all:
        if all:
            click.secho("\n[+] Collecting all models\n", fg='blue', bold=True)
        else:
            click.secho("\n[+] Collecting optimized models\n", fg='blue', bold=True)
            
        columns, values = Models.get_optimized_models(fmt="table")
        print_table(columns, values)


@click.command(name="inspect")
@click.option('--id', required=True, help='Model ID')
def model_inspect(id):
    click.secho("\n[+] Collecting information from this model\n", fg='blue', bold=True)
    
    model = Models.get_model(id)
    click.echo(model.get_model_info())
    
    
@click.command(name="download")
@click.option('--id', required=True, help='Model ID that you want to download')
@click.option('--path', required=True, help='Path where the downloaded model will be saved')
def model_download(id, path):
    click.secho("\n[+] Downloading the model\n", fg='blue', bold=True)
    model = Models.get_model(id)
    model.download(path)
    click.secho("\n[+] Model downloaded\n", fg='green', bold=True)


@click.command(name="upload")
@click.option('--name', required=True, help='Path where the model to upload is located')
@click.option('--dir_path', required=True, help='Directory where the model to upload is located')
@click.option('--type', required=True, help='Model type. It should be hf, pt or custom')
def model_upload(name, dir_path, type):
    type = type.strip()
    assert type in ["hf", "pt", "custom"], "Model type should be hf, pt or custom"
    dir_path = Path(dir_path)
    assert dir_path.exists(), "The directory path does not exist"
    
    model = Model(
        name=name,
        directory_path=dir_path,
        model_type=type
    )
    
    click.secho("\n[+] Uploading model...\n", fg='blue', bold=True)  
    model.upload()
    click.secho("\n[+] Model uploaded\n", fg='green', bold=True)


models.add_command(ls_models)
models.add_command(model_inspect)
models.add_command(model_download)
models.add_command(model_upload)