"""Downloading data from the M4 competition
"""

import os
import requests


def download(datapath, url, name, split=None):
    
    os.makedirs(datapath, exist_ok=True)
    namesplit = f"{split}/{name}" if split is not None else name
    url = url.format(namesplit)
    file_path = f"{os.path.join(datapath, name)}.csv"

    if os.path.exists(file_path):
        print(f"{name} already exists")
        return

    print(f'Downloading {url}')

    r = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=16 * 1024 ** 2):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

    return


if __name__ == "__main__":
    data_frequencies = ['Yearly', 'Quarterly', 'Monthly', 'Weekly', 'Daily', 'Hourly']
    datapath = "./dataset/"
    url = "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/{}.csv"

    download(datapath, url, 'M4-info')
    for freq in data_frequencies:
        for split in ['train', 'test']:
            download(datapath+split, url, f'{freq}-{split}', split.capitalize())
