from cores import stdvarinit
from cores import fs
import urllib.request
class PlatformPackageManager(object):



    def install(self,spec,silent=False,force=False,):
        pa = stdvarinit.stdcache_dir + "/" + spec
        pas = stdvarinit.std_platform_dir + "/" + spec
        ud = "https://stduino-generic.pkg.coding.net/stduino_packages/stdplatforms/"+spec+".tar.gz?version=latest"

        urllib.request.urlretrieve(ud, pa)
        fs.untar_file(pa, pas)
        return True

    def uninstall(self):
        pass
    def update(self):
        pass

    pass
