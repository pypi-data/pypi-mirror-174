from cores import stdvarinit
import json
from cores import fs
import requests
import os
import click
@stdvarinit.cli.group("boards", short_help="boards manager")
def cli():
    pass
@cli.command("installed", short_help="find board")
def boards_installed():
    pass



@cli.command("search", short_help="Search for development board")
@click.argument("query", required=False)
@click.option("--json-output", is_flag=True)
def board_search(query, json_output):
    load_data = []
    stdboards_json = stdvarinit.session_dir + "/stdboards.json"
    url = "https://stduino-generic.pkg.coding.net/stduino_packages/stdplatforms/stdboards.json?version=latest"
    if os.path.isfile(stdboards_json):
        if fs.is_connected():
            html = requests.head(url)  # 用head方法去请求资源头
            if html.status_code == 200:
                online_size = int(html.headers['Content-Length'])  # 提取出来的是个数字str
                current_size = os.path.getsize(stdboards_json)
                if online_size==current_size:
                    load_data=fs.load_json(stdboards_json)
                    #click.echo()
                else:
                    fs.delete_file(stdboards_json)
                    fs.fast_download(url,stdboards_json)
                    load_data=fs.load_json(stdboards_json)
        else:
            load_data=fs.load_json(stdboards_json)

    else:
        if fs.is_connected():
            fs.fast_download(url, stdboards_json)
            load_data=fs.load_json(stdboards_json)
    if json_output:
        click.echo(json.dumps(load_data))
    else:
        click.echo(json.dumps(load_data))
        pass
        #_#print_platforms(load_data)
    #json.dumps(pio_boards)
def test():
    target_path="C:/Users/debug/.stduino/platforms/dS1"
    if not os.path.isdir(target_path):
        print(0)
    else:
        from multiprocessing import cpu_count
        print(cpu_count())


# 大小写区分待解决 win下
if __name__ == '__main__':
    test()