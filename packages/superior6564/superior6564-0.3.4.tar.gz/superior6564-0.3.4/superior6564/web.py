"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""
import requests
import os
import subprocess
import sys
from IPython.display import Image, display
import itertools


def get_info(package: str, mode: str = "print"):
    """
    Args:
        package (str): Name of package for getting info.
        mode (str): Mode of getting info ("print", "return" or "all").
    Description:
        get_info() gives information about the package.\n
        Before you can get info about the package, you have to download it.
    """
    package_show = subprocess.run([sys.executable, "-m", "pip", "show", package], capture_output=True, text=True)
    if package_show.stderr.split('\n')[0][:30] != "WARNING: Package(s) not found:":
        lines = package_show.stdout.split('\n')
        if mode == "print" or mode == "return" or mode == "all":
            if mode == "print" or mode == "all":
                for line in lines:
                    print(line)
            if mode == "return" or mode == "all":
                return lines
        else:
            print("Incorrect mode")
    else:
        print("Before you can get info about the package, you have to download it.")


def install_package(package: str, version: str = None, output: bool = True):
    """
    Args:
        package (str): Name of package.
        version (str|None): Version of package.
        output (bool): Info about process will be output or not.
    Description:
        install_package() installs package.
    """
    if version is None:
        if output:
            print(f"Trying to install package {package}...")
        install_output = subprocess.run([sys.executable, "-m", "pip", "install", package], capture_output=True, text=True)
        if install_output.stderr.split('\n')[0][:31] == "ERROR: Could not find a version" or install_output.stderr.split('\n')[0][:27] == "ERROR: Invalid requirement:":
            print("ERROR: Bad name.")
            print("Write the correct name of the package.")
        else:
            uprade_output = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], capture_output=True, text=True)
            if output:
                print(f"Package {package} installed.")
    else:
        if output:
            print(f"Trying to install package {package} with version {version}...")
        new_package = package + "==" + version
        install_output = subprocess.run([sys.executable, "-m", "pip", "install", new_package], capture_output=True, text=True)
        if install_output.stderr.split('\n')[0][:31] == "ERROR: Could not find a version" or install_output.stderr.split('\n')[0][:27] == "ERROR: Invalid requirement:":
            print("ERROR: Bad name or Bad version.")
            print("Write the correct name or version.")
        else:
            if output:
                if install_output.stdout.split('\n')[0][:29] == "Requirement already satisfied":
                    print(f"Package {package} with version {version} is already installed.")
                elif install_output.stdout.split('\n')[0][:10] == "Collecting":
                    print(f"Package {package} with version {version} installed.")


def install_list_packages(packages, versions=None, output: bool = True):
    """
    Args:
        packages (list): List of packages. List of strings.
        versions (list): Versions of packages. List of strings.
        output (bool): Info about process will be output or not.
    Description:
        install_list_packages() installs packages.
    """
    for i in range(len(packages)):
        if versions is None:
            install_package(package=packages[i], output=output)
            if output:
                print(f"Status: {i + 1} of {len(packages)}.")
                print()
        else:
            install_package(package=packages[i], version=versions[i], output=output)
            if output:
                print(f"Status: {i + 1} of {len(packages)}.")
                print()


def pip_upgrade(version: str = None, output: bool = True):
    """
    Args:
        version (str): The version of PIP you need.
        output (bool): Info about process will be output or not.
    Description:
        pip_upgrade() upgrades pip.
    """
    if version is None:
        if output:
            print("Trying to upgrade PIP...")
        pip_version = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True).stdout.split('\n')[0][4:8]
        if output:
            print(f"Version before upgrading is {pip_version}.")
        upgrade_pip = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True, text=True)
        pip_version = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True).stdout.split('\n')[0][4:8]
        if output:
            print(f"Version after upgrading is {pip_version}.")
    else:
        if output:
            print(f"Trying to upgrade PIP with version {version}...")
        pip_version = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True).stdout.split('\n')[0][4:8]
        if output:
            print(f"Version before upgrading is {pip_version}.")
        upgrade_pip = subprocess.run([sys.executable, "-m", "pip", "install", "pip==" + version], capture_output=True, text=True)
        if output and upgrade_pip.stdout.split("\n")[2][:39] == "[notice] A new release of pip available":
            print(upgrade_pip.stdout.split("\n")[2])
        pip_version = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True).stdout.split('\n')[0][4:8]
        if output:
            print(f"Version after upgrading is {pip_version}.")


