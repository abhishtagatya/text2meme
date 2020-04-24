import json
import requests
import hashlib
from hashlib import sha256

from bs4 import BeautifulSoup

page_limit = 200
imgflip_dataset = []

with open('memes_reference.json') as memes_reference:
    json_meme = json.load(memes_reference)

for i, memes in enumerate(json_meme['data']['memes']):

    memes_data = {
        "id" : i,
        "name" : memes['name'],
        "base_img" : memes['url'],
        "width" : memes['width'],
        "height": memes['height'],
        "text_box" : memes["box_count"],
        "generated_memes" : []
    }

    count = 0
    
    for j in range(page_limit): # page_limit x 14 = ?

        imgflip_meme = "https://imgflip.com/meme/{}".format(memes['name'].replace(' ', '-'))

        req = requests.get(imgflip_meme, {'page': j})
        page = req.text

        soup = BeautifulSoup(page, 'html.parser')
        img_found = soup.find_all('img', class_='base-img')

        for img in img_found:
            generated_memes = { "id" : count+1 }
            generated_memes['alt_text'] = img['alt']

            # Meme might contain images and less captions
            if 'image tagged in memes,' in img['alt']:
                continue

            generated_memes['caption_text'] = (img['alt'].split('|'))[1]
            generated_memes['image_url'] = img['src']

            combination = generated_memes['alt_text'] + generated_memes['caption_text'] + generated_memes['image_url']
            generated_memes['hash_id'] = str(sha256(combination.encode('utf-8')).hexdigest())

            memes_data['generated_memes'].append(generated_memes)
            count += 1    
        
    imgflip_dataset.append(memes_data)
    print('{} appended to dataset'.format(memes['name']))

with open('imgflip_dataset.json', 'w') as outfile:
    json.dump(imgflip_dataset, outfile)




