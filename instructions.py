from psychopy import visual, core, data, event, logging, gui, misc
from psychopy.constants import *

class Instructions(object):
    
    ''' Defines a routine for the instruction
    Instructions (win=window, instruction_number=selects option for the text presented on the instruction screen)'''
    
    def __init__(self, win, instruction_number):
        self.win=win
        self.text1='''Please look at the spinning dot duplets and increase or decrease frame duration with keys "q" and "p" until you see tilting of the circle. Press "e" to save your response and proceed to the next trial. To star, press space bar.'''
        self.text2='''You may have a break now. Press space bar when ready to continue.'''
        self.text3='''You have finished the session. Thank you!'''
        self.text4=''' Please look at the spinning dot duplets and increase or decrease the distance between the dots with keys "q" and "p" until you see tilting of the circle. Press "e" to save your response and proceed to the next trial. To start, pres space bar.''' 
        self.text5='''You finished the first part of the experiment. Press space bar to proceed to the second part.'''
        self.text6='''Please watch a presentation and response if you saw spinning of dot pairs or tilting of the circle'''
        self.text7='''Please watch a presentation and with keys "q" and "p" decrease or increase the contrast of the elements until you just start seeing them organized in rows. Press "e" to save your response. To start, press space bar.'''
        self.text8='''Please watch a presentation and report the direction of motion. To start, press the space bar.'''

        if instruction_number==1:
            self.text=self.text1
        if instruction_number==2:
            self.text=self.text2
        if instruction_number==3:
            self.text=self.text3
        if instruction_number==4:
            self.text=self.text4
        if instruction_number==5:
            self.text=self.text5
        if instruction_number==6:
            self.text=self.text6
        if instruction_number==7:
            self.text=self.text7
        if instruction_number==8:
            self.text=self.text8
            
        self.instruction_breakClock=core.Clock()
        text_instruction_break = visual.TextStim(self.win, ori=0, text=self.text, font=u'Arial', pos=[0, 0], height=1.0, wrapWidth=20, color=u'white', colorSpace=u'rgb', opacity=1, depth=0.0)
        t=0; self.instruction_breakClock.reset()
        frameN=-1
        key_resp = event.BuilderKeyResponse() #create an object of type KeyResponse
        continueRoutine=True
        while continueRoutine:
            t=self.instruction_breakClock.getTime()
            frameN=frameN+1
            if frameN>=0 and key_resp.status==NOT_STARTED:
                text_instruction_break.setAutoDraw(True)
                key_resp.status=STARTED
                key_resp.clock.reset() # now t=0
                event.clearEvents()
            if key_resp.status==STARTED:#only update if being drawn
                theseKeys = event.getKeys(keyList=['space'])
            if len(theseKeys)>0:#at least one key was pressed
                key_resp.keys=theseKeys[-1]#just the last key pressed
                #abort routine on response
                text_instruction_break.setAutoDraw(False)
                continueRoutine=False
            if event.getKeys(["escape"]): core.quit()
            #refresh the screen
            if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                self.win.flip()
