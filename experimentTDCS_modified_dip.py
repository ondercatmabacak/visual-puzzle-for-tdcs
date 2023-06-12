import os
from psychopy import visual, core, data, event, logging, gui, misc, monitors
from psychopy.constants import *
from psychopy.hardware import crs
from numpy import *
from random import choice
from numpy.random import random, randint, normal, shuffle
import itertools
import numpy as np

# for gratings
from instructions import Instructions
from Responses import Responses


''' 
measuring contrast sensitiivty using N interleaved staircase procedures3
'''
#class Grating_presentation(object):
class Dipoles_presentation(object):
    
    #def __init__(self, win, dataFile, filename, expInfo, tfr=[1, 2], sfr=[1, 2], ntrials = 1,bit = 1):
    
    def __init__(self, win, dataFile, filename, expInfo, tfr=[18, 3], sfr=[1, 2], Rx=1, speed=1, contrastt=1, tstep=1, start = 1, ntrials = 1,bit = 1):
        self.win=win
        self.dataFile=dataFile
        self.filename=filename
        self.expInfo=expInfo
        self.tfr=tfr
        self.Rx=Rx
        self.speed=speed
        self.contrastt=contrastt
        self.tstep=tstep
        self.start=start
        self.trialClock=core.Clock()
        self.responseClock=core.Clock()
        self.sfr=sfr
        self.ntrials = ntrials
        self.bits = bit


    def run(self):
        # create list of trials
        conditions = [ i for i in itertools.product (self.tfr, self.sfr)] # create list of conditions
        for i in range(len(conditions)):
            conditions[i] = (conditions[i][0], conditions[i][1], i)
        cond = repeat(conditions, self.ntrials, axis = 0).tolist() # create minimum 20 trials per condition
        shuffle(cond)
        nextValue = [0.2   for i in range(len(conditions))]
        gr = visual.GratingStim(self.win, tex = "sin",mask = "gauss", units = "deg", pos = (0, 0), size = 4*0.1, sf = 0.1, contrast = 0.8) #*(1/2.0612))
        response = Responses(self.win, self.bits)
        key_corr=[]
        index0 = 0
        while len(cond)>1:
            params = cond.pop(0)
            tfreq = params[0]
            sfreq = params[1]
            nextIndex = int(params[2])
            dir = self.trial(self.win, gr, tfreq, sfreq, nextValue[nextIndex])
            key=response.run()
            if (key=='left'):
                key_c = -1 # we ask value to go down
            elif (key == 'right' ):
                key_c = 1 # we ask value to go up
            key_corr = append(key_corr, key_c * dir)
            self.dataFile.write('%.3f %.3f %.6f %i %i \n' %(tfreq, sfreq, nextValue[nextIndex], int(key_c), int(key_corr[-1]))) # +str(self.alphas) + str(startPosEllipse[:,0]) + str(startPosEllipse[:,1]))
            #self.mask(self.win)
            nextValue[nextIndex] = self.staircase(nextValue[nextIndex], key_corr)
            if (index0+1)%50==0:
                instruction_break=Instructions(self.win, 2)
            index0+=1
        self.bits.setContrast(1.0)
        instruction_break=Instructions(self.win, 2)

                
    def staircase(self, contrast, response):
        try:
            a=response[-1]
        except IndexError:
            a=-1
        try:
            b=response[-2]
        except IndexError:
            b=-1
        diff = log10(contrast)
        #print a,  b
        #print diff
        if (a==1) and (b==1): # 2 correct responces
            diff = diff-0.25 # decrease the value
        elif (a==1) and (b==-1):
            diff = diff
        elif (a==-1) and (b==1):
            diff = diff+0.25 # increase the value
        elif (a==-1) and (b==-1):
            diff = diff+0.25 # increase the value
        contrast = 10**(diff)
        #print diff
        if contrast > 1.0:
            contrast = 0.99
        if contrast<0.004:
            contrast = 0.004
        return contrast


    def trial(self, win, gr, tfreq, sfreq, nextValue):
        #ap = visual.Aperture(self.win, 15, pos=(0, 0), ori=0, nVert=120, shape='circle')
        direction = choice((-1, 1))
        gr.sf = sfreq
        #self.bits.setContrast(nextValue, gammaCorrect = "software")
        gr.size =8
        filename='data_response/' + '_frame_intervals' + data.getDateStr()+'.txt'#add a simple timestamp
        #Start of routine trial
        t=0; self.trialClock.reset()
        frameN=-1 
        trialComponents=[]#to keep track of which have finished
        trialComponents.append(gr)
        for thisComponent in trialComponents:
            if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
        continueRoutine=True
        #print condit[1]
        while continueRoutine:
           # print frameN
            t=self.trialClock.getTime()
            frameN=frameN+1
           
            if frameN>=30:
                gr.setAutoDraw(True)
                gr.phase =  t*tfreq*direction # drift at 7 Hz
                if frameN>(30+18) or event.getKeys(['e']):
                    gr.setAutoDraw(False)
                    #self.bits.setContrast(1.0, gammaCorrect = "software")
                    continueRoutine=False
                    for thisComponent in trialComponents:
                        if hasattr(thisComponent,'status'): thisComponent.status = FINISHED
                    
            for thisComponent in trialComponents:
                if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                    continueRoutine=True; break#at least one component has not yet finished
            if not continueRoutine:
                #self.bits.setContrast(1.0)
                break # lets a component forceEndRoutine
            if event.getKeys(["escape"]): 
                self.bits.setContrast(1.0)
                core.quit()
            if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                self.win.flip()
                self.win.clearBuffer()
            for thisComponent in trialComponents:
                if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
        
        return direction
                



