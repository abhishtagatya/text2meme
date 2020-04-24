import json

import numpy as np
import pandas as pd

with open('imgflip_dataset.json') as meme_ref:
    meme_ref = json.load(meme_ref)

meme_list = np.unique(df.MemeLabel)
meme_ref_list = []

count = 0
for meme in meme_ref:
    if meme['name'] not in meme_list:
        print(meme['name'])
        continue
    meme_ref_list.append([
        meme['name'],
        meme['base_img'],
        meme['height'],
        meme['width'],
        meme['text_box']
    ])
    count += 1

df_col = ['MemeLabel', 'BaseImageURL', 'Height', 'Width', 'StandardTextBox']

df = pd.DataFrame(meme_ref_list, columns=df_col)
df.to_csv('memes_reference_data.tsv', sep='\t', index=False)

memes_list = []

for meme in json_meme:
    for img in meme['generated_memes']:
        memes_list.append([
            img['alt_text'],
            img['caption_text'],
            img['image_url'],
            img['hash_id'],
            meme['name']
        ])

df2_col = ['AltText', 'CaptionText', 'ImageURL', 'HashId', 'MemeLabel']

df2 = pd.DataFrame(memes_list, columns=df2_col)
df2.to_csv('memes_data.tsv', sep='\t', index=False)

