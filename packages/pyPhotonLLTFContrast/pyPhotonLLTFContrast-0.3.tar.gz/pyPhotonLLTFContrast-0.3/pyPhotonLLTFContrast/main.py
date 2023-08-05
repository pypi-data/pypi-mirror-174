import os
import PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
import PyQt5.QtWidgets as Qt# QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import logging
import sys
import argparse

import abstract_instrument_interface
import pyPhotonLLTFContrast.driver_virtual
import pyPhotonLLTFContrast.driver

graphics_dir = os.path.join(os.path.dirname(__file__), 'graphics')

##This application follows the model-view-controller paradigm, but with the view and controller defined inside the same object (the GUI)
##The model is defined by the class 'interface', and the view+controller is defined by the class 'gui'. 

class interface(abstract_instrument_interface.abstract_interface):
    """
    Create a high-level interface with the device, validates input data and perform high-level tasks such as periodically reading data from the instrument.
    It uses signals (i.e. QtCore.pyqtSignal objects) to notify whenever relevant data has changes or event has happened. These signals are typically received by the GUI
    Several general-purpose attributes and methods are defined in the class abstract_interface defined in abstract_instrument_interface
    ...

    Attributes specific for this class (see the abstract class abstract_instrument_interface.abstract_interface for general attributes)
    ----------
    instrument
        Instance of driver.pyPhotonLLTFContrast
    connected_device_name : str
        Name of the physical device currently connected to this interface 
    settings = {   
                'device_file' : '',
                'step_size': 10,
                'ramp' : {  
                            'ramp_step_size': 1,
                            'ramp_wait_1': 1,
                            'ramp_wait_2': 1,
                            'ramp_numb_steps': 10,
                            'ramp_repeat': 1,
                            'ramp_reverse': 1,
                            'ramp_send_initial_trigger': 1
                            }
                }
    ramp 
        Instance of abstract_instrument_interface.ramp class 


    Methods
    -------
    connect_device(device_full_name)
        Connect to the device identified by device_full_name
    disconnect_device()
        Disconnect the currently connected device
    close()
        Closes this interface, close plot window (if any was open), and calls the close() method of the parent class, which typically calls the disconnect_device method
   
    set_connected_state()
        This method also calls the set_connected_state() method defined in abstract_instrument_interface.abstract_interface

    TO FINISH

    """

    output = {'Wavelength':0}  #We define this also as class variable, to make it possible to see which data is produced by this interface without having to create an object

    ## SIGNALS THAT WILL BE USED TO COMMUNICATE WITH THE GUI
    #                                                           | Triggered when ...                                        | Sends as parameter    
    #                                                       #   -----------------------------------------------------------------------------------------------------------------------         
    sig_update_wavelength = QtCore.pyqtSignal(float)        #   | Wavelength has changed/been read                          | New wavelength
    sig_step_size = QtCore.pyqtSignal(float)                #   | Step size has been changed or resetted                    | Step size
    sig_change_moving_status = QtCore.pyqtSignal(int)       #   | A movement has started or has ended                       | 1 = movement has started,  2 = movement has ended
    ##
    # Identifier codes used for view-model communication. Other general-purpose codes are specified in abstract_instrument_interface
    SIG_MOVEMENT_STARTED = 1
    SIG_MOVEMENT_ENDED = 2

    def __init__(self, **kwargs):
        self.output = {'Wavelength':0}
        ### Default values of settings (might be overlapped by settings saved in .json files later)
        self.settings = {   
                    'device_file' : '',
                    'step_size': 10,
                    'ramp' : {  
                                'ramp_step_size': 1,
                                'ramp_wait_1': 1,
                                'ramp_wait_2': 1,
                                'ramp_numb_steps': 10,
                                'ramp_repeat': 1,
                                'ramp_reverse': 1,
                                'ramp_send_initial_trigger': 1
                                }
                    }

        self.connected_device_name = ''
        self._units = 'nm'
        ###
        if ('virtual' in kwargs.keys()) and (kwargs['virtual'] == True):
            self.instrument = pyPhotonLLTFContrast.driver_virtual.pyPhotonLLTFContrast() 
        else:    
            self.instrument = pyPhotonLLTFContrast.driver.pyPhotonLLTFContrast() 
        ###
        super().__init__(**kwargs)
        # Setting up the ramp object, which is defined in the package abstract_instrument_interface
        self.ramp = abstract_instrument_interface.ramp(self)  
        self.ramp.set_ramp_settings(self.settings['ramp'])
        self.ramp.set_ramp_functions(func_move = self.instrument.move_by,
                                     func_check_step_has_ended = self.is_device_not_moving, 
                                     func_trigger = self.update, 
                                     func_trigger_continue_ramp = None,
                                     func_set_value = self.set_wavelength, 
                                     func_read_current_value = self.read_wavelength, 
                                     list_functions_step_not_ended = [self.read_wavelength],  
                                     list_functions_step_has_ended = [lambda:self.end_movement(send_signal=False)],  
                                     list_functions_ramp_ended = [])
        self.ramp.sig_ramp.connect(self.on_ramp_state_changed)

    def connect_device(self,device_file):
        '''
        Parameters
        ----------
        device_file : str
            Path of the .xml file which identifies the device

        Returns
        -------
        None.

        '''
        if(device_file==''): # Check  that the file name is not empty
            self.logger.error("No valid file path has been passed.")
            return
        self.set_connecting_state()
        self.logger.info(f"Connecting to device identified by the file {device_file}...")
        try:
            code,device_name = self.instrument.connect_device(device_file) 
            if(code==0):  #If connection was successful
                self.logger.info(f"Connected to device {device_name}.")
                self.connected_device_name = device_name
                self.settings['device_file']=device_file
                self.set_connected_state()
            else: #If connection was not successful
                self.logger.error(f"An error occurred when trying to connect to this device. Code returned = {code}")
                self.set_disconnected_state()
        except Exception as e:
            self.logger.error(f"An error occurred when trying to connect to this device: {e}")
            self.set_disconnected_state()

    def disconnect_device(self):
        self.logger.info(f"Disconnecting from device {self.connected_device_name}...")
        self.set_disconnecting_state()
        (code,Msg) = self.instrument.disconnect_device()
        if(code==0): # If disconnection was successful
            self.logger.info(f"Disconnected from device {self.connected_device_name}.")
            #self.continuous_read = 0 # We set this variable to 0 so that the continuous reading from the powermeter will stop
            self.set_disconnected_state()
        else: #If disconnection was not successful
            self.logger.error(f"Error: {Msg}")
            self.set_disconnected_state() #When disconnection is not succeful, it is typically because the device alredy lost connection
                                          #for some reason. In this case, it is still useful to have the widget reset to disconnected state      

    def close(self,**kwargs):
        self.settings['ramp'] = self.ramp.settings
        super().close(**kwargs)   

    def set_connected_state(self):
        self.min_max_wl = self.instrument.read_min_max_wavelength()
        self.read_wavelength()
        super().set_connected_state()

    def set_moving_state(self):
        self.sig_change_moving_status.emit(self.SIG_MOVEMENT_STARTED)
                             
    def set_non_moving_state(self): 
        self.sig_change_moving_status.emit(self.SIG_MOVEMENT_ENDED)

    def is_device_not_moving(self):
        # In the current implementation (see definition of instrument.is_device_not_moving()) This function will always return True.
        # We still define this function for compatibility reasons
        return self.instrument.is_device_not_moving()

    def on_ramp_state_changed(self,status):
        '''
        Slot for signals coming from the ramp object
        '''
        if status == self.ramp.SIG_RAMP_STARTED:
            self.set_moving_state()
            self.settings['ramp'] = self.ramp.settings
        if status == self.ramp.SIG_RAMP_ENDED:
            self.set_non_moving_state()
        
    def set_step_size(self, s):
        try: 
            step_size = float(s)
            if self.settings['step_size'] == step_size: #if the value passed is the same as the one currently stored, we end here
                return True
        except ValueError:
            self.logger.error(f"The step size must be a valid number.")
            self.sig_step_size.emit(self.settings['step_size'])
            return False
        self.logger.info(f"The step size is now {step_size}.")
        self.settings['step_size'] = step_size
        self.sig_step_size.emit(self.settings['step_size'])
        return True

    def move_single_step(self,direction,step_size = None):
        if step_size == None:
            step_size = self.settings['step_size']
        new_wl = self.instrument.wavelength + direction*step_size
        #self.logger.info(f"Will move by {step_size}. Begin moving...")
        #self.set_moving_state()
        self.set_wavelength(new_wl)
        #Start checking periodically the value of self.instrument.is_in_motion. It it's true, we read current
        #wavelength. When it becomes False, call self.end_movement
        #self.check_property_until(lambda : self.is_device_not_moving,[False,True],[[self.read_wavelength],[self.end_movement]])

    def read_wavelength(self):
        self.output['Wavelength'] = self.instrument.wavelength
        self.sig_update_wavelength.emit(self.output['Wavelength'])
        return self.output['Wavelength']
        
    def set_wavelength(self,wl):
        try:
            wl = float(wl)
        except:
            return
        self.logger.info(f"Moving to wavelength: {wl}...")
        try:
            self.set_moving_state()
            self.instrument.wavelength = wl
            self.check_property_until(self.is_device_not_moving,[False,True],[[self.read_wavelength],[self.end_movement]])
        except Exception as e:
            self.logger.error(f"An error occurred while setting the wavelength: {e}")
            self.sig_update_wavelength.emit(self.output['Wavelength'])

    def end_movement(self,send_signal = True):
        # When send_signal = False, the method self.set_non_moving_state() is NOT called, which means the signal self.sig_change_moving_status.emit(self.SIG_MOVEMENT_ENDED) is not emitted
        # This is useful, e.g., when doing a ramp, when at each step of the ramp we want to read the position but we do not want to send the signal that the movement has ended, so that the GUI remains disabled
        self.read_wavelength()
        self.logger.info(f"Movement ended. New wavelength = {self.output['Wavelength']}")
        if send_signal:
            self.set_non_moving_state()
            
    
