import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
import random
from pygame import mixer
from mutagen.mp3 import MP3
import time
import style

musicList = []
mixer.init()
muted = False
currentVolume = 0
soundLength = 0
count = 0
index = 0
paused = False
pauseValue = 0
pauseProgressBar = False

class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Music Player')
        self.setGeometry(520, 150, 360, 550)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ########ProgressBar####################
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet(style.progressBarStyle())
        #self.progressBar.setToolTip('ProgressBar')
        ##########LABEL########################
        self.songTimmerLabel = QLabel('00:00')
        self.songLengthLabel = QLabel('00:00')
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

        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(QIcon('icons/pause.png'))
        self.pauseButton.setIconSize(QSize(24, 24))
        self.pauseButton.setToolTip('Pause')
        self.pauseButton.clicked.connect(self.pauseSounds)

        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon('icons/play.png'))
        self.playButton.setIconSize(QSize(24, 24))
        self.playButton.setToolTip('Play')
        self.playButton.clicked.connect(self.playSounds)

        self.nextButton = QToolButton()
        self.nextButton.setIcon(QIcon('icons/next.png'))
        self.nextButton.setIconSize(QSize(24, 24))
        self.nextButton.setToolTip('Play Next')
        self.nextButton.clicked.connect(self.nextSounds)

        self.muteButton = QToolButton()
        self.muteButton.setIcon(QIcon('icons/mute.png'))
        self.muteButton.setIconSize(QSize(24, 24))
        self.muteButton.setToolTip('Mute')
        self.muteButton.clicked.connect(self.muteVolume)

        ##########Volume Slider##############################
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setStyleSheet(style.sliderStyle())
        self.volumeSlider.setToolTip('Volume')
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setVolume)

        ###########Play List################################
        self.playList = QListWidget()
        self.playList.setStyleSheet(style.listBoxStyle())
        self.playList.doubleClicked.connect(self.playSounds)
        ##############TIMER##################################
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.progressBarUpdate)



    def layouts(self):
        ############Creating Layouts#########################
        self.mainLayout = QVBoxLayout()
        self.topMainLayaout = QVBoxLayout()
        self.topGroupLayaout = QGroupBox('Music Player') # Widget
        self.topGroupLayaout.setStyleSheet(style.groupBoxStyle())
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()
        ############Adding Widgets############################
        ###########Top Layout Widgets#########################
        self.topLayout.addWidget(self.progressBar)
        self.topLayout.addWidget(self.songTimmerLabel)
        self.topLayout.addWidget(self.songLengthLabel)
        ###########MiddleLayout Widget########################
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addButton)
        self.middleLayout.addWidget(self.shuffleButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.pauseButton)
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
        global soundLength
        global count
        global index
        count = 0
        index = self.playList.currentRow()
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            soundLength = sound.info.length
            soundLength = round(soundLength)
            self.progressBar.setMaximum(soundLength)
            self.progressBar.setValue(count)
            equivalent = round(soundLength/60, 2)
            self.songLengthLabel.setText(str(equivalent).replace('.', ':').ljust(4, '0').rjust(5, '0'))
            self.topGroupLayaout.setTitle(os.path.basename(str(musicList[index])))
        except:
            QMessageBox.information(self,'Warning', 'Somethimg wrong here!')

    def pauseSounds(self):
        global paused
        global pauseValue
        try:
            if paused == False:
                mixer.music.pause()
                paused = True
                pauseValue = self.progressBar.value()
                print('ProgerssBar:', pauseValue)
                self.timer.stop()
            else:
                mixer.music.unpause()
                paused = False
                pauseProgressBar = True
                self.timer.start()
        except:
            QMessageBox.information(self, 'Warning', 'Somethimg wrong here!')

    def progressBarUpdate(self):
        global count
        global soundLength
        global pauseProgressBar
        global pauseValue
        count += 1
        if pauseProgressBar == False:
            self.progressBar.setValue(count)
            self.songTimmerLabel.setText(time.strftime('%M:%S', time.gmtime(count)))
            if count == soundLength:
                self.timer.stop()

        if count == pauseValue:
            count = pauseValue
            self.progressBar.setValue(count)
            self.songTimmerLabel.setText(time.strftime('%M:%S', time.gmtime(count)))
        self.progressBar.setToolTip(time.strftime('%M:%S', time.gmtime(count)))




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
            self.muteButton.setIcon(QIcon('icons/mute.png'))
            self.muteButton.setIconSize(QSize(24, 24))
            self.muteButton.setToolTip('Mute')

        else:
            mixer.music.set_volume(currentVolume/100)
            self.volumeSlider.setValue(currentVolume)
            muted = False
            self.muteButton.setIcon(QIcon('icons/volume.png'))
            self.muteButton.setIconSize(QSize(24, 24))
            self.muteButton.setToolTip('Unmute')

    def previousSound(self):
        global soundLength
        global count
        global index
        count = 0
        items = self.playList.count()
        if index == 0:
            index = items
        index -= 1
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            soundLength = sound.info.length
            soundLength = round(soundLength)
            self.progressBar.setMaximum(soundLength)
            self.progressBar.setValue(count)
            equivalent = round(soundLength / 60, 2)
            self.songLengthLabel.setText(str(equivalent).replace('.', ':').ljust(4, '0').rjust(5, '0'))
            self.topGroupLayaout.setTitle(os.path.basename(str(musicList[index])))
        except:
            QMessageBox.information(self, 'Warning', 'Somethimg wrong here!')

    def nextSounds(self):
        global soundLength
        global count
        global index
        count = 0
        items = self.playList.count()
        index += 1
        if index == items :
            index = 0
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))
            soundLength = sound.info.length
            soundLength = round(soundLength)
            self.progressBar.setMaximum(soundLength)
            self.progressBar.setValue(count)
            equivalent = round(soundLength / 60, 2)
            self.songLengthLabel.setText(str(equivalent).replace('.', ':').ljust(4, '0').rjust(5, '0'))
            self.topGroupLayaout.setTitle(os.path.basename(str(musicList[index])))
        except:
            QMessageBox.information(self, 'Warning', 'Somethimg wrong here!')

def main():
    APP = QApplication(sys.argv)
    window = Player()
    sys.exit(APP.exec_())

if __name__ == '__main__':
    main()
