import argparse
from ...utils import extract_file
from ..utils import joiner, next_datai
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
        help="If this flag isn't provided, new independent standard directory will be made for this dataset and it won't be joined within data/ folders in the data_path.",
    )

    parser.add_argument(
        "--delete_old",
        action="store_true",
        help="If this flag is provided, dataset from previous steps of pipeline will be deleted. Use this when you have less memory or huge dataset.",
    )

    parser.add_argument(
        "--langs",
        default="pa-hi-bn-or-gu-mr-kn-te-ml-ta",
        help="A '-' separated list of languages whose data is to be downloaded.",
    )
    args = parser.parse_args()

    final_data_path = next_datai(args.data_path)

    mono = args.langs.split("-")

    # Monolingual Part
    for lg in mono:

        urllib.request.urlretrieve(
            "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/data/monolingual/indicnlp_v1/sentence/"
            + lg
            + ".txt.gz",
            os.path.join(args.data_path, lg+'.txt.gz'),
        )

        # Unzip & Probably Clean dataset here, remember to delete files of previous pipeline step if delete_old is given.
        extract_file(
            os.path.join(args.data_path, lg + ".txt.gz"),
            os.path.join(final_data_path, "mono"),
        )

    if args.merge:
        # Join datasets
        joiner(args.data_path, args.delete_old)