class gui(abstract_instrument_interface.abstract_gui):
    """
    Attributes specific for this class (see the abstract class abstract_instrument_interface.abstract_gui for general attributes)
    ----------
    """
    def __init__(self,interface,parent):
        super().__init__(interface,parent)
        self.initialize()
       
    def initialize(self):
        self.create_widgets()
        self.connect_widgets_events_to_functions()

         ### Call the initialize method of the super class. 
        super().initialize()

        ### Connect signals from model to event slots of this GUI
        self.interface.sig_connected.connect(self.on_connection_status_change) 
        self.interface.sig_update_wavelength.connect(self.on_wavelength_change)
        self.interface.sig_step_size.connect(self.on_step_size_change)
        self.interface.sig_change_moving_status.connect(self.on_moving_state_change)
        #self.interface.ramp.sig_ramp.connect(self.on_ramp_state_change)
        self.interface.sig_close.connect(self.on_close)

        ### SET INITIAL STATE OF WIDGETS
        self.edit_StepSize.setText(str(self.interface.settings['step_size']))
        self.edit_File_xml.setText(self.interface.settings['device_file'])
        self.on_moving_state_change(self.interface.SIG_MOVEMENT_ENDED)
        self.on_connection_status_change(self.interface.SIG_DISCONNECTED) #When GUI is created, all widgets are set to the "Disconnected" state    
        ###


    def create_widgets(self):
        """
        Creates all widgets and layout for the GUI. Any Widget and Layout must assigned to self.containter, which is a pyqt Layout object
        """ 
        self.container = Qt.QVBoxLayout()

        hbox1 = Qt.QHBoxLayout()
        self.label_Device = Qt.QLabel("Device .xml file: ")
        self.edit_File_xml = Qt.QLineEdit()
        self.button_ChooseFile =Qt.QPushButton("Choose File")
        self.button_ConnectDevice =Qt.QPushButton("Connect")
        hbox1.addWidget(self.label_Device)
        hbox1.addWidget(self.edit_File_xml, stretch=1)
        hbox1.addWidget(self.button_ChooseFile)
        hbox1.addWidget(self.button_ConnectDevice)
        #hbox1.addStretch(1)

        hbox2 = Qt.QHBoxLayout()
        #self.button_ConnectDevice = Qt.QPushButton("Connect")
        self.label_Wavelength = Qt.QLabel("Wavelength (nm): ")
        self.edit_Wavelength = Qt.QLineEdit()
        self.edit_Wavelength.setAlignment(QtCore.Qt.AlignRight)
        #self.label_PositionUnits = Qt.QLabel(" deg")
        self.label_Move = Qt.QLabel("Change wavelength: ")
        self.button_MoveNegative = Qt.QPushButton("<")
        self.button_MoveNegative.setToolTip('')
        self.button_MoveNegative.setMaximumWidth(30)
        self.button_MovePositive = Qt.QPushButton(">")
        self.button_MovePositive.setToolTip('')
        self.button_MovePositive.setMaximumWidth(30)
        self.label_By  = Qt.QLabel("By ")
        self.edit_StepSize = Qt.QLineEdit()
        self.edit_StepSize.setToolTip('')
        for w in [self.label_Wavelength,self.edit_Wavelength,self.label_Move,self.button_MoveNegative,self.button_MovePositive,self.label_By,self.edit_StepSize]:
            hbox2.addWidget(w)
        
        self.ramp_groupbox = abstract_instrument_interface.ramp_gui(ramp_object=self.interface.ramp)
                
        for box in [hbox1,hbox2]:
            self.container.addLayout(box)  
        self.container.addWidget(self.ramp_groupbox)

        self.container.addStretch(1)
        
        self.widgets_disabled_when_doing_ramp = [self.label_Device,self.edit_File_xml,self.button_ChooseFile,self.button_ConnectDevice,
                                                 self.label_Wavelength,self.edit_Wavelength,  
                                                 self.label_Move,self.button_MoveNegative,self.button_MovePositive,self.label_By,self.edit_StepSize
                                                 ]

        #These widgets are enabled ONLY when interface is connected to a device
        self.widgets_enabled_when_connected = [self.label_Wavelength, self.edit_Wavelength,
                                               self.label_Move,self.button_MoveNegative,self.button_MovePositive,self.label_By,self.edit_StepSize,
                                               ]
        
        #These widgets are enabled ONLY when interface is NOT connected to a device   
        self.widgets_enabled_when_disconnected = [self.label_Device,self.edit_File_xml,self.button_ChooseFile]

        self.widgets_disabled_when_moving = [self.edit_Wavelength,self.edit_StepSize ,self.button_MoveNegative ,self.button_MovePositive ]

    def connect_widgets_events_to_functions(self):
        self.button_ChooseFile.clicked.connect(self.click_button_SelectFile)
        self.button_ConnectDevice.clicked.connect(self.click_button_connect_disconnect)
        self.edit_Wavelength.returnPressed.connect(self.press_enter_edit_Wavelength)
        self.button_MoveNegative.clicked.connect(lambda x:self.click_button_Move(-1))
        self.button_MovePositive.clicked.connect(lambda x:self.click_button_Move(+1))
        self.edit_StepSize.returnPressed.connect(self.press_enter_edit_StepSize)

