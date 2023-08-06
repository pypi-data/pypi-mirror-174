import os

import requests
import tqdm


def download_once(url: str, file: str) -> None:
    res: requests.Response = requests.get(url=url, stream=True)
    total: str = res.headers.get("content-length", default=0)
    total = int(total)
    os.makedirs(name=os.path.dirname(p=file), exist_ok=True)
    with open(file=file, mode="wb") as fp, tqdm.tqdm(
        desc=file,
        total=total,
        leave=None,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in res.iter_content(chunk_size=8192):
            bytes_written: int = fp.write(chunk)
            bar.update(n=bytes_written)


def download(url: str, file: str, max_retries: int = 4) -> None:
    for _ in range(max_retries):
        try:
            download_once(url=url, file=file)
        except:
            pass
        else:
            break
