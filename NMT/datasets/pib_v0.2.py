import argparse
from ...utils import extract_file
from ..utils import joiner, next_datai
import urllib.request
import os, shutil

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

    # Download dataset
    urllib.request.urlretrieve(
        "http://preon.iiit.ac.in/~jerin/resources/datasets/pib_v0.2.tar.gz",
        args.data_path,
    )

    # Unzip & Probably Clean dataset here, remember to delete files of previous pipeline step if delete_old is given.
    extract_file(os.path.join(args.data_path, "pib_v0.2.tar.gz"))

    # Transform the cleaned dataset to the standard format, in data_path/datai/
    data_path = os.path.join(args.data_path, "pib_v0.2")
    final_data_path = next_datai(args.data_path)

    for root, dirs, files in os.walk(data_path):
        for f in files:
            filepath = os.path.join(root, f)
            new_filepath = os.path.join(
                final_data_path, "para", root.split("/")[-1] + "." + f.split(".")[-1]
            )
            if args.delete_old:
                os.rename(filepath, new_filepath)
            else:
                shutil.copyfile(filepath, new_filepath)

    if args.merge:
        # Join datasets
        joiner(args.data_path, args.delete_old)
