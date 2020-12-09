def groupBoxStyle():
    return """
        QGroupBox {
        background-color: #D0ECE7;
        font:8pt Times Bold;
        color:#2C3E50;
        border:2px solid #2C3E50;
        border-radius:12px;
        }
    """

def listBoxStyle():
    return """
        QListWidget {
        background-color:#2C3E50;
        font:10pt Times Bold; 
        color:#D0ECE7;
        border:2px solid #D0ECE7;
        border-radius:4px;    
        }
    """

def progressBarStyle():
    return """
    QProgressBar {
    border:1px solid #7B241C;
    background: #D0ECE7;
    height: 5px;
    border-radius: 6px;
    }
    QProgressBar::chunk {
     background-color: #05B8CC;
    }
    """

def sliderStyle():
    return """
    QSlider{
    border:1px solid #7B241C;
    background: #D0ECE7;
    height: 8px;
    border-radius: 6px;
    }
    """