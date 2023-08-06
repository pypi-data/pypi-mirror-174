import os
import time
from cores import stdvarinit
import click
from multiprocessing import cpu_count
import subprocess
try:
    DEFAULT_JOB_NUMS = cpu_count()
except NotImplementedError:
    DEFAULT_JOB_NUMS = 1

@stdvarinit.cli.group("run", short_help="run manager")
def cli():
    pass

@cli.command("build", short_help="Run project targets (build, upload, clean, etc.)")
@click.option("-e", "--environment", multiple=True)
@click.option("-t", "--target", multiple=True)
@click.option("--upload-port")
@click.option(
    "-d",
    "--project-dir",
    default=os.getcwd,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, writable=True, resolve_path=True
    ),
)
@click.option(
    "-c",
    "--project-conf",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
)
@click.option(
    "-j",
    "--jobs",
    type=int,
    default=DEFAULT_JOB_NUMS,
    help=(
        "Allow N jobs at once. "
        "Default is a number of CPUs in a system (N=%d)" % DEFAULT_JOB_NUMS
    ),
)
@click.option("-s", "--silent", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("--disable-auto-clean", is_flag=True)
@click.option("--list-targets", is_flag=True)
@click.pass_context
def build(
    ctx,
    environment,
    target,
    upload_port,
    project_dir,
    project_conf,
    jobs,
    silent,
    verbose,
    disable_auto_clean,
    list_targets,
):

    t1 = time.time()
    print(ctx,
    environment,
    target,
    upload_port,
    project_dir,
    project_conf,
    jobs,
    silent,
    verbose,
    disable_auto_clean,
    list_targets)
    os.chdir("C:/Users/debug/.stduino/packages/framework-arduino-w80x/tools/stduino/")  # 通过更改当前运行目录
    cmd = "C:/Users/debug/.stduino/packages/python3/python C:/Users/debug/.stduino/packages/framework-arduino-w80x/tools/stduino/test.py"
    cmd = "scons -Q -j 8"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in iter(proc.stdout.readline, b''):
        # s1 = str(line)#
        #line=str(line).replace("\\r", "").replace("\\n", "").replace("\\n", "")
        try:

            s1 = str(line, encoding='gbk')
        except:
            s1 = str(line)
        s1=s1.strip()
        print(s1)#
        # response = gdbmiparser.parse_response(s1)
        # print(response)
        #click.echo(s1)
        # print(s1)
        if not subprocess.Popen.poll(proc) is None:
            if line == "":
                break
    proc.stdout.close()
    t2 = time.time()
    click.echo("========================= [SUCCESS] Took %s seconds =========================" % str(int(t2 - t1)))
    pass

    #app.set_session_var("custom_project_conf", project_conf)


