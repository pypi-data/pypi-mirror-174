import click


@click.command('list-repos')
@click.pass_context
def command(ctx):
    """List all repositories"""

    user = ctx.obj['github'].get_user()

    for repo in user.get_repos():
        print(repo.full_name)
