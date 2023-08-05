import json
import typer
import requests
from os import getenv
from typing import Optional
from pkg_resources import get_distribution, DistributionNotFound

LOCALSTACK_HOST = getenv('LOCALSTACK_HOST')
EDGE_PORT = getenv('EDGE_PORT', '4566')
AWS_LOCALSTACK_ENDPOINT = None

DML_ZONE = getenv('DML_ZONE', 'prod')
DML_REGION = getenv('DML_REGION', 'us-west-2')
DML_API_ENDPOINT = getenv('DML_API_ENDPOINT')

if DML_API_ENDPOINT is None:
    DML_API_ENDPOINT = 'https://api.{}-{}.daggerml.com'.format(DML_ZONE, DML_REGION)

if LOCALSTACK_HOST is not None:
    AWS_LOCALSTACK_ENDPOINT = 'http://{}:{}'.format(LOCALSTACK_HOST, EDGE_PORT)

try:
    __version__ = get_distribution("daggerml-cli").version
except DistributionNotFound:
    __version__ = 'local'

def api(data):
    return requests.post(DML_API_ENDPOINT, json=data).json()

def print_result(x, **kwargs):
    typer.echo(json.dumps(x, indent=2))
    if x['status'] != 'ok':
        raise typer.Exit(code=1)

def print_version(x):
    if x:
        typer.echo(__version__)
        raise typer.Exit(0)

app = typer.Typer(result_callback=print_result)

@app.command()
def login():
    return {'status': 'ok', 'result': 'foo'}

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=print_version,
        is_eager=True,
        help="Print daggerml version and exit."
    ),
    region: str = typer.Option(
        DML_REGION,
        help="The AWS region in which to execute. Defaults to DML_REGION environment variable."
    ),
    zone: str = typer.Option(
        DML_ZONE,
        help="The zone in which to execute. Defaults to DML_ZONE environment variable."
    )
):
    """
    DaggerML command line tool.
    """
    print('asdfasdfasdfasd')
    global DML_REGION, DML_ZONE
    DML_REGION, DML_ZONE = region, zone
    return
