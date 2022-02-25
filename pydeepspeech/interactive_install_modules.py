import argparse

from pydeepspeech.install_models import install_deepspeechmodules


def main():
    args = argparse.ArgumentParser(
        description="Installs pbmm and scorer files for pydeepspeech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    args.add_argument("--pbmm", required=True, help="Path to the pbmm file")
    args.add_argument("--scorer", required=True, help="Path to the scorer file")
    args = args.parse_args()
    url_pbmm = args.pbmm or input("Path or URL to the pbmm file: ")
    url_scorer = args.pbmm or input("Path or URL to the scorer file: ")
    install_deepspeechmodules(url_pbmm=url_pbmm, url_scorer=url_scorer)


if __name__ == "__main__":
    main()
