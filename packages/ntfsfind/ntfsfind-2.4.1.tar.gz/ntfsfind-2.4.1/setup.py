# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ntfsfind']
install_requires = \
['mft>=0.5.6,<0.6.0', 'ntfsdump==2.4.0', 'pytsk3>=20211111,<20211112']

entry_points = \
{'console_scripts': ['ntfsfind = ntfsfind:entry_point']}

setup_kwargs = {
    'name': 'ntfsfind',
    'version': '2.4.1',
    'description': 'A tool for search paths from an NTFS volume on an image file.',
    'long_description': "# ntfsfind\n\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![PyPI version](https://badge.fury.io/py/ntfsfind.svg)](https://badge.fury.io/py/ntfsfind)\n[![Python Versions](https://img.shields.io/pypi/pyversions/ntfsfind.svg)](https://pypi.org/project/ntfsfind/)\n[![docker build](https://github.com/sumeshi/ntfsdump/actions/workflows/build-docker-image.yaml/badge.svg)](https://github.com/sumeshi/ntfsdump/actions/workflows/build-docker-image.yaml)\n\n![ntfsfind](https://gist.githubusercontent.com/sumeshi/c2f430d352ae763273faadf9616a29e5/raw/baa85b045e0043914218cf9c0e1d1722e1e7524b/ntfsfind.svg)\n\nA tool to search file/directory/ADS paths directly from NTFS image files.\n\n\n## Usage\n\nntfsfind can be invoked from the shell or run from a Python script.\n\n```bash\n$ ntfsfind {{query_regex}} /path/to/imagefile.raw\n```\n\n```python\nfrom ntfsfind import ntfsfind\n\n# imagefile_path: str\n# search_query: str\n# volume_num: Optional[int] = None\n# file_type: Literal['raw', 'e01', 'vhd', 'vhdx', 'vmdk'] = 'raw'\n# multiprocess: bool = False\n#\n# -> List[str]\n\nrecords = ntfsfind(\n    imagefile_path='./path/to/your/imagefile.raw',\n    search_query='.*\\.evtx',\n    volume_num=2,\n    file_type='raw',\n    multiprocess=False\n)\n\nfor record in records:\n    print(record)\n```\n\n\n### Query\n\nThis tool can search files/directories/ADS with regular expression queries.\nPaths are separated by slashes(Unix/Linux-Style), not backslashes(Windows-Style).\n\ne.g.\n```\nOriginal Path: C:\\$MFT\nQuery: '/\\$MFT'\n\n# find Eventlogs\nQuery: '.*\\.evtx'\n\n# find Alternate Data Streams\nQuery: '.*:.*'\n```\n\n\n### Example\n\nThis tool can extract and search $MFT information directly from image files(RAW, E01, VHD, VHDX, VMDK) with recorded NTFS volumes as follows.\n\n```.bash\n$ ntfsfind '.*\\.evtx' /path/to//imagefile.raw\nWindows/System32/winevt/Logs/Setup.evtx\nWindows/System32/winevt/Logs/Microsoft-Windows-All-User-Install-Agent%4Admin.evtx\nLogs/Windows PowerShell.evtx\nLogs/Microsoft-Windows-Winlogon%4Operational.evtx\nLogs/Microsoft-Windows-WinINet-Config%4ProxyConfigChanged.evtx\nLogs/Microsoft-Windows-Windows Firewall With Advanced Security%4ConnectionSecurity.evtx\nLogs/Microsoft-Windows-UserPnp%4ActionCenter.evtx\nLogs/Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Admin.evtx\nLogs/Microsoft-Windows-TerminalServices-LocalSessionManager%4Admin.evtx\nLogs/Microsoft-Windows-SMBServer%4Security.evtx\nLogs/Microsoft-Windows-SMBServer%4Connectivity.evtx\nLogs/Microsoft-Windows-SMBServer%4Audit.evtx\nLogs/Microsoft-Windows-SmbClient%4Security.evtx\nLogs/Microsoft-Windows-SMBClient%4Operational.evtx\nLogs/Microsoft-Windows-Shell-Core%4ActionCenter.evtx\nLogs/Microsoft-Windows-SettingSync%4Operational.evtx\n...\n\n```\n\n\n#### When use with [ntfsdump](https://github.com/sumeshi/ntfsdump)\n\nCombined with ntfsdump, the retrieved files can be dumped directly from the image file.\n\n```.bash\n$ ntfsfind '.*\\.evtx' /path/to/imagefile.raw | ntfsdump /path/to/your/imagefile\n```\n\nhttps://github.com/sumeshi/ntfsdump\n\n\n### Options\n\nThe tool supports the following options.\n\n```\n--help, -h:\n    show help message and exit.\n\n--version, -v:\n    show program's version number and exit.\n\n--volume-num, -n:\n    NTFS volume number (default: autodetect).\n\n--type, -t:\n    image file format (default: raw(dd-format)).\n    (raw|e01|vhd|vhdx|vmdk) are supported.\n\n--multiprocess, -m:\n    flag to run multiprocessing.\n```\n\n\n## Prerequisites\nThe image file to be processed must meet the following conditions.\n\n- File format is RAW, E01, VHD, VHDX, or VMDK.\n- The target volume is an NT file system(NTFS).\n- The target partition style is GUID partition table(GPT).\n\nAdditional file formats will be added in the future.  \nIf you have any questions, please submit an issue.  \n\n\n## Installation\n\n### via PyPI\n\n```\n$ pip install ntfsfind\n```\n\n## Run with Docker\nhttps://hub.docker.com/r/sumeshi/ntfsfind\n\n\n```bash\n$ docker run --rm -v $(pwd):/app -t sumeshi/ntfsfind:latest '/\\$MFT' /app/sample.raw\n```\n\n## Contributing\n\nThe source code for ntfsfind is hosted at GitHub, and you may download, fork, and review it from this repository(https://github.com/sumeshi/ntfsfind).  \nPlease report issues and feature requests. :sushi: :sushi: :sushi:\n\n\n## License\n\nntfsfind is released under the [LGPLv3+](https://github.com/sumeshi/ntfsfind/blob/master/LICENSE) License.\n\nPowered by following libraries.\n- [pytsk3](https://github.com/py4n6/pytsk)\n- [libewf](https://github.com/libyal/libewf)\n- [libvhdi](https://github.com/libyal/libvhdi)\n- [libvmdk](https://github.com/libyal/libvmdk)\n- [pymft-rs](https://github.com/omerbenamram/pymft-rs)\n",
    'author': 'sumeshi',
    'author_email': 'sum3sh1@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sumeshi/ntfsfind',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
