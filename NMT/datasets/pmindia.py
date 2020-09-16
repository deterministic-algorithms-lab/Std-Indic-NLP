import argparse
from ...utils import extract_file, join_files
from ..utils import joiner, next_datai, split_single_pll
import urllib.request
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_path",
        required=True,
        help="Path to directory where you want to store data, or path to existing data. data/ will be created or should exist inside this.",
    )

    parser.add_argument(
        "--merge",
        action="store_true",
        help="If this flag isn't provided, new independent standard directory will be made for this dataset and it won't be joined within data/ folders in the data_path..",
    )

    parser.add_argument(
        "--delete_old",
        action="store_true",
        help="If this flag is provided, dataset from previous steps of pipeline will be deleted. Use this when you have less memory or huge dataset.",
    )

    args = parser.parse_args()

    final_data_path = next_datai(args.data_path)

    lg_pairs = [
        "as-en",
        "bn-en",
        "gu-en",
        "hi-en",
        "kn-en",
        "ml-en",
        "mni-en",
        "mr-en",
        "or-en",
        "pa-en",
        "ta-en",
        "te-en",
        "ur-en",
    ]
    mono = [
        "as",
        "bn",
        "en",
        "gu",
        "hi",
        "kn",
        "ml",
        "mni",
        "mr",
        "or",
        "pa",
        "ta",
        "te",
        "ur",
    ]

    # Monolingual Part
    for lg in mono:

        urllib.request.urlretrieve(
            "http://data.statmt.org/pmindia/v1/monolingual/pmindia.v1." + lg + ".tgz",
            os.path.join(args.data_path, "pmindia.v1." + lg + ".tgz"),
        )

        # Unzip & Probably Clean dataset here, remember to delete files of previous pipeline step if delete_old is given.
        extract_file(os.path.join(args.data_path, "pmindia.v1." + lg + ".tgz"))

        # Transform the cleaned dataset to the standard format, in data_path/datai/
        extracted_folder = os.path.join(args.data_path, "pmindia.v1." + lg)
        if lg == "mni":
            lg = "mp"  # For Manipuri
        join_files(
            extracted_folder,
            os.path.join(final_data_path, "mono", lg + ".mono"),
            args.delete_old,
        )

    # Parallel Part
    for pair in lg_pairs:

        urllib.request.urlretrieve(
            "http://data.statmt.org/pmindia/v1/parallel/pmindia.v1." + pair + ".tsv",
            os.path.join(args.data_path, "pmindia.v1." + pair + ".tsv"),
        )

        # Transform the cleaned dataset to the standard format, in data_path/datai/
        lg1, lg2 = pair.split("-")
        if lg2 == "mni":
            lg2 = "mp"  # For Manipuri

        tsv_path = os.path.join(args.data_path, "pmindia.v1." + pair + ".tsv")
        split_single_pll(tsv_path, lg2, lg1, os.path.join(final_data_path, "para"))

        if args.delete_old:
            os.remove(tsv_path)

    if args.merge:
        # Join datasets
        joiner(args.data_path, args.delete_old)
