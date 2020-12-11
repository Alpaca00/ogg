import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
import random
from pygame import mixer
from mutagen.mp3 import MP3
import time
from datetime import datetime
import style
from threading import Timer

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
forward = False
themes = True

class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Music Player')
        self.setGeometry(520, 150, 360, 550)
        self.setStyleSheet('background-color:#D0ECE7;')
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()


    def widgets(self):
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet(style.progressBarStyle())

        self.songTimmerLabel = QLabel('00:00')
        self.songLengthLabel = QLabel('00:00')

        self.stopButton = QToolButton()
        self.stopButton.setIcon(QIcon('icons/stop.png'))
        self.stopButton.setIconSize(QSize(24, 24))
        self.stopButton.setToolTip('Stop a song')
        self.stopButton.clicked.connect(self.stopSounds)

        self.previousButton = QToolButton()
        self.previousButton.setIcon(QIcon('icons/previous.png'))
        self.previousButton.setIconSize(QSize(24, 24))
        self.previousButton.setToolTip('Play Previous')
        self.previousButton.clicked.connect(self.previousSound)

        self.pauseButton = QToolButton()
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

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setStyleSheet(style.sliderStyle())
        self.volumeSlider.setToolTip('Volume')
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setVolume)

        self.forwardButton = QToolButton()
        self.forwardButton.setIcon(QIcon('icons/forward.png'))
        self.forwardButton.setIconSize(QSize(24, 24))
        self.forwardButton.setToolTip('Forward a song ')
        self.forwardButton.clicked.connect(self.forwardSong)

        self.playList = QListWidget()
        self.playList.setStyleSheet(style.listBoxStyle())
        self.playList.doubleClicked.connect(self.playSounds)

        self.addButton = QToolButton()
        self.addButton.setIcon(QIcon('icons/add.png'))
        self.addButton.setIconSize(QSize(24, 24))
        self.addButton.setToolTip('Add a song')
        self.addButton.clicked.connect(self.addSound)

        self.deleteSongListButton = QToolButton()
        self.deleteSongListButton.setIcon(QIcon('icons/delete.png'))
        self.deleteSongListButton.setIconSize(QSize(24, 24))
        self.deleteSongListButton.setToolTip('Delete a song')
        self.deleteSongListButton.clicked.connect(self.deleteSongs)

        self.shuffleButton = QToolButton()
        self.shuffleButton.setIcon(QIcon('icons/shuffle.png'))
        self.shuffleButton.setIconSize(QSize(24, 24))
        self.shuffleButton.setToolTip('Shuffle The list')
        self.shuffleButton.clicked.connect(self.shufflePlayList)

        self.clearListButton = QToolButton()
        self.clearListButton.setIcon(QIcon('icons/clear.png'))
        self.clearListButton.setIconSize(QSize(24, 24))
        self.clearListButton.setToolTip('Clear The list')
        self.clearListButton.clicked.connect(self.clearPlayList)

        self.timmerExitButton = QToolButton()
        self.timmerExitButton.setIcon(QIcon('icons/exitTimmer.png'))
        self.timmerExitButton.setIconSize(QSize(24, 24))
        self.timmerExitButton.setToolTip('Сonfirm The Output Timer')
        self.timmerExitButton.clicked.connect(self.exitTimmer)

        self.exitButton = QToolButton()
        self.exitButton.setIcon(QIcon('icons/exitTool.png'))
        self.exitButton.setIconSize(QSize(24, 24))
        self.exitButton.setToolTip('Exit')
        self.exitButton.clicked.connect(self.exit)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.progressBarUpdate)

        self.combo = QComboBox()
        self.combo.addItems(['15', '30', '45', '60', '120'])

        self.countDownLabel = QLabel('00:00')
        self.countDownLabel.setMaximumSize(QSize(28, 28))

        self.themeButton = QToolButton()
        self.themeButton.setIcon(QIcon('icons/theme.png'))
        self.themeButton.setIconSize(QSize(24, 24))
        self.themeButton.setToolTip('Themes')
        self.themeButton.clicked.connect(self.themesChange)

        ###############QTimer for label#######################
        self.timerLabelTime = QTimer()
        self.timerLabelTime.setInterval(1000)
        self.timerLabelTime.timeout.connect(self.updateLabel)

    def layouts(self):
        ############Creating Layouts#########################
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(1)
        self.topMainLayaout = QVBoxLayout()
        self.topGroupLayaout = QGroupBox('Music Player') # Widget
        self.topGroupLayaout.setStyleSheet(style.groupBoxStyle())
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()
        self.bellowLayout = QHBoxLayout()
        ############Adding Widgets############################
        ###########Top Layout Widgets#########################
        self.topLayout.addWidget(self.progressBar)
        self.topLayout.addWidget(self.songTimmerLabel)
        self.topLayout.addWidget(self.songLengthLabel)
        ###########MiddleLayout Widget########################
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.stopButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.forwardButton)
        self.middleLayout.addWidget(self.pauseButton)
        self.middleLayout.addWidget(self.previousButton)
        self.middleLayout.addWidget(self.nextButton)
        self.middleLayout.addWidget(self.volumeSlider)
        self.middleLayout.addWidget(self.muteButton)
        self.middleLayout.addStretch()
        #############BottomLayout Widget######################
        self.bottomLayout.addWidget(self.playList)
        #############BellowLayout Widgets######################
        self.bellowLayout.addWidget(self.addButton)
        self.bellowLayout.addWidget((self.deleteSongListButton))
        self.bellowLayout.addWidget(self.shuffleButton)
        self.bellowLayout.addWidget(self.clearListButton)
        self.bellowLayout.addStretch()
        self.bellowLayout.addStretch()
        self.bellowLayout.addWidget(self.themeButton)
        self.bellowLayout.addWidget(self.combo)
        self.bellowLayout.addWidget(self.countDownLabel)
        self.bellowLayout.addWidget(self.timmerExitButton)
        self.bellowLayout.addWidget(self.exitButton)
        self.bottomLayout.setSpacing(1)


        self.topMainLayaout.addLayout(self.topLayout)
        self.topMainLayaout.addLayout(self.middleLayout)
        self.topGroupLayaout.setLayout(self.topMainLayaout)
        self.mainLayout.addWidget(self.topGroupLayaout) # Widget

        self.mainLayout.addLayout(self.bottomLayout)
        self.mainLayout.addLayout(self.bellowLayout)

        self.setLayout(self.mainLayout)

    def addSound(self):
        directory = QFileDialog.getOpenFileName(self,'Add Sound','','Sound Files (*.mp3 *.ogg *.wav)')
        fileName = os.path.basename(directory[0])
        self.playList.addItem(fileName)
        musicList.append(directory[0])

    def deleteSongs(self):
        global musicList
        try:
            song = self.playList.currentRow()
            self.playList.takeItem(song)
            musicList.remove(musicList[song])
        except:
            QMessageBox.warning(self, 'Warning', 'Not working correctly in file playback')


    def clearPlayList(self):
        global musicList
        self.playList.clear()
        musicList.clear()


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
            sound = MP3(str(musicList[index]))
            soundLength = sound.info.length
            soundLength = round(soundLength)
            self.progressBar.setMaximum(soundLength)
            self.progressBar.setValue(count)
            equivalent = round(soundLength/60, 2)
            mixer.music.play()
            self.timer.start()
            self.songLengthLabel.setText(str(equivalent).replace('.', ':').ljust(4, '0').rjust(5, '0'))
            self.topGroupLayaout.setTitle(os.path.basename(str(musicList[index])))
        except:
            QMessageBox.information(self,'Warning', 'System Error')

    def forwardSong(self):
        global forward
        global count
        global soundLength
        self.progressBar.setValue(count)
        try:
            if forward == False:
                mixer.music.pause()
                if count > 59:
                    mixer.music.play(loops=0, start=90)
                    count += 90
                    if count > 225:
                        self.nextFuncSong = Timer(1, self.nextSounds())
                mixer.music.play(loops=0, start=30)
                mixer.music.unpause()
                forward = True
                count += 30
                if count >= soundLength:
                    self.nextFuncSong = Timer(1, self.nextSounds())
                    print(count, soundLength)
            else:
                mixer.music.pause()
                if count > 119:
                    mixer.music.play(loops=0, start=145)
                    count += 145
                mixer.music.play(loops=0, start=60)
                mixer.music.unpause()
                forward = False
                count += 60
                if count >= soundLength:
                    self.nextFuncSong = Timer(1, self.nextSounds())
                    print(count, soundLength)
        except:
            QMessageBox.information(self, 'Warning', 'System error')


    def nextSounds(self):
        global soundLength
        global count
        global index
        count = 0
        items = self.playList.count()
        index += 1
        if index == items or index > items: # '>' if delete last song
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
            QMessageBox.information(self, 'Warning', 'System error')

    def pauseSounds(self):
        global paused
        global pauseValue
        try:
            if paused == False:
                mixer.music.pause()
                paused = True
                pauseValue = self.progressBar.value()
                self.timer.stop()
            else:
                mixer.music.unpause()
                paused = False
                pauseProgressBar = True
                self.timer.start()
        except:
            QMessageBox.information(self, 'Warning', 'System Error')

    def stopSounds(self):
        self.timer.stop()
        mixer.music.stop()
        self.songTimmerLabel.setText('00:00')
        self.progressBar.setValue(0)

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
            QMessageBox.information(self, 'Warning', 'System Error')


    def exit(self):
        self.close()
        self.t.cancel()

    def exitTimmer(self):
        value = self.combo.currentText()
        try:
            if value == '15':
                mbox = QMessageBox.question(self, 'Information!!!', 'Are you sure to exit?',QMessageBox.Yes | QMessageBox.No | QMessageBox.No, QMessageBox.No)
                if mbox == QMessageBox.Yes:
                    self.t = Timer(900, self.exit)
                    self.t.start()
                    QMessageBox.information(self, 'Information', 'Music player closes after 15 minutes')
            elif value == '30':
                mbox = QMessageBox.question(self, 'Information!!!', 'Are you sure to exit?',QMessageBox.Yes | QMessageBox.No | QMessageBox.No, QMessageBox.No)
                if mbox == QMessageBox.Yes:
                    self.t = Timer(1800, self.exit)
                    self.t.start()
                    QMessageBox.information(self, 'Information', 'Music player closes after 30 minutes')
            elif value == '45':
                mbox = QMessageBox.question(self, 'Information!!!', 'Are you sure to exit?',QMessageBox.Yes | QMessageBox.No | QMessageBox.No, QMessageBox.No)
                if mbox == QMessageBox.Yes:
                    self.t = Timer(2700, self.exit)
                    self.t.start()
                    QMessageBox.information(self, 'Information', 'Music player closes after 45 minutes')
            elif value == '60':
                mbox = QMessageBox.question(self, 'Information!!!', 'Are you sure to exit?',QMessageBox.Yes | QMessageBox.No | QMessageBox.No, QMessageBox.No)
                if mbox == QMessageBox.Yes:
                    self.t = Timer(3600, self.exit)
                    self.t.start()
                    QMessageBox.information(self, 'Information', 'Music player closes after 60 minutes')
            elif value == '120':
                mbox = QMessageBox.question(self, 'Information!!!', 'Are you sure to exit?',QMessageBox.Yes | QMessageBox.No | QMessageBox.No, QMessageBox.No)
                if mbox == QMessageBox.Yes:
                    self.t = Timer(7200, self.exit)
                    self.t.start()
                    QMessageBox.information(self, 'Information', 'Music player closes after 120 minutes')
        except:
            QMessageBox.warning(self, 'Warning', 'System errors')

    def updateLabel(self):
        self.timerLabelTime.start(1000)
        current_time = datetime.now().time()
        self.countDownLabel.setText(str(current_time))

    def themesChange(self):
        global themes
        if themes == True:
            self.setStyleSheet('background-color:#294B6B;')
            self.progressBar.setStyleSheet(style.progressBarStyleDark())
            self.volumeSlider.setStyleSheet(style.sliderStyleDark())
            self.playList.setStyleSheet(style.listBoxStyleDark())
            self.topGroupLayaout.setStyleSheet(style.groupBoxStyleDark())
            self.combo.setStyleSheet('color:white;')
            self.countDownLabel.setStyleSheet('color:white;')
            themes = False
        else:
            self.setStyleSheet('background-color:#D0ECE7;')
            self.progressBar.setStyleSheet(style.progressBarStyle())
            self.volumeSlider.setStyleSheet(style.sliderStyle())
            self.playList.setStyleSheet(style.listBoxStyle())
            self.topGroupLayaout.setStyleSheet(style.groupBoxStyle())
            self.combo.setStyleSheet('color:black;')
            self.countDownLabel.setStyleSheet('color:black;')
            themes = True


def main():
    app = QApplication(sys.argv)
    window = Player()
    window.updateLabel()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()




