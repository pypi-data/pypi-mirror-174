import requests
import json
import urllib.request
from shutil import rmtree
import os,stat
import tarfile
import glob
import re

def is_connected():
    try:
        requests.get("https://www.baidu.com", timeout=2)
    except:
        return False
    return True
def load_json(target_abs):
    try:
        fo = open(target_abs, mode='r', encoding='UTF-8')
        pio_boards =json.loads(fo.read())  # 字符串转json
        fo.close()  # cmd_args["cmd_rtlib"]
        return pio_boards
    except:
        return []

def path_endswith_ext(path, extensions):
    if not isinstance(extensions, (list, tuple)):
        extensions = [extensions]
    for ext in extensions:
        if path.endswith("." + ext):
            return True
    return False
def match_src_files(src_dir, src_filter=None, src_exts=None, followlinks=True):
    def _append_build_item(items, item, src_dir):
        if not src_exts or path_endswith_ext(item, src_exts):
            items.add(os.path.relpath(item, src_dir))

    src_filter = src_filter or ""
    if isinstance(src_filter, (list, tuple)):
        src_filter = " ".join(src_filter)

    matches = set()
    # correct fs directory separator
    src_filter = src_filter.replace("/", os.sep).replace("\\", os.sep)
    for (action, pattern) in re.findall(r"(\+|\-)<([^>]+)>", src_filter):
        items = set()
        for item in glob.glob(
            os.path.join(glob.escape(src_dir), pattern), recursive=True
        ):
            if os.path.isdir(item):
                for root, _, files in os.walk(item, followlinks=followlinks):
                    for f in files:
                        _append_build_item(items, os.path.join(root, f), src_dir)
            else:
                _append_build_item(items, item, src_dir)
        if action == "+":
            matches |= items
        else:
            matches -= items
    return sorted(list(matches))
#一次性打包整个根目录。空子目录会被打包。
#如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir,arcname="")#,


def untar_file(filename,tarpath):
    t = tarfile.open(filename)
    t.extractall(path=tarpath)



def fast_download(url,target_path):
    try:
        urllib.request.urlretrieve(url, target_path)
    except:
        return False
    return True

def remove_readonly(func, path, _):
    try:
        # "Clear the readonly bit and reattempt the removal"
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except:
        print("something wrong of file delete")


def delete_file(path):
    try:
        if os.path.isdir(path):
            try:
                rmtree(path, onerror=remove_readonly)
            except:
                print("something wrong of file delete")
        else:
            try:
                os.remove(path)
            except:
                try:
                    # shutil.rmtree(path, onerror=self.remove_readonly)
                    os.chmod(path, stat.S_IWRITE)
                    os.remove(path)
                except:
                    print("something wrong of file delete")
    except:
        print("something wrong of file delete")

if __name__ == '__main__':
    ss="C:/Users/debug/.stduino/platforms/w80x"
    name="C:/Users/debug/.stduino/platforms/w80x.tar.gz"
    make_targz(name,ss)