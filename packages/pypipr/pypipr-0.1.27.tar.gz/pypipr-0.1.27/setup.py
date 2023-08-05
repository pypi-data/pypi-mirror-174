# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypipr']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0', 'lxml==4.7.1', 'pytz>=2022.4,<2023.0']

extras_require = \
{':platform_system == "Linux"': ['getch>=1.0,<2.0']}

setup_kwargs = {
    'name': 'pypipr',
    'version': '0.1.27',
    'description': 'The Python Package Index Project',
    'long_description': '# About\nThe Python Package Index Project (pypipr)\n\n\n# Setup\nInstall with pip\n```\npython -m pip install pypipr\n```\n\nImport with * for fastest access\n```\nfrom pypipr.pypipr import *\n```\n\nTest with\n```python\nPypipr.test_print()\n```\n\n\n# Pypipr Class\n`test_print()` memastikan module sudah terinstal dan dapat dijalankan\n\n```python\nPypipr.test_print()\n```\n\n\n# functions\n`sets_ordered()` Hanya mengambil nilai unik dari suatu list\n\n```python\narray = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]\nprint([i for i in sets_ordered(array)])\n```\n\n\n`list_unique()` sama seperti `sets_ordered()`\n\n```python\narray = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]\nprint([i for i in list_unique(array)])\n```\n\n\n`chunck_array()` membagi array menjadi potongan dengan besaran yg diinginkan\n\n```python\narray = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]\nprint([i for i in chunck_array(array, 5)])\n```\n\n\n`print_colorize()` print ke console dengan warna\n\n```python\nprint_colorize("Print some text")\n```\n\n\n`@Log()` / `Log decorator` akan melakukan print ke console. Mempermudah pembuatan log karena tidak perlu mengubah fungsi yg sudah ada. Berguna untuk memberikan informasi proses program yg sedang berjalan.\n\n```python\n@log("Calling some function")\ndef some_function():\n    ...\n    return\n```\n\n\n`print_log` akan melakukan print ke console. Berguna untuk memberikan informasi proses program yg sedang berjalan.\n\n```python\nprint_log("Standalone Log")\n```\n\n\n`input_char()` meminta masukan satu huruf tanpa menekan enter. Char tidak ditampilkan.\n\n```python\ninput_char("Input Char without print : ")\n```\n\n\n`input_char()` meminta masukan satu huruf tanpa menekan enter. Char ditampilkan.\n\n```python\ninput_char_echo("Input Char n : ")\n```\n\n\n`datetime_now()` memudahkan dalam membuat tanggal dan waktu untuk suatu timezone\n\n```python\ndatetime_now("Asia/Jakarta")\ndatetime_now("GMT")\ndatetime_now("Etc/GMT+7")\n```\n\n\n`WINDOWS` True apabila berjalan di platform Windows\n\n```python\nprint(WINDOWS)\n```\n\n\n`LINUX` True apabila berjalan di platform Linux\n\n```python\nprint(LINUX)\n```\n\n\n`file_put_contents()` membuat file kemudian menuliskan contents ke file. Apabila file memiliki contents, maka contents akan di overwrite.\n\n```python\nfile_put_contents("ifile_test.txt", "Contoh menulis content")\n```\n\n\n`file_get_contents()` membaca contents file ke memory.\n\n```python\nprint(file_get_contents("ifile_test.txt"))\n```\n\n\n`create_folder()` membuat folder secara recursive.\n\n```python\ncreate_folder("contoh_membuat_folder")\ncreate_folder("contoh/membuat/folder/recursive")\ncreate_folder("./contoh_membuat_folder/secara/recursive")\n```\n\n\n`iscandir()` scan folder, subfolder, dan file\n\n```python\nfor i in iscandir():\n    print(i)\n```\n\n\n`scan_folder()` scan folder dan subfolder\n\n```python\nfor i in scan_folder():\n    print(i)\n```\n\n\n`scan_file()` scan file dalam folder dan subfolder\n\n```python\nfor i in scan_file():\n    print(i)\n```\n\n\n`regex_multiple_replace()` Melakukan multiple replacement untuk setiap list regex. \n\n```python\nregex_replacement_list = [\n    {"regex": r"\\{\\{\\s*ini\\s*\\}\\}", "replacement": "itu"},\n    {"regex": r"\\{\\{\\s*sini\\s*\\}\\}", "replacement": "situ"},\n]\ndata = "{{ ini }} adalah ini. {{sini}} berarti kesini."\ndata = regex_multiple_replace(data, regex_replacement_list)\nprint(data)\n```\n\n\n`github_push()` simple github push\n\n```python\ngithub_push()\n```\n\n\n`github_pull()` simple github pull\n\n```python\ngithub_pull()\n```\n\n\n`html_get_contents()` Mengambil content html dari url\n\n```python\na = html_get_contents("https://google.com/", xpath="//a")\nfor i in a:\n    print(i.text)\n    print(i.attrib.get(\'href\'))\n```\n\n\n`get_filesize()` Mengambil informasi file size dalam bytes\n\n```python\nprint(get_filesize(__file__))\n```\n\n\n`get_filemtime()` Mengambil informasi last modification time file dalam nano seconds\n\n```python\nprint(get_filemtime(__file__))\n```\n',
    'author': 'ufiapjj',
    'author_email': 'ufiapjj@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
