import argparse

from pydeepspeech.install_models import URL_PBMM, URL_SCORER, install_deepspeechmodules


def main():
    args = argparse.ArgumentParser(
        description="Installs pbmm and scorer files for pydeepspeech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    args.add_argument("--pbmm", required=True, help="Path to the pbmm file")
    args.add_argument("--scorer", required=True, help="Path to the scorer file")
    args = args.parse_args()
    url_pbmm = args.pbmm or input(
        f"Path or URL to the pbmm file [{URL_PBMM}]: "
    )
    url_scorer = args.pbmm or input(
        f"Path or URL to the scorer file [{URL_SCORER}]: "
    )
    if url_pbmm.strip() == "":
        url_pbmm = URL_PBMM
    if url_scorer.strip() == "":
        url_scorer = URL_SCORER
    install_deepspeechmodules(url_pbmm=url_pbmm, url_scorer=url_scorer)


if __name__ == "__main__":
    main()
