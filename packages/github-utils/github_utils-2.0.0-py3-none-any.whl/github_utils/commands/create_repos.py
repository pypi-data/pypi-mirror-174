import click
from github.GithubObject import NotSet


@click.command(name='create-repos')
@click.argument('name', nargs=-1, required=True)
@click.option('--description', help='Short description.', metavar='DESC', default=None)
@click.option('--homepage', help='URL with more information.', metavar='URL', default=None)
@click.option('--private', help='Private repository.', is_flag=True, default=True)
@click.option('--has-issues', help='With issues page.', is_flag=True, default=True)
@click.option('--has-wiki', help='With wiki page.', is_flag=True, default=True)
@click.option('--has-downloads', help='With downloads page.', is_flag=True, default=True)
@click.option('--auto-init', help='Create an initial commit.', is_flag=True, default=False)
@click.option('--gitignore_template', help='Apply .gitignore template.', metavar='LANG', default=None)
@click.pass_context
def command(ctx, name, **kwargs):
    """Create new repositories."""
    args = {k: v is None and NotSet or v for k, v in kwargs.items()}

    user = ctx.obj['github'].get_user()

    for repo_name in name:
        user.create_repo(repo_name, **args)
