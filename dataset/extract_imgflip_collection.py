import numpy as np
import pandas as pd

import requests

df = pd.read_csv('memes_data.tsv', sep='\t')

for i, row in df.iterrows():
    url = 'https:' + row.ImageURL
    r = requests.get(url)

    with open('./image_collection/imgflip_collection/' + row.MemeLabel + '_' + str(i) +'.jpg', 'wb') as outfile:
        outfile.write(r.content)