###########################################################################################################
### Event Slots. They are normally triggered by signals from the model, and change the GUI accordingly  ###
###########################################################################################################

    def on_connection_status_change(self,status):
        if status == self.interface.SIG_DISCONNECTED:
            self.disable_widget(self.widgets_enabled_when_connected)
            self.enable_widget(self.widgets_enabled_when_disconnected)
            self.button_ConnectDevice.setText("Connect")
            self.label_Wavelength.setText((f"Wavelength (nm): "))
        if status == self.interface.SIG_DISCONNECTING:
            self.disable_widget(self.widgets_enabled_when_connected)
            self.enable_widget(self.widgets_enabled_when_disconnected)
            self.button_ConnectDevice.setText("Disconnecting...")
        if status == self.interface.SIG_CONNECTING:
            self.disable_widget(self.widgets_enabled_when_connected)
            self.enable_widget(self.widgets_enabled_when_disconnected)
            self.button_ConnectDevice.setText("Connecting...")
        if status == self.interface.SIG_CONNECTED:
            self.enable_widget(self.widgets_enabled_when_connected)
            self.disable_widget(self.widgets_enabled_when_disconnected)
            self.button_ConnectDevice.setText("Disconnect")
            self.label_Wavelength.setText((f"Wavelength (nm) [<b>{int(self.interface.min_max_wl[0])}-{int(self.interface.min_max_wl[1])}</b>]: "))
    
    def on_wavelength_change(self,wl):
        self.edit_Wavelength.setText(str(wl))

    def on_step_size_change(self,value):
        self.edit_StepSize.setText(f"{value:.4f}")

    def on_moving_state_change(self,status):
        if status == self.interface.SIG_MOVEMENT_STARTED:
            self.disable_widget(self.widgets_disabled_when_moving)
        if status == self.interface.SIG_MOVEMENT_ENDED and self.interface.ramp.is_not_doing_ramp(): #<-- ugly solution, it assumes that the ramp object exists:
            self.enable_widget(self.widgets_disabled_when_moving)

    def on_close(self):
        pass

