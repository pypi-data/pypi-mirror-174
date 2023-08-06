import click
import json
import urllib.request


@click.command(name='create-repo')
@click.argument('name', required=True)
@click.option('--path', help='Path of repository.', metavar='PATH', default=None)
@click.option('--description', help='Short description.', metavar='DESC', default=None)
@click.option('--homepage', help='URL with more information.', metavar='URL', default=None)
@click.option('--private', help='Private repository.', is_flag=True, default=True)
@click.option('--has-issues', help='With issues page.', is_flag=True, default=True)
@click.option('--has-wiki', help='With wiki page.', is_flag=True, default=True)
@click.option('--can-comment', help='Can make comments.', is_flag=True, default=True)
@click.option('--auto-init', help='Create an initial commit.', is_flag=True, default=False)
@click.option('--gitignore-template', help='Apply .gitignore template.', metavar='LANG', default=None)
@click.option('--license-template', help='Apply license template.', metavar='LICENSE', default=None)
@click.pass_context
def command(ctx, **kwargs):
    kwargs['access_token'] = ctx.obj['access_token']

    req = urllib.request.Request(
        url='https://gitee.com/api/v5/user/repos',
        method='POST',
        headers={
            'Content-Type': 'application/json;charset=UTF-8'
        },
        data=bytes(json.dumps(kwargs).encode('utf-8'))
    )

    urllib.request.urlopen(req)
