import inspect
import json
import os
import time
from libs3tl import Step
import pandas as pd

class Transform(Step.Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Tr"
        self.paramsFile = 'Transform.properties'
        self.logger = 'logTransform'
        self.logFile = self.getRelativeFile(os.getcwd() + '\../logs/Transform.log')
        self.preStep= "Ex"


    def startup(self):
        super(Transform,self).startup()
        self.startSubscriber()

    def doWorkAndHandoff(self):
        pass

    def doWork(self):
        pass