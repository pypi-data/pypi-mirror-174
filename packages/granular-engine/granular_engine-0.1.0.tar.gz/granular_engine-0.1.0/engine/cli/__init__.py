import os
import click
import json
from appdirs import user_config_dir

from engine import __version__ as version

from engine.connections import Callisto

from .project import project 
from .experiment import experiment

    
@click.group()
@click.version_option(version, message='%(version)s')
def cli():
    config_dir = user_config_dir('engine')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(os.path.join(config_dir, "config.json")):
        fout = open(os.path.join(config_dir, "config.json"), "w")
        json.dump({"host": None,
                    "org":  None, 
                   "email": None,   
                   "password": None, 
                   "cookie": None}, fout)
        fout.close()

@click.command()
@click.option('--host', required=False, type=str, 
                default='https://api.granular.ai', 
                help='Platform root address')
@click.option('--email', required=True, type=str,
                help='Email registered on GeoEngine')
@click.option('--password', required=True, type=str,
                help='Password registered in GeoEngine')
def login(host, email, password):
    """Login on GeoEngine platform

    Examples:

    \b
    $ engine login --email=EMAIL --password=PASSWORD
    """
    callisto = Callisto(email=email, password=password, host=host)

cli.add_command(login)
cli.add_command(project)
cli.add_command(experiment)


if __name__ == "__main__":
    cli()
