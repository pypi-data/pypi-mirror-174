import os
import urllib.parse

import tqdm.contrib.concurrent

from . import settings
from utility_collection.common.download import download


def prepare_files(data: dict | list | str) -> list[str]:
    if isinstance(data, dict):
        res: list[str] = []
        for key, value in data.items():
            files: list[str] = prepare_files(data=value)
            res += [os.path.join(key, file) for file in files]
        return res
    elif isinstance(data, list):
        res: list[str] = sum([prepare_files(data=x) for x in data], start=[])
        return res
    elif isinstance(data, str):
        return [data]
    else:
        return data


def main():
    files: list[str] = prepare_files(data=settings.SAMPLES)
    urls: list[str] = [
        urllib.parse.urljoin(base="https://filesamples.com/samples/", url=file)
        for file in files
    ]
    tqdm.contrib.concurrent.thread_map(download, urls, files)


if __name__ == "__main__":
    main()
