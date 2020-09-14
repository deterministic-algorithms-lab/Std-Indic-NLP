import os
import re


def execute(command):
    """
    Executes the command, exits, and doesn't execute any further command, if the current one fails
    """
    x = os.system(command)
    if x >> 8 != 0:
        exit(1)


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
