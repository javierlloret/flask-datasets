
from flask import Flask, render_template
from flask import jsonify
from random import *
from pycocotools.coco import COCO
import json
from itertools import islice
import os

app = Flask(__name__)
app.config["DEBUG"] = True

#It loads data from the COCO Localized Narratives dataset
def load_data():
    rand_number = randint(1,2400)
    print(rand_number)

    json_file_str =""
    with  app.open_resource('2400_coco_val_localized_narratives_1.jsonl') as lines:
        for line in islice(lines, rand_number-1, rand_number):
            #print(line)
            json_file_str=line

    # parse file
    obj = json.loads(json_file_str)
    image_id = obj["image_id"]

    print(f"image_id={image_id}")

    annFile=os.getcwd()+'/annview/static/coco_2017_annotations/instances_val2017.json'

    # initialize COCO api for instance annotations
    coco=COCO(annFile)
    image=coco.loadImgs(int(image_id))
    print(image[0]['flickr_url'])
    print(image[0]['coco_url'])
    img_url=image[0]['coco_url']
    return img_url,json_file_str, obj

@app.route('/getpythondata',methods=['POST'])
def get_python_data():
    img_url, _, obj = load_data()
    obj.update({'coco_url': img_url})
    return obj


@app.route('/')
def index():
    img_url, annotation_file, _=load_data()

    return render_template("main_page_ajax.html", img_url=img_url,annotation_file=annotation_file)
