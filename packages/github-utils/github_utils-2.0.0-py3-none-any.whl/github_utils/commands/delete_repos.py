import click


@click.command('delete-repos')
@click.argument('name', nargs=-1, default=None)
@click.option('--all', help='Delete all repositories.', is_flag=True, default=False)
@click.pass_context
def command(ctx, name, all):
    """Delete existing repositories"""
    user = ctx.obj['github'].get_user()

    if all:
        for repo in user.get_repos():
            repo.delete()
    else:
        if name is None:
            raise Exception('Not repository specified.')

        for repo_name in name:
            user.get_repo(repo_name).delete()
