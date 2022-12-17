from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel, QWidget, QFileDialog
    )
import sys
import os


app = QApplication(sys.argv)
window = QWidget()
window.resize(900,600)
window.setWindowTitle('easy_edit')

btn_open_dir = QPushButton("открыть папку")
btn_rotate_left = QPushButton("лево")
btn_rotate_right = QPushButton("право")
btn_contrast = QPushButton("контраст")
btn_mirror = QPushButton("отзеркалить")
btn_black_white = QPushButton("ч/б")
image = QLabel("картинка наверное")
image_list = QListWidget()

h_main = QHBoxLayout()
v_left = QVBoxLayout()
v_right = QVBoxLayout()
h_add = QHBoxLayout()

h_add.addWidget(btn_rotate_left)
h_add.addWidget(btn_rotate_right)
h_add.addWidget(btn_mirror)
h_add.addWidget(btn_contrast)
h_add.addWidget(btn_black_white)

v_left.addWidget(btn_open_dir)
v_left.addWidget(image_list)

v_right.addWidget(image)
v_right.addLayout(h_add)

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

def show_image():
    print(image_list.currentItem)

btn_open_dir.clicked.connect(show_files)
image_list.itemChanged(show_image)

app.exec_()
