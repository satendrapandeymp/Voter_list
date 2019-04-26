from glob import glob
import cv2, os

def get_name(name):
    return name.split("/")[-2]

def check(name):
    if not os.path.exists("Details/" + name):
        os.mkdir("Details/" + name)
    
    if not os.path.exists("IDs/" + name):
        os.mkdir("IDs/" + name)



class splitter:
    
    def __init__(self, file_name, folder_name):
        self.file_name = file_name
        self.id_folder = "IDs/" + folder_name + "/"
        self.details_folder = "Details/" + folder_name + "/"
        self.active = True
        self.x_start = 60
        self.y_start = 115
        self.width_detail = 500
        self.width_id = 240
        self.hight_detail = 195
        self.hight_id = 40
        self.id_name = ""
        self.detail_name = ""
        self.detail = None
        self.id = None

    def customize(self):
        if 'out0.' in self.file_name or 'out1.' in self.file_name:
            self.active = False
        
        if 'out2.' in self.file_name:
            self.y_start = 132

    def get_page(self):
        self.page = int(self.file_name.split("out")[1].split(".")[0])

    def read_file(self):
        self.frame = cv2.imread(self.file_name)

    def get_filename(self, i, j):
        temp = self.page * 30 + i * 3 + j
        self.id_name = self.id_folder + str(temp) + ".jpg"
        self.detail_name = self.details_folder + str(temp) + ".jpg"

    def get_splitted_files(self):
        for i in range(10):
            for j in range(3):
                self.get_filename(i, j)
                detail_y_start, detail_x_start = self.y_start + i * self.hight_detail,  self.x_start + j * self.width_detail
                detail_y_end, detail_x_end = detail_y_start + self.hight_detail, detail_x_start + self.width_detail
                id_y_end, id_x_start = detail_y_start + 40, detail_x_end - 240 
                self.detail = self.frame[ detail_y_start: detail_y_end, detail_x_start: detail_x_end]
                self.id = self.frame[detail_y_start: id_y_end, id_x_start: detail_x_end]
                self.write_files()

    def write_files(self):
        cv2.imwrite(self.id_name, self.id)
        cv2.imwrite(self.detail_name, self.detail)

    def excute(self):
        self.customize()
        if self.active:
            self.get_page()
            self.read_file()
            self.get_splitted_files()


folders = glob("Imgs/*/")

for folder in folders:

    check(get_name(folder))
    files =  glob(folder + "*")
    for file in files:
        s = splitter(file, get_name(folder))
        s.excute()

    
