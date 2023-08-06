""" PYPIPR Module """
from .idatetime import idatetime

"""PYTHON Standard Module"""
import datetime
import re
import subprocess
import platform
import pathlib
import urllib.request

from pypipr.idatetime import idatetime

WINDOWS = platform.system() == "Windows"
LINUX = platform.system() == "Linux"

if WINDOWS:
    import msvcrt as _getch


"""PYPI Module"""
import pytz
import colorama
import lxml.html

if LINUX:
    import getch as _getch


colorama.init()


class Pypipr:
    @staticmethod
    def test_print():
        """Print simple text to test this module is working"""
        print("Hello from PyPIPr")


def print_colorize(
    text,
    color=colorama.Fore.GREEN,
    bright=colorama.Style.BRIGHT,
    color_end=colorama.Style.RESET_ALL,
    text_start="",
    text_end="\n",
):
    """Print text dengan warna untuk menunjukan text penting"""
    print(f"{text_start}{color + bright}{text}{color_end}", end=text_end, flush=True)


def log(text):
    """
    Melakukan print ke console untuk menginformasikan proses yg sedang berjalan didalam program.
    """

    def inner_log(func):
        def callable_func(*args, **kwargs):
            print_log(text)
            result = func(*args, **kwargs)
            return result

        return callable_func

    return inner_log


def print_log(text):
    print_colorize(f">>> {text}")


def console_run(command):
    """Menjalankan command seperti menjalankan command di Command Terminal"""
    return subprocess.run(command, shell=True)


def input_char(prompt=None, prompt_ending="", newline_after_input=True):
    """Meminta masukan satu huruf tanpa menekan Enter. Masukan tidak ditampilkan."""
    if prompt:
        print(prompt, end=prompt_ending, flush=True)
    g = _getch.getch()
    if newline_after_input:
        print()
    return g


def input_char_echo(prompt=None, prompt_ending="", newline_after_input=True):
    """Meminta masukan satu huruf tanpa menekan Enter. Masukan akan ditampilkan."""
    if prompt:
        print(prompt, end=prompt_ending, flush=True)
    g = _getch.getche()
    if newline_after_input:
        print()
    return g


def datetime_now(timezone=None):
    """
    Datetime pada timezone tertentu
    """
    tz = pytz.timezone(timezone) if timezone else None
    return datetime.datetime.now(tz)
    # return datetime.datetime.now(zoneinfo.ZoneInfo(timezone))


def sets_ordered(iterator):
    """
    Hanya mengambil nilai unik dari suatu list
    """
    r = {i: {} for i in iterator}
    for i, v in r.items():
        yield i


def list_unique(iterator):
    """Sama seperti sets_ordered()"""
    return sets_ordered(iterator)


def chunck_array(array, size, start=0):
    """
    Membagi array menjadi potongan-potongan sebesar size
    """
    for i in range(start, len(array), size):
        yield array[i : i + size]


def regex_multiple_replace(data, regex_replacement_list):
    """
    Melakukan multiple replacement untuk setiap list.

    regex_replacement_list = [
        {"regex":r"", "replacement":""},
        {"regex":r"", "replacement":""},
        {"regex":r"", "replacement":""},
    ]
    """
    for v in regex_replacement_list:
        data = re.sub(v["regex"], v["replacement"], data)
    return data


def github_push(commit=None):
    def console(t, c):
        print_log(t)
        console_run(c)

    def console_input(prompt):
        print_colorize(prompt, text_end="")
        return input()

    console("Checking files", "git status")
    if commit:
        msg = commit
        print_colorize("Commit Message if any or empty to exit : ", text_end="")
        print(msg)
    else:
        msg = console_input("Commit Message if any or empty to exit : ")

    if msg:
        console("Mempersiapkan files", "git add .")
        console("Menyimpan files", f'git commit -m "{msg}"')
        console("Mengirim files", "git push")
        print_log("Finish")


def github_pull():
    print_log("Git Pull")
    console_run("git pull")


def file_get_contents(filename):
    """
    Membaca seluruh isi file ke memory.
    Apabila file tidak ada maka akan return None.
    Apabila file ada tetapi kosong, maka akan return empty string
    """
    try:
        f = open(filename, "r")
        r = f.read()
        f.close()
        return r
    except:
        return None


def file_put_contents(filename, contents):
    """
    Menuliskan content ke file.
    Apabila file tidak ada maka file akan dibuat.
    Apabila file sudah memiliki content maka akan di overwrite.
    """
    f = open(filename, "w")
    r = f.write(contents)
    f.close()
    return r


def create_folder(folder_name):
    """
    Membuat folder.
    Membuat folder secara recursive dengan permission.
    """
    pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)


def iscandir(folder_name=".", glob_pattern="*", recursive=True):
    """
    Mempermudah scandir untuk mengumpulkan folder, subfolder dan file
    """
    if recursive:
        return pathlib.Path(folder_name).rglob(glob_pattern)
    else:
        return pathlib.Path(folder_name).glob(glob_pattern)


def scan_folder(folder_name="", glob_pattern="*", recursive=True):
    """
    Hanya mengumpulkan nama-nama folder dan subfolder.
    Tidak termasuk [".", ".."].
    """
    p = iscandir(
        folder_name=folder_name,
        glob_pattern=glob_pattern,
        recursive=recursive,
    )
    for i in p:
        if i.is_dir():
            yield i


def scan_file(folder_name="", glob_pattern="*", recursive=True):
    """
    Hanya mengumpulkan nama-nama file dalam folder dan subfolder.
    """
    p = iscandir(
        folder_name=folder_name,
        glob_pattern=glob_pattern,
        recursive=recursive,
    )
    for i in p:
        if i.is_file():
            yield i


def html_get_contents(url, xpath=None, regex=None, css_select=None):
    """
    Mengambil content html dari url.

    Return :
    - String            : Apabila hanya url saja yg diberikan
    - List of etree     : Apabila xpath diberikan
    - False             : Apabila terjadi error
    """
    try:
        if xpath:
            return lxml.html.parse(urllib.request.urlopen(url)).findall(xpath)
        if regex:
            return re.findall(regex, urllib.request.urlopen(url).read().decode())
        if css_select:
            return (
                lxml.html.parse(urllib.request.urlopen(url))
                .getroot()
                .cssselect(css_select)
            )
        return urllib.request.urlopen(url).read().decode()
    except:
        return False


def url_get_contents(url, xpath=None):
    """
    Sama seperti html_get_contents()
    """
    return html_get_contents(url=url, xpath=xpath)


def get_filesize(filename):
    """
    Mengambil informasi file size dalam bytes
    """
    return pathlib.Path(filename).stat().st_size


def get_filemtime(filename):
    """
    Mengambil informasi file size dalam bytes
    """
    return pathlib.Path(filename).stat().st_mtime_ns


def datetime_from_string(*args, **kwargs):
    return idatetime(*args, **kwargs).to_datetime()
