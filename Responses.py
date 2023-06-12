from psychopy import visual, core, data, event, logging, gui, misc
from psychopy.constants import * #things like STARTED, FINISHED

class Responses(object):
    
    ''' Defines a routine for the response
    Resposes(win=window, response_number=selects option for the text presented on the response screen)'''
    
    def __init__(self, win, bits):
        self.win=win
        text4= "left                                                             right"
        self.text=text4
        self.keylist=['left','right']
        self.responseClock=core.Clock()
        self.bits = bits
        
    def run(self):
        #Start of routine response
        text_1=visual.TextStim(self.win, ori=0, name='text_1',
        text=self.text, alignHoriz='center', alignVert='top',    font=u'Arial',
        pos=[0, -2.0], height=0.5,
        color=u'white', wrapWidth=20, colorSpace=u'rgb', units='deg')
        t=0; self.responseClock.reset()
        frameN=-1
        key_resp_2 = event.BuilderKeyResponse() #create an object of type KeyResponse
        key_resp_2.status=NOT_STARTED
        #keep track of which have finished
        responseComponents=[]#to keep track of which have finished
        responseComponents.append(key_resp_2)
        continueRoutine=True
        while continueRoutine:
            t=self.responseClock.getTime()
            frameN=frameN+1#number of completed frames (so 0 in first frame)
            if t>=0.0 and key_resp_2.status==NOT_STARTED:
                event.clearEvents()
                text_1.setAutoDraw(True)
                key_resp_2.status=STARTED
            if key_resp_2.status==STARTED:#only update if being drawn
                theseKeys = event.getKeys(keyList=self.keylist)
                if len(theseKeys)>0:#at least one key was pressed
                    key_resp_2.keys=theseKeys[-1]#just the last key pressed
                    key_resp_2.rt = self.responseClock.getTime()
                    text_1.setAutoDraw(False)
                    continueRoutine=False
            #check if all components have finished
            if not continueRoutine:
                break # lets a component forceEndRoutine
            continueRoutine=False#will revert to True if at least one component still running
            for thisComponent in responseComponents:
                if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                    continueRoutine=True; break#at least one component has not yet finished
            #check for quit (the [Esc] key)
            if event.getKeys(["escape"]): core.quit()
            #refresh the screen
            if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                self.win.flip()
        return key_resp_2.keys
