import argparse
from ...utils import extract_file, append_file
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
        "http://ufal.mff.cuni.cz/~ramasamy/parallel/data/v2/en-ta-parallel-v2.tar.gz",
        args.data_path,
    )

    # Unzip & Probably Clean dataset here, remember to delete files of previous pipeline step if delete_old is given.
    extract_file(os.path.join(args.data_path, "en-ta-parallel-v2.tar.gz"))

    # Transform the cleaned dataset to the standard format, in data_path/datai/
    data_path = os.path.join(args.data_path, "en-ta-parallel-v2")
    final_data_path = next_datai(args.data_path)
    
    for filename in sorted(os.listdir(data_path)):

        filepath = os.path.join(data_path, filename)

        if filename.endswith('.en'):
            append_file( filepath, 
                         os.path.join(final_data_path, 'para', 'en-ta.en'))
        if filename.endswith('.ta'):
            append_file( filepath, 
                         os.path.join(final_data_path, 'para', 'en-ta.ta'))
        if args.delete_old:
            os.remove(filepath)

    if args.merge:
        # Join datasets
        joiner(args.data_path, args.delete_old)
