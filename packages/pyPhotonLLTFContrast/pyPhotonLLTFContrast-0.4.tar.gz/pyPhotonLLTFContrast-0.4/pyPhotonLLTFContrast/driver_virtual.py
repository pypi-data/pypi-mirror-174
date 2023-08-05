import ctypes
import os

class pyPhotonLLTFContrast():

    def __init__(self,dll_file=None):
        self.connected = False
        self.connected_device_name = ''
        self._wavelength = 1500
        # if dll_file:
        #     self.dll_file = dll_file
        # else:
        #     self.dll_file = os.path.join(os.path.dirname(__file__),"PE_Filter_SDK.dll")   #By default, we look for the DLL file in the same folder as the driver.py file
        # self.dll = ctypes.CDLL(self.dll_file)   #Open DLL file
        
        # self.handle = ctypes.c_void_p()         #Creates container for the handle to the instrument
        # self.handle_ptr = ctypes.byref(self.handle)
        
        # Initialize the DLL functions
        # self.devicename_size = 256
        # self.devicename_str = (ctypes.c_char*self.devicename_size)()
        # self.dll.PE_GetSystemName.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_char*self.devicename_size), ctypes.c_int]
        # self.dll.PE_Open.argtypes = [ctypes.c_void_p,  ctypes.POINTER(ctypes.c_char*self.devicename_size)]
        # self.dll.PE_GetWavelength.argtypes = [ctypes.c_void_p,  ctypes.POINTER(ctypes.c_double)]
        # self.dll.PE_GetWavelengthRange.argtypes = [ctypes.c_void_p,  ctypes.POINTER(ctypes.c_double),  ctypes.POINTER(ctypes.c_double)] 
        # self.dll.PE_SetWavelength.argtypes = [ctypes.c_void_p,  ctypes.c_double]
        # self.dll.PE_Close.argtypes = [ctypes.c_void_p]
        # self.dll.PE_Destroy.argtypes = [ctypes.c_void_p]
        

    def connect_device(self,device_xml_file:str):
        #device_xml_file = device_xml_file.encode('utf-8')
        #if (str(device_xml_file) and os.path.exists(device_xml_file) and device_xml_file.lower().endswith(b'.xml')):     
        #    returnVal = self.dll.PE_Create(device_xml_file,self.handle_ptr )
        #    if not(returnVal == 0):
        #        raise ValueError(f"It was not possible to create a connection to the instrument. Error code returned = {returnVal}")
        #    returnVal = self.dll.PE_GetSystemName(self.handle,0,ctypes.byref(self.devicename_str),self.devicename_size)
        self.connected_device_name = 'virtual_device'#self.devicename_str.value.decode("utf-8")
            
        #else:
        #    raise ValueError("device_xml_file must be the path to a valid .xml file for this instrument, provided by Photon etc. inc.")
        
        returnVal = 0#self.dll.PE_Open(self.handle,ctypes.byref(self.devicename_str))
        if returnVal == 0:
            self.connected = True
            self.read_parameters_upon_connection()
            return (0,self.connected_device_name)
        else:
            return (returnVal,'')

    def disconnect_device(self):
        if(self.connected == True):
            try:   
                returnVal = 0#self.dll.PE_Close(self.handle)
                if not(returnVal == 0):
                    raise ValueError(f"It was not possible to disconnect from the instrument. Error code returned by function PE_Close = {returnVal}")
                returnVal = 0#self.dll.PE_Destroy(self.handle)
                if not(returnVal == 0):
                    raise ValueError(f"It was not possible to disconnect from the instrument. Error code returned by function PE_Destroy = {returnVal}")
                ID = returnVal
                Msg = 'Succesfully disconnected.'
            except Exception as e:
                ID = -1 
                Msg = e
            if(ID==0):
                self.connected = False
            return (ID,Msg)
        else:
            raise RuntimeError("Device is already disconnected.")
            
    def read_parameters_upon_connection(self):
        self.read_min_max_wavelength()
        
    def check_valid_connection(self):
        if not(self.connected):
            raise RuntimeError("No device is currently connected.")

    def is_device_not_moving(self):
        '''
        Ideally, this function should allow to check whether the device is currently moving to a certain wavelength or not. This is useful in automatized processess, where, after
        setting a certain wavelength, one wants to be sure that the wavelength as been correctly set before proceeding to next operation.
        The .dll file of this instrument do not allow for this check. At the moment, this function returns always True. That is, it is assumed that any movement of the filter happens
        instantaneously
        '''
        return True

    @property
    def wavelength(self):
        self.check_valid_connection()
        #WL = ctypes.c_double(0)
        #self.dll.PE_GetWavelength(self.handle,ctypes.byref(WL))
        #self._wavelength = WL.value
        return self._wavelength

    @wavelength.setter
    def wavelength(self, wl):
        #Input variable wl can be either a string or a float or an int
        self.check_valid_connection()
        try:
            wl = float(wl)
        except:
            raise TypeError("Wavelength value must be a valid number")
        if wl<0:
            raise ValueError("Wavelength must be a positive number.")
        if wl<self.min_wavelength or wl>self.max_wavelength:
            raise ValueError(f"Wavelength must be between {self.min_wavelength} and {self.max_wavelength}.")
        returnVal = 0#self.dll.PE_SetWavelength(self.handle,wl)
        if not(returnVal == 0 or returnVal == 6):
            raise ValueError(f"It was not possible to set the wavelength. Error code returned by function PE_SetWavelength = {returnVal}")
        self._wavelength = wl
        return self._wavelength

    def move_by(self,delta_wl):
        try:
            delta_wl = float(delta_wl)
        except:
            raise TypeError("Wavelength shift value must be a valid number")
        new_wl = self.wavelength + delta_wl
        self.wavelength = new_wl
        return
    
    def read_min_max_wavelength(self):
        self.check_valid_connection()
        WL_min = 800 #ctypes.c_double(0)
        WL_max = 2100 #ctypes.c_double(0)
        returnVal = 0 #self.dll.PE_GetWavelengthRange(self.handle,ctypes.byref(WL_min),ctypes.byref(WL_max))
        if not(returnVal == 0 ):
            raise ValueError(f"It was not possible to retrieve the wavelength range. Error code returned by function PE_GetWavelengthRange = {returnVal}")
        self.min_wavelength = WL_min#.value
        self.max_wavelength = WL_max#.value
        return self.min_wavelength, self.max_wavelength