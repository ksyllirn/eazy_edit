from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel, QWidget, QFileDialog
    )
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
from PIL import Image, ImageEnhance, ImageFilter


app = QApplication(sys.argv)
window = QWidget()
window.resize(900,600)
window.setWindowTitle('easy_edit')

btn_open_dir = QPushButton("открыть папку")
btn_rotate_left = QPushButton("лево")
btn_rotate_right = QPushButton("право")
lbl_contrast = QLabel("Контраст")
btn_add_contrast = QPushButton("+")
btn_remove_contrast = QPushButton("-")
btn_mirror = QPushButton("отзеркалить")
btn_black_white = QPushButton("ч/б")
image = QLabel("картинка наверное")
image_list = QListWidget()
btn_sharpen = QPushButton("резкость")
btn_smooth = QPushButton("гладкость")
btn_make_square = QPushButton("сделать квадрат")

h_main = QHBoxLayout()
v_left = QVBoxLayout()
v_right = QVBoxLayout()
h_add = QHBoxLayout()
h_add_2 = QHBoxLayout()
h_add_3 = QHBoxLayout()

h_add.addWidget(btn_rotate_left)
h_add.addWidget(btn_rotate_right)
h_add.addWidget(btn_mirror)
h_add.addWidget(btn_black_white)

h_add_2.addWidget(lbl_contrast)
h_add_2.addWidget(btn_add_contrast)
h_add_2.addWidget(btn_remove_contrast)


h_add_3.addWidget(btn_sharpen)
h_add_3.addWidget(btn_smooth)
h_add_3.addWidget(btn_make_square)

v_left.addWidget(btn_open_dir)
v_left.addWidget(image_list)

v_right.addWidget(image)
v_right.addLayout(h_add)
v_right.addLayout(h_add_2)
v_right.addLayout(h_add_3)

h_main.addLayout(v_left, stretch=2)
h_main.addLayout(v_right, stretch=6)

window.setLayout(h_main)
window.show()

workdir = ''

def choose_dir():
    current_dir = QFileDialog.getExistingDirectory(window)
    return (len(current_dir) != 0, current_dir)


def show_files():
    result = choose_dir()
    if result[0]:
        global workdir
        workdir = result[1]
        files = os.listdir(workdir)
        images = filter(files, ['.jpg', '.png', '.jpeg', '.bpm'])
        image_list.clear()
        image_list.addItems(images)

def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
                break
    return result

class ImageProccesor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified'
    
    def load_image(self, dir, filename):
        self.dir = dir
        self.filename = filename
        path = os.path.join(dir,filename)
        self.image = Image.open(path)

    def show_image(self, path):
        image.hide()
        pixmap = QPixmap(path)
        w, h = image.width(), image.height()
        pixmap = pixmap.scaled(w,h,Qt.KeepAspectRatio)
        image.setPixmap(pixmap)
        image.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.Transpose.ROTATE_90)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_right(self):
        self.image = self.image.transpose(Image.Transpose.ROTATE_270)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT )
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_enhance(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def save_image(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        path = os.path.join(path, self.filename)
        self.image.save(path)

    def less_enhance(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(0.5)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_smooth(self):
        self.image = self.image.filter(ImageFilter.SMOOTH)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_square(self):
        box = ()
        w, h = self.image.width, self.image.height
        
        if w < h:
            offset = (h-w)//2
            box = (0,0+offset,w,w+offset)
        else:
            offset = (w-h)//2
            box = (0+offset,0,h+offset,h)
        self.image = self.image.crop(box)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)


def showCurrentImage():
    if image_list.currentRow() >= 0:
        filename = image_list.currentItem().text()
        img_proc.load_image(workdir, filename)
        path = os.path.join(workdir, filename)
        img_proc.show_image(path)


img_proc = ImageProccesor()

btn_open_dir.clicked.connect(show_files)
image_list.currentRowChanged.connect(showCurrentImage)
btn_black_white.clicked.connect(img_proc.do_bw)
btn_rotate_left.clicked.connect(img_proc.do_left)
btn_rotate_right.clicked.connect(img_proc.do_right)
btn_mirror.clicked.connect(img_proc.do_mirror)
btn_add_contrast.clicked.connect(img_proc.do_enhance)
btn_remove_contrast.clicked.connect(img_proc.less_enhance)
btn_sharpen.clicked.connect(img_proc.do_sharpen)
btn_smooth.clicked.connect(img_proc.do_smooth)
btn_make_square.clicked.connect(img_proc.do_square)

app.exec_()
