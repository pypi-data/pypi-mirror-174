
from cores import stdvarinit
import os
import click
@stdvarinit.cli.group("project", short_help="project manager")
def cli():
    pass


# @cli.command("init", short_help="Create a project")
# @click.option('--project-dir','-d', help='target_path.')
# @click.option('--board', '-b', help='target_path.')
# @click.option("-O", "--project-option", multiple=True)
# def project_init(project_dir,board,project_option):
#     section = "env:%s" % board
#     print(section)
#     print(project_dir)
#     click.secho(project_dir, fg="cyan", nl=False)
#     click.echo('Hello %s!' % project_dir)
#     if boards.boards_search(board):
#         pass
#     else:
#
#         _install_platform(board)
#         pass

#cmd = self.pio_env + " project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework

@cli.command("init", short_help="Create a project")
@click.option('--project-dir','-d', help='target_path.')
@click.option('--board', '-b', help='target_path.')
@click.option("-O", "--project-option", multiple=True)
def stdproject_init(project_dir,board,project_option):
    stduino_framework("arduino",project_dir,board)


    click.echo(project_option)

    pass

def other_framework():
    pass
def update_project_env(project_dir, environment, project_option):
    if not project_option:
        return
    config = ProjectConfig(
        os.path.join(project_dir, "platformio.ini"), parse_extra=False
    )

    section = "env:%s" % environment
    if not config.has_section(section):
        config.add_section(section)

    for item in project_option:
        if "=" not in item:
            continue
        _name, _value = item.split("=", 1)
        config.set(section, _name.strip(), _value.strip())

    config.save()
