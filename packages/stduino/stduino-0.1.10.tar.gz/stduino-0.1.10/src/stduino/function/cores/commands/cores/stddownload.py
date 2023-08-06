from cores import stdvarinit
import os


import urllib.request
import tarfile
import requests


def tools_is_on_coding(self, name, file_url):
    try:
        file_url = "https://dl.bintray.com/platformio/tool-packages/" + file_url
        url = "https://stduino-generic.pkg.coding.net/stduino_packages/piopackages/" + name[8:]
        html = requests.head(url)  # 用head方法去请求资源头
        re = html.status_code

        if re == 200:

            mirror_file_size_str = html.headers['Content-Length']  # 提取出来的是个数字str

    except:
        return False
def untar_file(self, file, tarpath):
    t = tarfile.open(file)
    t.extractall(path=tarpath)
    pass

def down_test():
    pa = stdvarinit.stdcache_dir + "/stdplatforms.json"
    size=os.path.getsize(pa)
    print(size)
    print(pa)
    pas = stdvarinit.std_platform_dir + "/"# + self.app.pargs.name
    print(pas)
    ud="https://stduino-generic.pkg.coding.net/stduino_packages/stdplatforms/stdplatforms.json?version=latest"

    html = requests.head(ud)  # 用head方法去请求资源头
    re = html.status_code

    if re == 200:
        mirror_file_size_str = html.headers['Content-Length']  # 提取出来的是个数字str
        print(mirror_file_size_str)

    #urllib.request.urlretrieve(ud, pa)

# class StdDownload(Controller):
#     class Meta:
#         label = 'stddownload'
#         stacked_type = 'nested'
#         stacked_on = 'base'
#         arguments = [
#             (['-t'], {'help': 'type of package file', 'action': 'store', 'dest': 'type'}),
#             (['-n'], {'help': 'name of package file', 'action': 'store', 'dest': 'name'}),
#         ]
#     plat=None
#
#     @ex(hide=True)
#     def _default(self):
#         self.downfile()
#     def geturl(self):
#         if self.app.pargs.type=="platform":
#             print("plat")
#             return "https://stduino-generic.pkg.coding.net/stduino_packages/stdplatforms/" + self.app.pargs.name
#
#         else:
#             return "https://stduino-generic.pkg.coding.net/stduino_packages/stdpackages/" + self.app.pargs.name
#
#         pass
#     def downfile(self):
#
#         pa=stdvarinit.stdcache_dir+"/"+ self.app.pargs.name
#         pas = stdvarinit.std_platform_dir + "/" + self.app.pargs.name
#         ud="https://stduino-generic.pkg.coding.net/stduino_packages/piopackages/framework-lgt8fx-1.0.6.tar.gz?version=latest"
#         url=self.geturl()
#         urllib.request.urlretrieve(ud, pa)
#         self.untar_file(pa, pas)
#
#         # with zipfile.ZipFile(pa, mode="r") as f:
#         #     f.extractall(pas)
#
#     def untar_file(self,file,tarpath):
#         t = tarfile.open(file)
#         t.extractall(path=tarpath)
#         pass
#     def tar_file(self,tarfile,tarpath):
#         pass
#     def delfile(self):
#         pass


if __name__ == '__main__':
    down_test()

