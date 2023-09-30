import os
import sys

import requests


def download_file(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"File downloaded successfully to {save_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def verify_download_model(model_path, model_url):
    if not os.path.exists(model_path):
        print('Downloading model...')
        download_file(model_url, model_path)
        print(f"New model file downloaded to {model_path}")


class suppress_stdout_stderr(object):
    def __enter__(self):
        # self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, "w")

        # self.old_stdout_fileno_undup    = sys.stdout.fileno()
        self.old_stderr_fileno_undup = sys.stderr.fileno()

        # self.old_stdout_fileno = os.dup ( sys.stdout.fileno() )
        self.old_stderr_fileno = os.dup(sys.stderr.fileno())

        # self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        # os.dup2 ( self.outnull_file.fileno(), self.old_stdout_fileno_undup )
        os.dup2(self.errnull_file.fileno(), self.old_stderr_fileno_undup)

        # sys.stdout = self.outnull_file
        sys.stderr = self.errnull_file
        return self

    def __exit__(self, *_):
        # sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        # os.dup2 ( self.old_stdout_fileno, self.old_stdout_fileno_undup )
        os.dup2(self.old_stderr_fileno, self.old_stderr_fileno_undup)

        # os.close ( self.old_stdout_fileno )
        os.close(self.old_stderr_fileno)

        # self.outnull_file.close()
        self.errnull_file.close()
