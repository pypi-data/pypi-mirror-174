# -*- encoding: utf-8 -*-
import platform
from subprocess import getoutput
from os import getenv

os_type = None
os_arch = platform.machine()
os_ver = platform.release()
home_dir = getenv('HOME')
username = getenv('echo $USER')
uid = 1
if platform.system().lower() == 'linux':
	os_type = getoutput("""grep ^ID /etc/os-release | sed 's/ID=//' | sed -n 1p | sed 's#\"##g'""")
	os_ver = getoutput(cmd="""grep ^Min /etc/os-version | awk -F '=' '{print $2}'""")
	if str(os_type).lower() == 'kylin'.lower():
		os_ver = getoutput(cmd="""cat /etc/kylin-build | sed -n 2p | awk '{print $2}'""")
	uid = getoutput('echo $UID')
