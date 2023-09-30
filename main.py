import argparse

import yaml
from rich.console import Console

from language_model import LLM
from utils import suppress_stdout_stderr, verify_download_model

parser = argparse.ArgumentParser()
parser.add_argument(
    "--config",
    default="./config/config.yaml",
    help="Config file path",
)
console = Console()


def run(args):
    console.clear()
    with open(args.config) as f:
        conf = yaml.safe_load(f)
    verify_download_model(conf["model_path"], conf["model_url"])
    with suppress_stdout_stderr():
        llm = LLM(conf, console)
        llm.chat()


if __name__ == "__main__":
    args = parser.parse_args()
    run(args)
