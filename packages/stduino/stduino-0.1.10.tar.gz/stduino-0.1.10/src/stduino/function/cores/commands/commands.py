

# from cores.download import StdDownload

import click
from cores import stdvarinit
from cores import stdboards
from cores import stdrun
from cores import stdproject
from cores import stdplatform

# class Stduino(App):
#     class Meta:
#         label = 'stduino'
#         handlers = [
#             Base,
#             Project,
#             StdDownload,
#         ]

@stdvarinit.cli.group("Test", short_help="Test manager")
def cli():
    pass

@cli.command("test", short_help="Create a test")
@click.option('--name', prompt='Your name',help='The person to greet.')
@click.option('--output', '-o', multiple=True)
def test(name,output):
    print(name)
    print(output)
    click.echo('Hello %s!' % name)

    pass

@cli.command("pack", short_help="Create a tarball from a package")
@click.option('--name', prompt='Your name',help='The person to greet.')
@click.option('--output', '-o', multiple=True)
def pack(name,output):
    print(name)
    print(output)
    click.echo('Hello %s!' % name)
    click.echo('\n'.join(output))
    pass

# @cli.command()
# @click.option('--password', prompt=True, hide_input=True,
#               confirmation_prompt=False)#可验证
# def encrypt(password):
#     print(password)
    #click.echo('Encrypting password to %s' % password.encode('rot13'))




# with Stduino() as app:
#     app.run()
if __name__ == '__main__':
    stdvarinit.cli()

