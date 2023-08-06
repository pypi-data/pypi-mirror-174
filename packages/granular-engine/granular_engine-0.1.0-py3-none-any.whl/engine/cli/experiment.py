from subprocess import call
import click 

from engine.connections import Callisto
from engine.connections import Dione 


@click.group()
@click.pass_context
def experiment(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Preparing GeoEngine project for training')

@experiment.command()
@click.option('--org', required=True, type=str, 
              help='Organization to which the project belongs')
@click.option('--projectid', required=True, type=str, 
              help='Project for which experiments to show')
def ls(org, projectid):
    """List all the experiments available for a project in GeoEngine

    Examples:

    \b
    $ engine experiments ls --projectId=PROJECT_ID --org=ORG_SLUG
    """
    print (projectid)
    callisto = Callisto()
    if org:
        org_id = callisto.get_org_id_from_slug(org_slug=org)
        if org_id:
            europa = Dione(callisto, org_id)
            europa.get_experiments(projectid)
    return 