def show_degget():
    """
    Description:
        show_degget() shows image of degget.
    """
    with open("degget_elite.jpg", "wb") as f:
        f.write(requests.get('https://raw.githubusercontent.com/Superior-GitHub/superior6564/main/superior6564/degget_elite.jpg').content)

    display(Image(filename="degget_elite.jpg"))


def gen_ru_words(letters: str = "лупогр", length_of_words: int = 3, mode: str = "Fast", printed: bool = True):
    """
    Args:
        letters (str): All the letters which do you have.
        length_of_words (int): Length of words which do you need.
        mode (str): "Fast" - outputs without an "ё"; "Slow" - outputs with an "ё".
        printed (bool): print result or not (True or False).
    Description:
        gen_ru_words() generates RU words.
    """

    if mode == "Fast":
        with open("russian_nouns_without_io.txt", "wb") as f:
            f.write(requests.get('https://raw.githubusercontent.com/Superior-GitHub/superior6564/main/superior6564/russian_nouns_without_io.txt').content)

        with open('russian_nouns_without_io.txt', encoding='utf-8') as f1:
            list_of_ru_words = []
            number_of_words_txt = 51301
            for j in range(number_of_words_txt):
                if j != (number_of_words_txt - 1):
                    list_of_ru_words.append(f1.readline()[0:-1])
                else:
                    list_of_ru_words.append(f1.readline()[0:])
            result = ""
            result += f"Words from {length_of_words} letters:\n"
            words = set(itertools.permutations(letters, r=length_of_words))
            count_2 = 1
            for word in words:
                count = 0
                generate_word = "".join(word)
                for j in range(len(list_of_ru_words)):
                    if generate_word == list_of_ru_words[j] and count == 0:
                        result += f"{count_2} word: {generate_word}\n"
                        count += 1
                        count_2 += 1
    elif mode == "Slow":
        with open("russian_nouns.txt", "wb") as f:
            f.write(requests.get('https://raw.githubusercontent.com/Superior-GitHub/Superior6564/main/superior6564/russian_nouns.txt').content)

        with open('russian_nouns.txt', encoding='utf-8') as f1:
            list_of_ru_words = []
            list_of_ru_gen_words = []
            list_of_counts_of_words = []
            number_of_words_txt = 51301
            for j in range(number_of_words_txt):
                if j != (number_of_words_txt - 1):
                    list_of_ru_words.append(f1.readline()[0:-1])
                else:
                    list_of_ru_words.append(f1.readline()[0:])

            words = set(itertools.permutations(letters, r=length_of_words))
            count_2 = 1
            for word in words:
                count = 0
                generate_word = "".join(word)
                for j in range(len(list_of_ru_words)):
                    if generate_word == list_of_ru_words[j] and count == 0 and generate_word not in list_of_ru_gen_words:
                        list_of_counts_of_words.append(count_2)
                        list_of_ru_gen_words.append(generate_word)
                        count += 1
                        count_2 += 1
            if "е" in letters:
                letters = letters.replace("е", "ё")
                words = set(itertools.permutations(letters, r=length_of_words))
                for word in words:
                    count = 0
                    generate_word = "".join(word)
                    for j in range(len(list_of_ru_words)):
                        if generate_word == list_of_ru_words[j] and count == 0 and generate_word not in list_of_ru_gen_words:
                            list_of_counts_of_words.append(count_2)
                            list_of_ru_gen_words.append(generate_word)
                            count += 1
                            count_2 += 1

            with open("results_gen_ru_words.txt", "w", encoding='utf-8') as f2:
                result = ""
                result += f"Words from {length_of_words} letters:\n"
                for i in range(len(list_of_ru_gen_words)):
                    result += f"{list_of_counts_of_words[i]} слово: {list_of_ru_gen_words[i]}\n"
    result = f"Letters: {letters}.\n" + f"Length of words: {length_of_words}.\n" + f"Mode: {mode}.\n" + result
    if printed:
        print(result)
    return result.split("\n")
