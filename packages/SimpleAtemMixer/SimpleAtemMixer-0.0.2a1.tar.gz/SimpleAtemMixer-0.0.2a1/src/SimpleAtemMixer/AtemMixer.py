
import PyATEMMax

class AtemMixer:

    def __init__(self, ip):
        self.connectionIP = ip
        self.switcher = PyAtemMax.ATEMMax()
        self.switcher.connect(self.connectionIP)
        self.switcher.waitForConnection()
        print("Connected to " + self.connectionIP)


    def disconnect(self):
        self.switcher.disconnect()

    def getProgramOutput(self):
        if self.switcher.isConnected:
            return self.switcher.programInput[0].videoSource
        return "unknown"

    def getPreviewOutput(self):
        if self.switcher.isConnected:
            return self.switcher.previewInput[0].videoSource
        return "unknown"
    

    def __str__(self):
        return "Connection to " + self.connectionIP