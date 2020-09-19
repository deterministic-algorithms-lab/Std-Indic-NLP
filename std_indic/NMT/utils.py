import os
from typing import List
from std_indic.utils import append_file, get_all_files, execute
import re
import random


def get_sorted_pair(lg_pair: str) -> str:
    """
    Takes in a string of form ".*(lg1-lg2).*" and returns a string of same form,
    with lg1 and lg2 sorted according to alphabetical order.
    """
    return re.sub("..-..", lambda st: "-".join(sorted(st.split("-"))), lg_pair)


def get_all_data(directory) -> List[str]:
    """
    Returns a list of all datai/ folders inside directory.
    """
    data_dirs = [
        f
        for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f))
        and (f.startswith("data") and len(f) > 4 and f[4:].isnumeric())
    ]
    data_dirs.sort(key=lambda f: int(f[4:]))
    return [os.path.join(directory, f) for f in data_dirs]


def make_std_fs(path):
    """
    Makes file structure for standard dataset, in the path directory;
    if it doesn't already exist.
    """
    assert os.path.split(path)[1].startswith(
        "data"
    ), '"path" must correspond to "data/" folder of standard file structure'

    if not os.path.isdir(path):
        os.makedirs(path)
    mono_path = os.path.join(path, "mono")
    para_path = os.path.join(path, "para")
    if not os.path.isdir(mono_path):
        os.makedirs(mono_path)
    if not os.path.isdir(para_path):
        os.makedirs(para_path)


def next_available(directory, append: bool = False):
    """
    Returns next available folder in the directory to store joining of data to.
    If append is true, then returns directory/data/, always
    """
    path = os.path.join(directory, "data")
    if not os.path.isdir(path) or append:
        make_std_fs(path)
        return path
    i = 0
    while True:
        path = os.path.join(directory, "data-join-" + str(i))
        if not os.path.isdir(path):
            make_std_fs(path)
            return path
        i = i + 1


def next_datai(directory) -> (int, str):
    """
    Returns next available 'datai/' folder store data into.
    """
    i = 0
    while True:
        data_dir = os.path.join(directory, "data" + str(i))
        if not os.path.isdir(data_dir):
            make_std_fs(data_dir)
            return i, data_dir
        i = i + 1


def joiner(
    directory, delete_old: bool = False, std_folders_lis: List[str] = None
) -> None:
    """
    Joins all data in datai/ or data/ standard dataset folders in the directory and stores in data/ folder.
    If std_folders_lis is provided, the folders in std_folders_lis are joined and put in directory/data/ or in directory/data-join-i/ .
    The files are appended to each other, in the order provided in std_folder_lis or in ascending order of i, for datai/.
    """
    assert os.path.isdir(directory)

    # Setting source and target folders
    if std_folders_lis is None:
        std_folders_lis = get_all_data(directory)
        tgt_dir = next_available(directory, append=True)
    else:
        tgt_dir = next_available(directory)

    for src_path in std_folders_lis:

        src_file_paths = (
            get_all_files(os.path.join(src_path, "mono"))[0]
            + get_all_files(os.path.join(src_path, "para"))[0]
        )

        for src_file in src_file_paths:

            base, filename = os.path.split(src_file)
            base, mono_para = os.path.split(base)
            tgt_file = os.path.join(tgt_dir, mono_para, filename)
            print("Appending ", src_file, " to ", tgt_file)
            append_file(src_file, tgt_file)
            if delete_old:
                os.remove(src_file)

    check_files(os.path.join(tgt_dir, mono_para))


def split_single_pll(
    filepath, lg1, lg2, target_dir=None, delimiter: str = "\\t"
) -> None:
    """
    Splits a single file having parallel data, into two files.

    :param lg1: Language of left column
    :param lg2: Language of right column
    """
    if target_dir is None:
        target_dir = os.path.split(filepath)[0]
    lg_first = min(lg1, lg2)
    lg_second = max(lg1, lg2)
    pair = lg_first + "-" + lg_second + "."
    command = (
        "cut -f1 -d"
        + delimiter
        + " "
        + filepath
        + " > "
        + os.path.join(target_dir, pair + lg1)
    )
    execute(command)
    command = (
        "cut -f2 -d"
        + delimiter
        + " "
        + filepath
        + " > "
        + os.path.join(target_dir, pair + lg2)
    )
    execute(command)


def have_same_lines(filepaths: List[str]) -> bool:
    """
    Returns true if both filepaths have same number of lines
    """
    file_sizes = []
    for filepath in filepaths:
        with open(filepath) as f:
            for i, l in enumerate(f):
                pass
            file_sizes.append(i + 1)
    return all(sz == file_sizes[0] for sz in file_sizes)


def get_pll_file(filename):
    """
    Returns the file having data parallel to that of filename
    """
    matches = re.match(r"(?:.*\.)*(..-..)\.(..).*", filename)
    lg_pair, cur_lg = matches.group(1), matches.group(2)
    pll_lang = [lg for lg in lg_pair.split("-") if lg != cur_lg][0]
    return re.sub(r"(?:.*\.)*(..-..)\.(..).*", r"\1." + pll_lang, filename)


def get_pll_pairs(para_dir) -> List[List[str]]:
    """
    Returns a list pairs of parallel files in para_dir.
    """
    lis = []
    for f in os.listdir(para_dir):
        if os.path.isfile(os.path.join(para_dir, f)):
            pair = set([f, get_pll_file(f)])
            print(pair)
            if pair not in lis:
                lis.append(pair)
    return lis


def check_files(para_dir) -> None:
    """
    Checks if all pairs of language files have same size.
    """
    lis = get_pll_pairs(para_dir)

    x = True
    for pair in lis:
        if not have_same_lines(pair):
            print(" does not have same line as ".join(pair))
            x = False
    if x:
        print("All parallel files in ", para_dir, "  are correct.")


def get_shuf_command() -> str:
    """
    Returns partial command for shuffling a pair of language files in same order.
    """
    command = "shuf --random-source=./rand "
    with open("./rand", "w+") as f:
        for i in range(10000000):
            f.write(str(random.randint(0, 2)) + "\n")
        print("Made new random file")
    return command


def shuf_pll(para_dir):
    """
    Shuffles parallel language data files in para_dir
    """
    lis = get_pll_pairs(para_dir)
    for pair in lis:
        command = get_shuf_command()
        for lg_file in pair:
            filepath = os.path.join(para_dir, lg_file)
            new_filepath = os.path.join(
                os.path.split(filepath)[0], "shuf." + os.path.split(filepath)[1]
            )
            to_execute = command + filepath + " > " + new_filepath
            execute(to_execute)
            to_execute = "rm " + filepath
            execute(to_execute)
            to_execute = "mv " + new_filepath + " " + filepath
            execute(to_execute)
            print("Shuffled : ", filepath)