def init_include_readme(include_dir):
    if not os.path.isdir(include_dir):
        os.makedirs(include_dir)
    with open(os.path.join(include_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for project header files.

A header file is a file containing C declarations and macro definitions
to be shared between several project source files. You request the use of a
header file in your project source file (C, C++, etc) located in `src` folder
by including it, with the C preprocessing directive `#include'.

```src/main.c

#include "header.h"

int main (void)
{
 ...
}
```

Including a header file produces the same results as copying the header file
into each source file that needs it. Such copying would be time-consuming
and error-prone. With a header file, the related declarations appear
in only one place. If they need to be changed, they can be changed in one
place, and programs that include the header file will automatically use the
new version when next recompiled. The header file eliminates the labor of
finding and changing all the copies as well as the risk that a failure to
find one copy will result in inconsistencies within a program.

In C, the usual convention is to give header files names that end with `.h'.
It is most portable to use only letters, digits, dashes, and underscores in
header file names, and at most one dot.

Read more about using header files in official GCC documentation:

* Include Syntax
* Include Operation
* Once-Only Headers
* Computed Includes

https://gcc.gnu.org/onlinedocs/cpp/Header-Files.html
""",
        )


def init_lib_readme(lib_dir):
    if not os.path.isdir(lib_dir):
        os.makedirs(lib_dir)
    with open(os.path.join(lib_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
待完善 更多信息请至wiki.stduino.com浏览
This directory is intended for project specific (private) libraries.
PlatformIO will compile them to static libraries and link into executable file.

The source code of each library should be placed in a an own separate directory
("lib/your_library_name/[here are source files]").

For example, see a structure of the following two libraries `Foo` and `Bar`:

|--lib
|  |
|  |--Bar
|  |  |--docs
|  |  |--examples
|  |  |--src
|  |     |- Bar.c
|  |     |- Bar.h
|  |  |- library.json (optional, custom build options, etc) https://docs.platformio.org/page/librarymanager/config.html
|  |
|  |--Foo
|  |  |- Foo.c
|  |  |- Foo.h
|  |
|  |- README --> THIS FILE
|
|- platformio.ini
|--src
   |- main.c

and a contents of `src/main.c`:
```
#include <Foo.h>
#include <Bar.h>

int main (void)
{
  ...
}

```

Stduino Library Dependency Finder will find automatically dependent
libraries scanning project source files.

More information about Stduino Library Dependency Finder
- https://docs.platformio.org/page/librarymanager/ldf.html
""",
        )


def init_test_readme(test_dir):
    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)
    with open(os.path.join(test_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for PlatformIO Unit Testing and project tests.

Unit Testing is a software testing method by which individual units of
source code, sets of one or more MCU program modules together with associated
control data, usage procedures, and operating procedures, are tested to
determine whether they are fit for use. Unit testing finds problems early
in the development cycle.

More information about PlatformIO Unit Testing:
- wiki.stduino.com
""",
        )

def init_std_ini(project_dir):
    pio_conetent = """
; Stduino Project Configuration File
;
;   Build options: build flags, source filter
;   Upload options: custom upload port, speed and extra flags
;   Library options: dependencies, extra library storages
;   Advanced options: extra scripting
;
; Please visit documentation for the other options and examples
; wiki.stduino.com

[env:w806duino]
platform = w806
platforms = stduino
board = w806
framework = arduino
debug_tool = cklink
upload_protocol = serial"""
    conf_path = os.path.join(project_dir, "stduino.ini")
    if os.path.isfile(conf_path):
        return
    with open(conf_path, mode="w", encoding="utf8") as fp:
        fp.write(pio_conetent)
    pass
def init_cvs_ignore(project_dir):

    conf_path = os.path.join(project_dir, ".gitignore")
    if os.path.isfile(conf_path):
        return
    with open(conf_path, mode="w", encoding="utf8") as fp:
        fp.write(".pio\n.std\n")
def init_main_other(main_dir):
    if not os.path.isdir(main_dir):
        os.makedirs(main_dir)
    conf_path = os.path.join(main_dir, "main.cpp")
    if os.path.isfile(conf_path):
        return
    main_content ="""

#include "header.h"

int main (void)
{

}
    """
    with open(conf_path, mode="w", encoding="utf8") as fp:
        fp.write(main_content)
def init_main_arduino(main_dir):
    if not os.path.isdir(main_dir):
        os.makedirs(main_dir)
    conf_path = os.path.join(main_dir, "main.cpp")
    if os.path.isfile(conf_path):
        return
    main_content = "\n".join(
        [
            "#include <Arduino.h>",
            "",
            "void setup() {",
            "  // put your setup code here, to run once:",
            "}",
            "",
            "void loop() {",
            "  // put your main code here, to run repeatedly:",
            "}",
            "",
        ]
    )
    with open(conf_path, mode="w", encoding="utf8") as fp:
        fp.write(main_content.strip())

def stduino_framework(framework,projects_dir,board):
    try:
        target_path = projects_dir
        # 大小写区分待解决 win下
        if not os.path.isdir(target_path):
            os.makedirs(target_path)
        # 大小写区分待解决 win下
        # if os.path.exists(target_path):
        #     pass
        # else:
        #     os.makedirs(target_path)
        #target_path = '"' + target_path + '"'
        #main_content = None
        if framework == "arduino":
            init_main_arduino(os.path.join(projects_dir, "src"))
            init_lib_readme(os.path.join(projects_dir, "lib"))
            init_test_readme(os.path.join(projects_dir, "test"))
            init_include_readme(os.path.join(projects_dir, "include"))
            init_cvs_ignore(projects_dir)
            init_std_ini(projects_dir)
            return True
        else:
            init_main_other(os.path.join(projects_dir, "src"))
            init_lib_readme(os.path.join(projects_dir, "lib"))
            init_test_readme(os.path.join(projects_dir, "test"))
            init_include_readme(os.path.join(projects_dir, "include"))
            init_cvs_ignore(projects_dir)
            init_std_ini(projects_dir)
            return True

        # if upload_m == "Disable":  # upload_m 调试前根据这个进行判断是否可以支持调试
        #     cmd = self.pio_env + " project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework
        # else:
        #     cmd = self.pio_env + " project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework + " -O debug_tool=" + upload_m
        #
        # # if upload_m=="Disable":#upload_m 调试前根据这个进行判断是否可以支持调试
        # #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework
        # # else:
        # #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework + " -O debug_tool=" + upload_m
        # #
        #
        # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        # for line in iter(proc.stdout.readline, b''):
        #     try:
        #         s1 = str(line, encoding='gbk')
        #     except:
        #         s1 = str(line)
        #     # print(s1)
        #     if not subprocess.Popen.poll(proc) is None:
        #         if line == "":
        #             break
        # proc.stdout.close()

        #return self.generate_project_main(framework)
    except:
        #stdinit.std_signal_gobal.stdprintln()
        return False

def _install_platform(board):
    pass

#self.pio_env + " project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework

    pass
if __name__ == '__main__':
    stdvarinit.cli()

