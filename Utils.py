import math, cv2, os
from scipy.signal import savgol_filter
import numpy as np
import scipy.fftpack

def check_dir():
	if not os.path.isdir("Data"):
	    os.mkdir("Data")

def get_cor(px, py):
	x = (px - 130) * 4 / 470.0
	y = (800 - py) * 4 / 470.0
	return x, y

def get_frame():
	cap = cv2.VideoCapture("sample_vid.MOV")
	for i in range(120):
	    ret, frame = cap.read()
	cv2.imwrite("out.jpg", frame)
	cap.release()

def get_pixels():
	temp = cv2.imread("Imgs/NanKari_1_decrypted/out2.jpg")
	cv2.namedWindow('Raw',cv2.WINDOW_NORMAL)
	cv2.imshow("Raw", temp)
	if cv2.waitKey(2000000) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
	
def read(filename):
    x = []
    y = []

    temp_t = open(filename, 'r').read().split("\n")
    for temp in temp_t:
        try:    
            x_t, y_t = temp.split()
            x.append(float(x_t))
            y.append(float(y_t))
        except:
            print "temp : " + temp 
    
    return x, y


def add_obs(ax):
    xO, yO, rO = [], [], []
    temp_t = open("obs.txt", 'r').read().split("\n")
    for temp in temp_t:
        try:    
            x_t, y_t, r_t = temp.split()
            xO.append(float(x_t))
            yO.append(float(y_t))
            rO.append(float(r_t))

        except:
            print "temp : " + temp

    circle1 = plt.Circle((xO[0], yO[0]), rO[0], color='r')
    circle2 = plt.Circle((xO[1], yO[1]), rO[1], color='r')
    circle3 = plt.Circle((xO[2], yO[2]), rO[2], color='r')
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)

    ax.set_aspect('equal', adjustable='datalim')

    return ax

def fftret():

    x, y = read("Data/40.txt")

    y = np.array(y)
    mean = np.mean(y)
    y -= mean

    yf = scipy.fftpack.fft(y)

    # removing other freq
    for i in range(4, len(yf)-4):
        yf[i] = np.complex(0+0j)

    y_f = scipy.fftpack.ifft(yf)

    return y_f + mean



class person:

    def __init__(self, id, x, y):
	check_dir()
        open("Data/" + str(id) + ".txt", 'w').write(str(x) + " " + str(y) + "\n")
        self.id = id
        self.x = x
        self.y = y
        self.status = True
    
    def get_dist(self, x, y):
        temp_x = self.x - x
        temp_y = self.y - y
        dist = math.sqrt(temp_x ** 2 + temp_y ** 2)
        return True if dist < .2 else False

    def set(self, x, y):
        open("Data/" + str(self.id) + ".txt", 'a').write(str(x) + " " + str(y) + "\n")
        self.x = x
        self.y = y
        self.status = True

    def set_status(self, flag):
        self.status = flag

    def print_details(self):
        print "id: ", self.id, "\tX: ", self.x, "\tY: ", self.y, "\tStatus: ", self.status


class filter:
    
    def __init__(self, data, timestep=.05):
        self.data = data
        self.timestep = timestep
        self.vel = []
        self.acc = []
        self.path = []

    def fit(self, poly=3, points = 51):
        yF = savgol_filter(self.data, 81, 3)
        vu = [(yF[i+1] - yF[i])/ .05 for i in range(0,len(yF)-1)]
        vf = savgol_filter(vu, points, poly)
        au = [(vf[i+1] - vf[i])/ .05 for i in range(0,len(vf)-1)]
        af = savgol_filter(au, points, poly)
        aF = [i for i in af]
        V = [vf[0]]
        for i in range(len(af)):
            temp = V[-1] + af[i] * .05
            V.append(temp)

        Y = [yF[0]]
        for i in range(len(V)):
            temp = Y[-1] + V[i] * .05
            Y.append(temp)

        aF = [aF[0]] + aF + [aF[-1]]

        V += [V[-1]]

        print len(aF)

        self.vel = V
        self.acc = aF
        self.path = Y

        print len(self.acc)

        return self.path, self.vel, self.acc

get_pixels()
