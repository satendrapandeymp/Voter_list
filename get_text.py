from glob import glob
import cv2, os, sys


reload(sys)
sys.setdefaultencoding('utf-8')

cmd = "tesseract {0} tempo"

def get_name(name):
    return "Res/" + name.split("/")[-2] + ".csv"


class person:

    def __init__(self, file_name, file_to_write):
        self.file_name = file_name
        self.file_to_write = file_to_write
        self.id = self.get_id()
        self.run()
        self.write()

    def run(self):
        os.system(cmd.format(self.file_name))

    def write(self):
        temp_str = open('tempo.txt', 'r').read().strip()
        if len(temp_str) > 5:
            open(self.file_to_write, 'a').write(self.id + "\t" + temp_str + "\n")

    def get_id(self):
        return self.file_name.split("/")[-1].split(".")[0]


folders = glob("IDs/*/")

for folder in folders:

    open(get_name(folder) , 'w').write("")
    files =  glob(folder + "*")
    for file in files:
        s = person(file, get_name(folder))

