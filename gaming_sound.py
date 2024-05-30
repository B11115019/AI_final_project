import winsound
from playsound import playsound

def PressButton():
    playsound("data/pressButton.wav", False)
    #winsound.PlaySound("data/pressButton.wav", winsound.SND_ASYNC | winsound.SND_FILENAME | winsound.SND_NOSTOP)

def PressConfirm():
    playsound("data/pressConfirm.wav", False)
    #winsound.PlaySound("data/pressConfirm.wav", winsound.SND_ASYNC | winsound.SND_FILENAME | winsound.SND_NOSTOP)

def MainMenu():
    winsound.PlaySound("data/mainMenuSound.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def CountDown():
    winsound.PlaySound("data/countDown.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)

def Gaming():
    winsound.PlaySound("data/gamingSound.wav", winsound.SND_ASYNC | winsound.SND_FILENAME | winsound.SND_LOOP)

def BreakRecord():
    winsound.PlaySound("data/breakRecord.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)

def Loss():
    winsound.PlaySound("data/loss.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)