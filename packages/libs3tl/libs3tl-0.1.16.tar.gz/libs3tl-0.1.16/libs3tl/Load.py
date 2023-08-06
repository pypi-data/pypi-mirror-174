import os
from requests import Session
from libs3tl import Step

class Load(Step.Step): 
    
    def __init__(self):
        self.setStartTime()
        self.step = "Lo"
        self.paramsFile = 'Load.properties'
        self.logger = 'logLoad'
        self.logFile = self.getRelativeFile(os.getcwd() + '\../logs/Load.log')
        self.preStep= "Ml"
        
    def startup(self):
        super(Load,self).startup()
        self.startSubscriber()
    
    def doWork(self):
        pass
    
        
        
