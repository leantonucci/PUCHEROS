import sys, time, logging
import PyIndi
import threading
  
class IndiClient(PyIndi.BaseClient):
 
    device = None
 
    def __init__(self, gain, offset, streaming_exposure, delay):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.logger.info('creating an instance of PyQtIndi.IndiClient')
        self.gain = gain
        self.offset = offset
        self.streaming_exposure = streaming_exposure
        self.delay = delay
        self.abort_thread = threading.Thread(target=self.abort_stream)
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
            #self.setBLOBMode(1, self.device.getDeviceName(), None)
        if p.getName() == "SDK_VERSION":
            # take first exposure
            self.takeExposure(self.gain, self.offset, self.streaming_exposure, self.delay)
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
        #self.takeExposure(1,0,1,0.2)
    def newSwitch(self, svp):
        self.logger.info ("new Switch "+ svp.name + " for device "+ svp.device)
    def newNumber(self, nvp):
        self.logger.info("new Number "+ nvp.name + " for device "+ nvp.device)
    def newText(self, tvp):
        self.logger.info("new Text "+ tvp.name + " for device "+ tvp.device)
        if tvp.name == "ACTIVE_DEVICES":
            pass
    def newLight(self, lvp):
        self.logger.info("new Light "+ lvp.name + " for device "+ lvp.device)
    def newMessage(self, d, m):
        #self.logger.info("new Message "+ d.messageQueue(m))
        pass
    def serverConnected(self):
        print("Server connected ("+self.getHost()+":"+str(self.getPort())+")")
    def serverDisconnected(self, code):
        self.logger.info("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")
    def takeExposure(self, gain, offset, s_exposure, delay):
        self.logger.info(">>>>>>>>")
        #get current exposure time
        ccd_exposure = self.device.getNumber("CCD_EXPOSURE")
        ccd_gain = self.device.getNumber("CCD_GAIN")
        ccd_offset = self.device.getNumber("CCD_OFFSET") 
        ccd_video_stream = self.device.getSwitch("CCD_VIDEO_STREAM")
        streaming_exposure = self.device.getNumber("STREAMING_EXPOSURE")
        stream_delay = self.device.getNumber("STREAM_DELAY")
        # Activate streaming
        ccd_video_stream[0].s = 1
        ccd_video_stream[1].s = 0
        for t in ccd_video_stream:
                print("       "+t.name+" = "+str(t.s))
        # set exposure time for streaming
        ccd_gain[0].value = gain
        ccd_offset[0].value = offset
        streaming_exposure[0].value = s_exposure
        stream_delay[0].value = delay
        # send new exposure time to server/device
        self.sendNewNumber(ccd_gain)
        self.sendNewNumber(ccd_offset)
        self.sendNewNumber(streaming_exposure)
        self.sendNewNumber(stream_delay)
        self.sendNewSwitch(ccd_video_stream)
        self.abort_thread.start()
        
    def abort_stream(self):
        # Deactivate streaming
        ccd_video_stream = self.device.getSwitch("CCD_VIDEO_STREAM")
        choice = input("Abort stream?: ")
        if choice == "yes" or choice =="YES" or choice == "Yes" or choice == "1":
            print("Ending stream")
            ccd_video_stream[0].s = 0
            ccd_video_stream[1].s = 1
            self.sendNewSwitch(ccd_video_stream)
        else:
            print("Stream continues")
        for t in ccd_video_stream:
                print("       "+t.name+" = "+str(t.s))
        
str_gain = input("Choose gain: ")
str_offset = input("Choose offset: ")
str_streaming_exposure = input("Choose streaming exposure time: ")
str_delay = input("Choose stream delay: ")
gain = int(str_gain)
offset = int(str_offset)
streaming_exposure = float(str_streaming_exposure)
delay = float(str_delay)
  
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
 
# instantiate the client
indiclient=IndiClient(gain, offset,streaming_exposure, delay)
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