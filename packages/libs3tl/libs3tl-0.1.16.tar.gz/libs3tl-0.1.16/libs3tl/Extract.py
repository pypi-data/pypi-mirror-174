import os
from requests import Request, Session
from libs3tl import Step
import websocket


class Extract(Step.Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Ex"
        self.paramsFile = 'Extract.properties'
        self.logger = 'logExtract'
        self.logFile =self.getRelativeFile(os.getcwd() +'\../logs/Extract.log') 
        self.preStep = ""

    def startup(self):
        super(Extract,self).startup()

    
    def doWorkAndHandoff(self):
        pass

    def doWork(self):
        pass


    

   
