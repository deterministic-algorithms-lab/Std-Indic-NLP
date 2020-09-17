import argparse
from std_indic.utils import extract_file, append_file
from std_indic.NMT.utils import next_datai, joiner
import os
import opustools

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
        "--pll_langs",
        default="en-pa,en-hi,bn-en,en-or,en-gu,en-mr,en-kn,en-te,en-ml,en-ta,\
                       hi-pa,bn-pa,or-pa,gu-pa,mr-pa,kn-pa,pa-te,ml-pa,ta-pa,\
                             bn-hi,hi-or,gu-hi,hi-mr,hi-kn,hi-te,hi-ml,hi-ta,\
                                   bn-or,bn-gu,bn-mr,bn-kn,bn-te,bn-ml,bn-ta,\
                                         gu-or,mr-or,kn-or,or-te,ml-or,or-ta,\
                                               gu-mr,gu-kn,gu-te,gu-ml,gu-ta,\
                                                     kn-mr,mr-te,ml-mr,mr-ta,\
                                                           kn-te,kn-ml,kn-ta,\
                                                                 ml-te,ta-te,\
                                                                       ml-ta",
        help="A comma separated list of language pair(lg1-lg2) whose data is to be downloaded.",
    )

    parser.add_argument(
        "--mono_langs",
        default="pa,hi,bn,or,gu,mr,kn,te,ml,ta,en",
        help="A comma separated list of languages whose data is to be downloaded.",
    )

    parser.add_argument(
        "--corpora",
        help="A comma separated list of corpora from which to download data. If not provided, all corpora would be searched.",
    )

    parser.add_argument(
        "--delete_metadata",
        help="If this flag is provided, metadata that comes with parallel files will be deleted.",
    )

    args = parser.parse_args()

    final_data_path = next_datai(args.data_path)[1]

    mono = args.mono_langs.split(",") if args.mono_langs != "" else []
    pll = args.pll_langs.split(",") if args.pll_langs != "" else []

    if corpora is None:
        corpora = [None]
    else:
        copora = args.corpora.split(",")

    # Monolingual Part
    for lg in mono:
        lg_files = []
        for directory in corpora:
            # Downloading
            mono_downloader = opustools.OpusGet(
                source=lg,
                preprocess="mono",
                directory=directory,
                download_dir=args.data_path,
                suppress_prompts=True,
            )
            corpora, file_n, total_size = mono_downloader.get_corpora_data()
            mono_downloader.download(corpora, file_n, total_size)
            downloaded_filenames = [mono_downloader.make_file_name(c) for c in corpora]

            # Extracting Files
            for filename in downloaded_filenames:
                lg_files += extract_file(os.path.join(args.data_path, filename))

        # Joining together files
        for filepath in lg_files:
            append_file(filepath, os.path.join(final_data_path, "mono", lg + ".mono"))

    # Parallel Part
    for lg_pair in pll:
        f_lang, s_lang = lg_pair.split("-")
        all_files = []

        for directory in corpora:

            # Downloading
            pll_downloader = opustools.OpusGet(
                source=f_lang,
                target=s_lang,
                preprocess="moses",
                directory=directory,
                download_dir=args.data_path,
                suppress_prompts=True,
            )
            data = pll_downloader.get_response(pll_downloader.url)
            c_size = pll_downloader.format_size(
                sum([elem["size"] for elem in data["corpora"]])
            )
            pll_downloader.download(data["corpora"], len(data["corpora"]), c_size)
            downloaded_filenames = [pll_downloader.make_file_name(c) for c in corpora]

            # Extracting Files
            for filename in downloaded_filenames:
                all_files += extract_file(os.path.join(args.data_path, filename))

        # Joining together files
        prefix = min(f_lang, s_lang) + "-" + max(f_lang, s_lang)
        for filepath in all_files:
            if filepath.endswith(prefix + "." + f_lang):
                append_file(
                    filepath,
                    os.path.join(final_data_path, "para", lg_pair + "." + f_lang),
                )
            elif filepath.endswith(prefix + "." + s_lang):
                append_file(
                    filepath,
                    os.path.join(final_data_path, "para", lg_pair + "." + s_lang),
                )
            elif args.delete_metadata:
                os.remove(filepath)

    if args.merge:
        # Join datasets
        joiner(args.data_path, args.delete_old)
