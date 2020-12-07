import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
import random
from pygame import mixer

musicList = []
mixer.init()
#index = 0
muted = False
currentVolume = 0

class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Music Player')
        self.setGeometry(520, 150, 320, 550)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ########ProgressBar####################
        self.progressBar = QProgressBar()
        ###########Buttons#####################
        self.addButton = QToolButton()
        self.addButton.setIcon(QIcon('icons/add.png'))
        self.addButton.setIconSize(QSize(24,24))
        self.addButton.setToolTip('Add a song')
        self.addButton.clicked.connect(self.addSound)

        self.shuffleButton = QToolButton()
        self.shuffleButton.setIcon(QIcon('icons/shuffle.png'))
        self.shuffleButton.setIconSize(QSize(24,24))
        self.shuffleButton.setToolTip('Shuffle The list')
        self.shuffleButton.clicked.connect(self.shufflePlayList)

        self.previousButton = QToolButton()
        self.previousButton.setIcon(QIcon('icons/previous.png'))
        self.previousButton.setIconSize(QSize(24, 24))
        self.previousButton.setToolTip('Play Previous')
        self.previousButton.clicked.connect(self.previousSound)

        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon('icons/play.png'))
        self.playButton.setIconSize(QSize(24, 24))
        self.playButton.setToolTip('Play')
        self.playButton.clicked.connect(self.playSounds)

        self.nextButton = QToolButton()
        self.nextButton.setIcon(QIcon('icons/next.png'))
        self.nextButton.setIconSize(QSize(24, 24))
        self.nextButton.setToolTip('Play Next')

        self.muteButton = QToolButton()
        self.muteButton.setIcon(QIcon('icons/mute.png'))
        self.muteButton.setIconSize(QSize(24, 24))
        self.muteButton.setToolTip('Mute')
        self.muteButton.clicked.connect(self.muteVolume)

        ##########Volume Slider##############################
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setToolTip('Volume')
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setVolume)

        ###########Play List################################
        self.playList = QListWidget()
        self.playList.setStyleSheet('background-color:#2C3E50;font:Times 14; color:white;')
        self.playList.doubleClicked.connect(self.playSounds)

    def layouts(self):
        ############Creating Layouts#########################
        self.mainLayout = QVBoxLayout()
        self.topMainLayaout = QVBoxLayout()
        self.topGroupLayaout = QGroupBox('Music Player') # Widget
        self.topGroupLayaout.setStyleSheet('background-color:#D0ECE7;')
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()
        ############Adding Widgets############################
        ###########Top Layout Widgets#########################
        self.topLayout.addWidget(self.progressBar)
        ###########MiddleLayout Widget########################
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addButton)
        self.middleLayout.addWidget(self.shuffleButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.previousButton)
        self.middleLayout.addWidget(self.nextButton)
        self.middleLayout.addWidget(self.volumeSlider)
        self.middleLayout.addWidget(self.muteButton)
        self.middleLayout.addStretch()
        #############BottomLayout Widget######################
        self.bottomLayout.addWidget(self.playList)

        self.topMainLayaout.addLayout(self.topLayout)
        self.topMainLayaout.addLayout(self.middleLayout)
        self.topGroupLayaout.setLayout(self.topMainLayaout)
        self.mainLayout.addWidget(self.topGroupLayaout) # Widget
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

    def addSound(self):
        directory = QFileDialog.getOpenFileName(self,'Add Sound','','Sound Files (*.mp3 *.ogg *.wav)')
        fileName = os.path.basename(directory[0])
        self.playList.addItem(fileName)
        musicList.append(directory[0])

    def shufflePlayList(self):
        random.shuffle(musicList)
        self.playList.clear()
        for song in musicList:
            fileName = os.path.basename(song)
            self.playList.addItem(fileName)

    def playSounds(self):
        #global index
        index = self.playList.currentRow()
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            #index += 1
            #mixer.music.queue(str(musicList[index]))
        except:
            pass
        #print(index)
        #fileName = os.path.basename(musicList[index])
        #print(fileName, type(fileName))


    def setVolume(self):
        self.volume = self.volumeSlider.value()
        mixer.music.set_volume(self.volume/100)

    def muteVolume(self):
        global muted
        global currentVolume
        if muted == False:
            currentVolume = self.volumeSlider.value()
            mixer.music.set_volume(0.0)
            muted = True
            self.volumeSlider.setValue(0)
            print(currentVolume)

        else:
            mixer.music.set_volume(currentVolume/100)
            self.volumeSlider.setValue(currentVolume)
            muted = False

    def previousSound(self):
        index = self.playList.currentRow()
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            index -= 2
            mixer.music.queue(str(musicList[index]))
        except:
            pass
        
def main():
    APP = QApplication(sys.argv)
    window = Player()
    sys.exit(APP.exec_())

if __name__ == '__main__':
    main()
