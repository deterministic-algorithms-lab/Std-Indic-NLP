import os, shutil
import re
import tarfile, zipfile, gzip


def execute(command):
    """
    Executes the command, exits, and doesn't execute any further command, if the current one fails
    """
    x = os.system(command)
    if x >> 8 != 0:
        exit(1)


def get_all_files(directory):
    """
    Returns lists of paths and names all files in directory
    """
    names = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    paths = [os.path.join(directory, f) for f in names]
    return paths, names


def shuf_mono(filename):
    """
    Shuffles a monolingual file
    """
    assert os.path.isfile(filename)


def shuf_pll(lg_pair: str, para_folder):
    """
    Shuffles parallel language data files
    """
    lgs = lg_pair.split("-")
    assert os.path.isfile(
        os.path.join(para_folder, lg_pair + "." + lgs[0])
    ) and os.path.isfile(os.path.join(para_folder, lg_pair + "." + lgs[1]))


def get_lang(filename):
    """
    To get language from filename
    """
    if len(filename) >= 8 and bool(re.match(r"..-..\...", filename[-8:])):
        return filename[-2] + filename[-1]
    if len(filename) >= 7 and bool(re.match(r"..\.mono", filename[-7:])):
        return filename[-7] + filename[-6]
    raise ValueError(
        "Filename "
        + filename
        + " should end with a string of form 'lg.mono' or 'lg-lg.lg' to be processed."
    )


def extract_file(filepath, dir=None) -> List[str]:
    """
    Extracts the file at 'filepath' to the directory passed in 'dir';
    Can only extract .tar.gz ; .tar; .gz and .zip files
    Returns List to paths to all files in final extracted file.
    """
    if dir is None:
        dir, filename = os.path.split(filepath)

    if not os.path.isdir(dir):
        os.makedirs(dir)

    if filepath.endswith(".tar.gz") or filepath.endswith(".tgz"):
        tar = tarfile.open(filepath, "r:gz")
        tar.extractall(dir)
        extracted_files = [
            os.path.join(dir, elem)
            for elem in tar.getnames()
            if os.path.isfile(os.path.join(dir, elem))
        ]
        tar.close()
        return extracted_files

    elif filepath.endswith(".tar"):
        tar = tarfile.open(filepath, "r")
        tar.extractall(dir)
        extracted_files = [
            os.path.join(dir, elem)
            for elem in tar.getnames()
            if os.path.isfile(os.path.join(dir, elem))
        ]
        tar.close()
        return extracted_files

    elif filepath.endswith(".zip"):
        zip = zipfile.ZipFile(filepath, "r")
        zip.extractall(dir)
        extracted_files = [
            os.path.join(dir, elem)
            for elem in zip.namelist()
            if os.path.isfile(os.path.join(dir, elem))
        ]
        zip.close()
        return extracted_files

    elif filepath.endswith(".gz"):
        gz = gzip.open(filepath)
        store_at = os.path.join(dir, filename[:-3])
        with open(store_at, "wb") as f:
            shutil.copyfileobj(gz, f)
        gz.close()
        return [os.path.join(dir, filename[:-3])]


# Adapted from https://superuser.com/questions/127786/efficiently-remove-the-last-two-lines-of-an-extremely-large-text-file
def remove_trailing_newline(file):
    """
    Removes multiple trailing newlines from the End of File
    """
    count = 0
    with open(file, "r+b", buffering=0) as f:
        f.seek(0, os.SEEK_END)
        while f.tell() > 0:
            f.seek(-1, os.SEEK_CUR)
            char = f.read(1)

            if char != b"\n":
                break

            count += 1
            f.seek(-1, os.SEEK_CUR)
            # Truncate all content in the file following and including the current location of file pointer.
            f.truncate()
    print("Removed " + str(count) + " lines from end of file.")


def append_file(src_file, tgt_file):
    """
    Appends src_file to tgt_file's end.
    """
    remove_trailing_newline(src_file)
    remove_trailing_newline(tgt_file)
    # cat is written in C , so faster. Will automatically create tgt_file, if it doesn't exist.
    command = "cat " + src_file + " >> " + tgt_file
    execute(command)


def join_files(directory, final_file, delete_old: bool = False):
    """
    Joins together all files directly under directory/ into a single file given by final_file
    """
    for f in os.listdir(directory):
        if os.path.isfile(f):
            append_file(os.path.join(directory, f), final_file)
            if delete_old:
                os.remove(os.path.join(directory, f))
