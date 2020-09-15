import argparse
from utils import joiner
import urllib.request

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_path",
        required=True,
        help="Path to directory where you want to store data, or path to existing data. data/ will be created or should exist inside this.",
    )

    parser.add_argument(
        "--exists",
        action="store_true",
        help="If this flag isn't provided, new independent standard directory will be made for this dataset.",
    )

    parser.add_argument(
        "--delete_old",
        action="store_true",
        help="If this flag is provided, dataset from previous steps of pipeline will be deleted. Use this when you have less memory or huge dataset.",
    )

    # Add other possible arguments

    args = parser.parse_args()

    # Download dataset
    urllib.request.urlretrieve("web_link", args.data_path)

    # Unzip & Probably Clean dataset here, remember to delete files of previous pipeline step if delete_old is given.

    # Transform the cleaned dataset to the standard format, in data_path/datai/

    if args.exists:
        # Join datasets
        joiner(args.data_path, args.delete_old)