#######################
### END Event Slots ###
#######################

###################################################################################################################################################
### GUI Events Functions. They are triggered by direct interaction with the GUI, and they call methods of the interface (i.e. the model) object.###
###################################################################################################################################################

    def click_button_SelectFile(self): 
        filename, _ = Qt.QFileDialog.getOpenFileName(self.parent, 
                        "Select a valid .xml file", "", ".xml files (*.xml)")
        if filename:
            self.edit_File_xml.setText(filename)
        return

    def click_button_refresh_list_devices(self):
        self.interface.refresh_list_devices()

    def click_button_connect_disconnect(self):
        if(self.interface.instrument.connected == False): # We attempt connection   
            self.interface.connect_device(self.edit_File_xml.text())
        elif(self.interface.instrument.connected == True): # We attempt disconnection
            self.interface.disconnect_device()
            
    def press_enter_edit_Wavelength(self):
        return self.interface.set_wavelength(self.edit_Wavelength.text())
    
    def press_enter_edit_StepSize(self):
        return self.interface.set_step_size(self.edit_StepSize.text())
     
    def click_button_Move(self,direction):
        self.press_enter_edit_StepSize()
        self.interface.move_single_step(direction)

############################################################
### END GUI Events Functions
############################################################

class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(__package__)
        # Set the central widget of the Window.
        # self.setCentralWidget(self.container)
    def closeEvent(self, event):
        #if self.child:
        pass#self.child.close()

def main():
    parser = argparse.ArgumentParser(description = "",epilog = "")
    parser.add_argument("-s", "--decrease_verbose", help="Decrease verbosity.", action="store_true")
    parser.add_argument('-virtual', help=f"Initialize the virtual driver", action="store_true")
    args = parser.parse_args()
    virtual = args.virtual
    
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    Interface = interface(app=app,virtual=virtual)
    Interface.verbose = not(args.decrease_verbose)
    app.aboutToQuit.connect(Interface.close) 
    view = gui(interface = Interface, parent=window) #In this case window is the parent of the gui
    
    window.show()
    app.exec()# Start the event loop.


if __name__ == '__main__':
    main()