#class ExperimentGratings(object):
class ExperimentDipoles(object):
    
    def __init__(self):
        #self.gratingeI, self.gratingdF, self.gratingfn, self.lumsGr = self.save_data()
        self.dipoleseI, self.dipolesdF, self.dipolesfn, self.lumsD = self.save_dataDipoles()
        #self.LatticeeI, self.LatticedF, self.Latticefn = self.save_dataLattices()

        self.instructionClock=core.Clock()
        self.feedbackClock=core.Clock()

       
    def run(self):
        self.win =self.create_window()
        #self.bits = self.create_bits(self.win)
       
        self.win.setColor((-1, -1, -1))
        myInstruction=Instructions(self.win, 6)
        speeds=[0.25, 0.34, 0.7, 1.2] #removed 0.15            #speed=[0.38, 0.64]  # the travelled distance is 0.06, 0.09, 0.15, 0.25, 0.5 # removed:0.15
        temporal_step=[2, 4]#[2, 4] #temporal_step=[1,2,4,6,10,20]
        st = [18, 3]
        ExpDipoles=Dipoles_presentation(self.win, dataFile=self.dipolesdF, filename=self.dipolesfn, expInfo=self.dipoleseI, Rx=3, speed=speeds, contrastt=1, tstep=temporal_step, start = st, ntrials = 15)#, bits = self.bits) # 208 trials
        ExpDipoles.run()
        
        #self.win.setColor((0, 0, 0))
        #Instruction=Instructions(self.win, 8)
        #sfreq=[0.1, 0.3, 1.0, 3.0, 9.0]#[0.38, 0.64, 1.1, 1.9]#[0.38, 0.55, 0.74, 1.28], 0.64, 1.1, 1.9, 3.0
        #tfreq=[7.35, 3.67]#[3.67, 7.35] # ,3,4] # 2,3 
        #ExpGrating=Grating_presentation(self.win, dataFile=self.gratingdF, filename=self.gratingfn, expInfo=self.gratingeI, tfr = tfreq, sfr = sfreq, ntrials = 30)#, bit =self.bits) # 300 trials
        #ExpGrating.run()
        
