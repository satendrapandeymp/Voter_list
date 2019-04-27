#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify
from glob import glob

app = Flask(__name__ , static_url_path='/static', static_folder = "static")

database = {}

class person:
    def __init__(self, file, id):
        self.file = file
        self.id = id
        self.booth = self.get_booth()
        self.detail = "static/Details/{0}/{1}.jpg".format(self.booth, self.id)

    def get_booth(self):
        return self.file.split("/")[-1].split(".")[0]

def load(files):
    for file in files:
        raw_data = open(file).read().strip().split("\n")
        for data in raw_data:
            data = data.split("\t")
            p = person(file, data[0])
            database.update({data[1]: p})

files = glob("Res/*.csv")
load(files)

@app.route("/")
def index():
    name = "/static/300.jpg"
    center = "Pooling Booth: Campus_3_decrypted"
    temp_id = "UP/64/292/0120094"
    id = request.args.get('id')
    try:
        p = database[id]
        name = p.detail
        center = "Polling booth: " + p.booth
        temp_id = id
    except:
        pass
    
    return render_template('index.html', name = name, center = center, temp_id= temp_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
