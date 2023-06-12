from psychopy import visual, logging
from psychopy.hardware import crs

logging.console.setLevel(logging.DEBUG)

win =  visual.Window(size=(1366, 768), useFBO=True, fullscr=True, screen=0, allowGUI=False, allowStencil=True)

bits= crs.BitsSharp(win, mode = 'bits++', checkConfigLevel = 2, gammaCorrect = "software")
core.wait(0.5)
print(bits, bits.OK)