import numpy as np
import pandas as pd

import requests

df = pd.read_csv('memes_reference_data.tsv', sep='\t')

for i, row in df.iterrows():
    url = row.BaseImageURL
    r = requests.get(url)

    with open('./image_collection/base_img/' + row.MemeLabel + '.jpg', 'wb') as outfile:
        outfile.write(r.content)

# url = 'http://papers.xtremepapers.com/CIE/Cambridge%20IGCSE/Mathematics%20(0580)/0580_s03_qp_1.pdf'
# r = requests.get(url)
# with open('0580_s03_qp_1.pdf', 'wb') as outfile:
#     outfile.write(r.content)