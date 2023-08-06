from subprocess import call
import click 

from engine.connections import Callisto
from engine.connections import Europa 


@click.group()
@click.pass_context
def project(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Preparing GeoEngine project for training')

@project.command()
@click.option('--org', required=False, type=str, 
                default=None, help='Organization from which tasks to show')
def ls(org):
    """List all the project available in GeoEngine

    Examples:

    \b
    $ engine project ls --org=ORG_SLUG
    """
    callisto = Callisto()
    if org:
        org_id = callisto.get_org_id_from_slug(org_slug=org)
        if org_id:
            europa = Europa(callisto, org_id)
            europa.get_projects()
    else:
        europa = Europa(callisto)
        europa.get_projects()
    return 

@project.command()
@click.option('--id', required=True, type=str, 
              default=None, help="ID of the project")
@click.option('--org', required=False, type=str, 
                default=None,  help='Organization from which tasks to show')
def describe(id, org):
    """Get details of a GeoEngine project

    Examples:

    \b
    $ engine project describe --id=ID --org=ORG_SLUG
    """
    callisto = Callisto()
    if org:
        org_id = callisto.get_org_id_from_slug(org_slug=org)
        if org_id:
            europa = Europa(callisto, org_id)
            europa.get_project_details(id)
    else:
        europa = Europa(callisto)
        europa.get_project_details(id)
    return

# @project.command()
# @click.option('--id', required=True, type=str, 
#               default=None, help="ID of the project")
# @click.option('--org', required=False, type=str, 
#                 default=None,  help='Organization from which tasks to show')
# def export(id, org):
#     """Export GeoEngine project

#     Examples:

#     \b
#     $ phobox project export --id=ID --org=ORG_SLUG
#     """
#     callisto = Callisto()
#     if org:
#         org_id = callisto.get_org_id_from_slug(org_slug=org)
#         if org_id:
#             europa = Europa(callisto, org)
#             europa.export_annotations(id)
#     else:
#         europa = Europa(callisto)
#         europa.export_annotations(id)


@project.command()
@click.option('--id', required=True, type=str, 
              default=None, help="ID of the project")
@click.option('--org', required=False, type=str, 
                default=None,  help='Organization from which tasks to show')
def exports(id, org):
    """Get exports of a GeoEngine project

    Examples:

    \b
    $ engine project datasets --id=ID --org=ORG_SLUG
    """
    callisto = Callisto()
    if org:
        org_id = callisto.get_org_id_from_slug(org_slug=org)
        if org_id:
            europa = Europa(callisto, org_id)
            europa.get_project_exports(id)
    else:
        europa = Europa(callisto)
        europa.get_project_exports(id)
    return