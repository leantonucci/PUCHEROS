import sys, time, logging
import PyIndi
import threading

class IndiClient(PyIndi.BaseClient):
 
    device = None
 
    def __init__(self, exposure_time, gain, offset):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.logger.info('creating an instance of PyQtIndi.IndiClient')
        self.exposure_time = exposure_time
        self.gain = gain
        self.offset = offset
        self.abort_thread = threading.Thread(target=self.abort_exposure)
    def newDevice(self, d):
        self.logger.info("new device " + d.getDeviceName())
        if d.getDeviceName() == "QHY CCD QHY5LII-M-60b7e":
            self.logger.info("Set new device QHY CCD QHY5LII-M-60b7e!")
            # save reference to the device in member variable
            self.device = d
    def newProperty(self, p):
        self.logger.info("new property "+ p.getName() + " for device "+ p.getDeviceName())
        if self.device is not None and p.getName() == "CONNECTION" and p.getDeviceName() == self.device.getDeviceName():
            self.logger.info("Got property CONNECTION for QHY-5L-II CCD!")
            # connect to device
            self.connectDevice(self.device.getDeviceName())
            # set BLOB mode to BLOB_ALSO
            self.setBLOBMode(1, self.device.getDeviceName(), None)
        if p.getName() == "SDK_VERSION":
            # take first exposure
            self.takeExposure(self.exposure_time,self.gain, self.offset)
            self.abort_thread.start()
    def removeProperty(self, p):
        self.logger.info("remove property "+ p.getName() + " for device "+ p.getDeviceName())
    def newBLOB(self, bp):
        self.logger.info("new BLOB "+ bp.name)
        # get image data
        img = bp.getblobdata()
        # write image data to BytesIO buffer
        import io
        blobfile = io.BytesIO(img)
        # open a file and save buffer to disk
        #with open("frame.fit", "wb") as f:
         #   f.write(blobfile.getvalue())
        # start new exposure
        self.takeExposure(self.exposure_time, self.gain, self.offset)
    def newSwitch(self, svp):
        self.logger.info ("new Switch "+ svp.name + " for device "+ svp.device)
    def newNumber(self, nvp):
        self.logger.info("new Number "+ nvp.name + " for device "+ nvp.device)
    def newText(self, tvp):
        self.logger.info("new Text "+ tvp.name + " for device "+ tvp.device)
    def newLight(self, lvp):
        self.logger.info("new Light "+ lvp.name + " for device "+ lvp.device)
    def newMessage(self, d, m):
        #self.logger.info("new Message "+ d.messageQueue(m))
        pass
    def serverConnected(self):
        print("Server connected ("+self.getHost()+":"+str(self.getPort())+")")
    def serverDisconnected(self, code):
        self.logger.info("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")
    def takeExposure(self, exposure_time, gain, offset):
        self.logger.info(">>>>>>>>")
        #get current exposure time
        ccd_exposure = self.device.getNumber("CCD_EXPOSURE")
        ccd_gain = self.device.getNumber("CCD_GAIN")
        ccd_offset = self.device.getNumber("CCD_OFFSET")
        ccd_abort_exposure = self.device.getSwitch("CCD_ABORT_EXPOSURE")
        #for i in ccd_abort_exposure:
            #print("       "+i.name+" = "+str(i.s))
        # set exposure time for captures
        ccd_exposure[0].value = exposure_time
        ccd_gain[0].value = gain
        ccd_offset[0].value = offset
        #STATUS
        for t in ccd_exposure:
            print("       "+t.name+" = "+str(t.value))
        # send new exposure time to server/device
        self.sendNewNumber(ccd_gain)
        self.sendNewNumber(ccd_offset)
        self.sendNewNumber(ccd_exposure)
        
        
    def abort_exposure(self):
        # Deactivate streaming
        #ccd_exposure = self.device.getNumber("CCD_EXPOSURE")
        ccd_abort_exposure = self.device.getSwitch("CCD_ABORT_EXPOSURE")
        choice = input("Abort exposure?: ")
        if choice == "yes" or choice =="YES" or choice == "Yes" or choice == "1":
            print("Ending exposure")
            #ccd_exposure[0].value = 0
            #ccd_abort_exposure[0].s = 0
            #self.sendNewNumber(ccd_exposure)
            self.sendNewSwitch(ccd_abort_exposure)
        else:
            print("Exposure continues")
        #for t in ccd_exposure:
         #   print("       "+t.name+" = "+str(t.value))
        for i in ccd_abort_exposure:
            print("       "+i.name+" = "+str(i.s))

str_exposure_time = input("Choose exposure time: ")
str_gain = input("Choose gain: ")
str_offset = input("Choose offset: ")
exposure_time = float(str_exposure_time)
gain = int(str_gain)
offset = int(str_offset)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
 
# instantiate the client
indiclient=IndiClient(exposure_time, gain, offset)
print(f"Tipo: {type(indiclient)}")
# set indi server localhost and port 7624
indiclient.setServer("localhost",7624)
# connect to indi server
print("Connecting to indiserver")
if (not(indiclient.connectServer())):
     print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
     print("  indiserver indi_simulator_telescope indi_simulator_ccd")
     sys.exit(1)

  
# start endless loop, client works asynchron in background
while True:
    time.sleep(1)