#        Instruction=InstructionsLattices(self.win, 8)
#        distance=[0.2, 0.38, 0.64, 1.1, 1.9]#[0.38, 0.55, 0.74, 1.28], 0.64, 1.1, 1.9, 3.0
#        ratio = 1.3
#        contrast=1.0
#        tstep=[2] # 2,3 
#        ExpLattices=LatticePresentation(self.win, dataFile=self.LatticedF, filename=self.Latticefn, expInfo=self.LatticeeI, temporal_steps=tstep, ratio1 = ratio, distances = distance, ntrials = 8, con1 = contrast, bits = self.bits)
#        ExpLattices.run()
        instruction_feedback=Instructions(self.win, 3)
        self.win.close()
        

    def save_data(self):
        #store info about the experiment session
        expName='Contrast_'#from the Builder filename that created this script
        expInfo={'participant':'', 'Experiment': 'tDCS_Contrast', 'Luminance':['50', '15']}
        dlg=gui.DlgFromDict(dictionary=expInfo, title=expName)
        if dlg.OK==False: core.quit() #user pressed cancel
        expInfo['date']=data.getDateStr()#add a simple timestamp
        expInfo['expName']=expName 
        lum = expInfo['Luminance']
        #setup files for saving
        if not os.path.isdir('data_response'):
            os.makedirs('data_response') #if this fails (e.g. permissions) we will get error
        filename='data_response' + os.path.sep +'%s_%s_%s_%s' %(expInfo['participant'], expInfo['Experiment'], expInfo['Luminance'], expInfo['date'])
        dataFile=open(filename +'.txt', 'w')
        dataFile.write('temporal_frequency spatial frequency contrast key_pressed  correct\n')# alphas     xStart      yStart')
        logFile=logging.LogFile(filename+'.log', level=logging.EXP)
        logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file
        return expInfo, dataFile, filename, lum
        
    def save_dataDipoles(self):
        #store info about the experiment session
        expName='None'#from the Builder filename that created this script
        expInfo={'participant':'', 'Experiment': 'tDCS_Dipoles', 'Luminance':['50', '15']}
        dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
        if dlg.OK==False: core.quit() #user pressed cancel
        expInfo['date']=data.getDateStr()#add a simple timestamp
        expInfo['expName']=expName
        lum = expInfo['Luminance']
        #setup files for saving
        if not os.path.isdir('results'):
            os.makedirs('results') #if this fails (e.g. permissions) we will get error
        filename='results' + os.path.sep +'%s_%s_%s_%s' %(expInfo['participant'], expInfo['Experiment'], expInfo['Luminance'], expInfo['date'])
        dataFile=open(filename +'.txt', 'w')
        dataFile.write('Rx angle temporal_step motion_distance  contrast  number size  correct\n')# alphas     xStart      yStart')
        logFile=logging.LogFile(filename+'.log', level=logging.EXP)
        logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file
        return expInfo, dataFile, filename, lum
        
    def save_dataLattices(self):
        #store info about the  session with lattices
        expName='MotionLatticesRandomized'#from the Builder filename that created this script
        expInfo={'participant':'', 'Experiment': 'Motion Lattices Randomized'}
        dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
        if dlg.OK==False: core.quit() #user pressed cancel
        expInfo['date']=data.getDateStr()#add a simple timestamp
        expInfo['expName']=expName 
        #setup files for saving
        if not os.path.isdir('data_response'):
            os.makedirs('data_response') #if this fails (e.g. permissions) we will get error
        filename='data_response' + os.path.sep +'%s_%s_%s' %(expInfo['participant'], expInfo['Experiment'], expInfo['date'])
        dataFile=open(filename +'.txt', 'w')
        dataFile.write('temporal_step distance1 ratio1 ratio2 diameter keyPressed keyCorrect\n')# alphas     xStart      yStart')
        logFile=logging.LogFile(filename+'.log', level=logging.EXP)
        logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file
        return expInfo, dataFile, filename
        
    def create_window(self):
        mon = monitors.Monitor("DELL2410")
        mon.setDistance(80)
        mon.setSizePix((1366, 768))
        mon.setWidth(60)
        linMethod = 1#monitor.getLineariseMethod()#typically = 1
        currentCal = mon.currentCalib['gammaGrid']
        print (currentCal)
        # for contrast 50, luminance 50
        # for contrast 50, luminance 50
        if (self.lumsD =='50'):#(self.lumsGr==self.lumsD and self.lumsD =='50'):
            lums =np.array(([0.22, 1.52, 5.24, 11.34, 19.3, 29.4, 39.6], [0.21, 4.11, 15.37, 33.2, 57.0, 84.1, 111.7], [0.21, 0.62, 1.64, 3.36, 5.71, 8.53, 11.55], [0.2, 5.95, 22.4, 48.5, 82.2, 121.8, 162.2] ))
        if (self.lumsD =='15'):#(self.lumsGr==self.lumsD and self.lumsD =='15'):
        # for contrast 15, luminance 50
            lums =np.array(([0.19, 0.27, 0.58, 1.1, 1.8, 2.67, 3.78], [0.19, 0.39, 1.35, 3.00, 5.25, 8.04, 11.52], [0.19, 0.21, 0.3, 0.46, 0.65, 0.92, 1.25], [0.19, 0.5, 1.95, 4.34, 7.59, 11.65, 16.63] ))
        #if (self.lumsD == self.lumsD):#self.lumsGr!=self.lumsD:
        #    print ("Error: Please choose one luminance value for both experiments")
            core.quit()
        for gun in [0,1,2,3]:
            gamCalc = monitors.GammaCalculator([0, 42, 84, 126, 168, 210, 255], lums[gun], eq=linMethod)
            print (vars(gamCalc))
            currentCal[gun,0]=lums[gun,0]#min
            currentCal[gun,1]=lums[gun,-1]#max
            currentCal[gun,2]=gamCalc.gamma#gamma
        print (currentCal)
        mon.saveMon()
        win = visual.Window(size=(1366, 768), useFBO=True, fullscr=True, screen=0, allowGUI=False, allowStencil=True,
        monitor= mon, color=[0, 0, 0], colorSpace='rgb', units='deg')
        return win
        
    #def create_bits(self, win):
        #bits = crs.BitsSharp(win, mode = 'bits++', checkConfigLevel = 2, gammaCorrect = "software")
        #core.wait(0.5)
        #print (bits.info)
        #if not bits.OK: 
                #print ('failed to connect to Bits box')
                #core.quit()
        #bits.mode = 'bits++' # 'color++', 'mono++', 'bits++', 'auto++' or 'status'
        #bits.temporalDithering = True
        #return bits




Experiment=ExperimentDipoles()#ExperimentGratings()
Experiment.run()#Experiment.run()


