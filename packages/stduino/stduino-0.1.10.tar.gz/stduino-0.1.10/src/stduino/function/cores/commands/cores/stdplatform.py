import json
import click
from cores import stdvarinit
from cores import fs
import requests
import os
from cores.stdpackage import PlatformPackageManager
@stdvarinit.cli.group("platform", short_help="platform manager")
def cli():
    pass


@cli.command("search", short_help="Search for development platform")
@click.argument("query", required=False)
@click.option("--json-output", is_flag=True)
def platform_search(query, json_output):
    load_data = []
    stdplatforms_json = stdvarinit.session_dir + "/stdplatforms.json"
    url = "https://stduino-generic.pkg.coding.net/stduino_packages/stdplatforms/stdplatforms.json?version=latest"
    if os.path.isfile(stdplatforms_json):
        if fs.is_connected():
            html = requests.head(url)  # 用head方法去请求资源头
            if html.status_code == 200:
                online_size = int(html.headers['Content-Length'])  # 提取出来的是个数字str
                current_size = os.path.getsize(stdplatforms_json)
                if online_size==current_size:
                    load_data=fs.load_json(stdplatforms_json)
                    #click.echo()
                else:
                    fs.delete_file(stdplatforms_json)
                    fs.fast_download(url,stdplatforms_json)
                    load_data=fs.load_json(stdplatforms_json)
        else:
            load_data=fs.load_json(stdplatforms_json)

    else:
        if fs.is_connected():
            fs.fast_download(url, stdplatforms_json)
            load_data=fs.load_json(stdplatforms_json)
    if json_output:
        click.echo(json.dumps(load_data))
    else:
        _print_platforms(load_data)
    #json.dumps(pio_boards)

@cli.command("install", short_help="Install new development platform")
@click.option("--platform", '-p', help='target install platform.')
@click.option("-s", "--silent", is_flag=True, help="Suppress progress reporting")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Reinstall/redownload dev/platform and its packages if exist",
)
def platform_install(  # pylint: disable=too-many-arguments
    platform,
    silent,
    force,
):
    return _platform_install(
        platform,
        silent,
        force,
    )


def _platform_install(  # pylint: disable=too-many-arguments
    platforms,
    silent=False,
    force=False,
):
    print(platforms)
    pm = PlatformPackageManager()
    pkg = pm.install(
        spec=platforms,
        silent=silent,
        force=force,
    )
    if pkg and not silent:
        click.secho(
            "The platform '%s' has been successfully installed!\n"
            "The rest of the packages will be installed later "
            "depending on your build environment." % platforms,
            fg="green",
        )


@cli.command("install2", short_help="Install new development platform")
@click.argument("platforms", nargs=-1, required=True, metavar="[PLATFORM...]")
@click.option("--with-package", multiple=True)
@click.option("--without-package", multiple=True)
@click.option("--skip-default-package", is_flag=True)
@click.option("--with-all-packages", is_flag=True)
@click.option("-s", "--silent", is_flag=True, help="Suppress progress reporting")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Reinstall/redownload dev/platform and its packages if exist",
)
def platforms_install(  # pylint: disable=too-many-arguments
    platforms,
    with_package,
    without_package,
    skip_default_package,
    with_all_packages,
    silent,
    force,
):
    return _platform_install(
        platforms,
        with_package,
        without_package,
        skip_default_package,
        with_all_packages,
        silent,
        force,
    )


def _platforms_install(  # pylint: disable=too-many-arguments
    platforms,
    with_package=None,
    without_package=None,
    skip_default_package=False,
    with_all_packages=False,
    silent=False,
    force=False,
):
    #pm = PlatformPackageManager()
    for platform in platforms:
        pkg = pm.install(
            spec=platform,
            with_packages=with_package or [],
            without_packages=without_package or [],
            skip_default_package=skip_default_package,
            with_all_packages=with_all_packages,
            silent=silent,
            force=force,
        )
        if pkg and not silent:
            click.secho(
                "The platform '%s' has been successfully installed!\n"
                "The rest of the packages will be installed later "
                "depending on your build environment." % platform,
                fg="green",
            )

@cli.command("list", short_help="List all installed platforms")
@click.option("--json-output", is_flag=True)
def platform_list(json_output):
    platforms = []
    # pm = PlatformPackageManager()
    # for pkg in pm.get_installed():
    #     platforms.append(
    #         _get_installed_platform_data(pkg, with_boards=False, expose_packages=False)
    #     )
    #
    # platforms = sorted(platforms, key=lambda manifest: manifest["name"])
    if json_output:
        click.echo(json.dumps(platforms))
    else:
        print(platforms)

def _install_platform(board):
    pass

#self.pio_env + " project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework

def _print_platforms(platforms):
    for platform in platforms:
        click.echo(
            "{name} ~ {title}".format(
                name=click.style(platform["name"], fg="cyan"), title=platform["title"]
            )
        )
        click.echo("=" * (3 + len(platform["name"] + platform["title"])))
        click.echo(platform["description"])
        click.echo()
        if "homepage" in platform:
            click.echo("Home: %s" % platform["homepage"])
        if "frameworks" in platform and platform["frameworks"]:
            click.echo("Frameworks: %s" % ", ".join(platform["frameworks"]))
        if "packages" in platform:
            click.echo("Packages: %s" % ", ".join(platform["packages"]))
        if "version" in platform:
            if "__src_url" in platform:
                click.echo(
                    "Version: %s (%s)" % (platform["version"], platform["__src_url"])
                )
            else:
                click.echo("Version: " + platform["version"])
        click.echo()
    pass
if __name__ == '__main__':
    stdvarinit.cli()

