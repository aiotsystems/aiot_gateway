#!/usr/bin/python

#============================ adjust path =====================================
from __future__ import print_function
import sys
import os
if __name__ == "__main__":
    here = sys.path[0]
    sys.path.insert(0, os.path.join(here, '..', '..','libs'))
    sys.path.insert(0, os.path.join(here, '..', '..','external_libs'))

#============================ imports =========================================

# built-in
import os
import copy
import time
import random
import threading
import traceback
import argparse
import json
import pprint
import socket
# requirements
import bottle
# SmartMeshSDK
from SmartMeshSDK            import sdk_version
from SmartMeshSDK.utils      import JsonManager
# DustCli
from dustCli                 import DustCli

#============================ define ==========================================

DFLT_SERIALPORT = 'COM40'
DFLT_TCPPORT    = 8081

MOTES = [
    # showroom
    {'name': 'big_data_mote',      'macAddress': None},
    {'name': 'reseau_mote',        'macAddress': None},
    {'name': 'apprentissage_mote', 'macAddress': None},
    {'name': 'robotique_mote',     'macAddress': None},
    {'name': 'information_mote',   'macAddress': None},
    {'name': 'language_mote',      'macAddress': None},
    {'name': 'algorithme_mote',    'macAddress': '00-17-0d-00-00-68-0a-ab'},
    {'name': 'xplore_mote',        'macAddress': None},
    {'name': 'machine_mote',       'macAddress': None},
    # expo
    {'name': 'expo_mote1',         'macAddress': None},
    {'name': 'expo_mote2',         'macAddress': None},
    {'name': 'expo_mote3',         'macAddress': None},
    {'name': 'expo_mote4',         'macAddress': None},
    {'name': 'expo_mote5',         'macAddress': None},
    # hall
    {'name': 'hall_mote1',         'macAddress': None},
    {'name': 'hall_mote2',         'macAddress': None},
    {'name': 'hall_mote3',         'macAddress': None},
    {'name': 'hall_mote4',         'macAddress': None},
    {'name': 'hall_mote5',         'macAddress': None},
    {'name': 'hall_mote6',         'macAddress': None},
]
MOTENAMES = [m['name'] for m in MOTES]
mote_macAddress2name = {}
for m in MOTES:
    mote_macAddress2name[m['macAddress']] = m['name']

MSGID_CMD_LOWPOWER = 0x01
MSGID_CMD_ACTIVE   = 0x02
MSGID_CMD_MUSIC    = 0x03
MSGID_NOTIF_US     = 0x04

#============================ helpers =========================================

def formatVersion():
    return 'SmartMesh SDK {0}'.format('.'.join([str(v) for v in sdk_version.VERSION]))

def currentUtcTime():
    return time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime())

def logError(err):
    output  = []
    output += ["============================================================="]
    output += [currentUtcTime()]
    output += [""]
    output += ["ERROR!"]
    output += [""]
    output += ["=== exception type ==="]
    output += [str(type(err))]
    output += [""]
    output += ["=== traceback ==="]
    output += [traceback.format_exc()]
    output  = '\n'.join(output)
    print (output)

pp = pprint.PrettyPrinter(indent=4)

#============================ classes =========================================

class AppData(object):
    '''
    {
        'motes': {
            'name1': {
                'fill':   'blue',
                'stroke': 'red',
            },
            ...
        },
    }
    '''
    
    # singleton pattern
    _instance   = None
    _init       = False
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppData, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        
        # singleton patterm
        if self._init:
            return
        self._init = True
        
        # local variables
        self.dataLock             = threading.RLock()
        self.data                 = {}
        self.data['motes'] = {}
        for motename in MOTENAMES:
            self.data['motes'][motename] = {
                'fill':   'blue',
                'stroke': 'black',
            }
    
    #======================== public ==========================================
    
    def notifData(self,motename,fill):
        with self.dataLock:
            self.data['motes'][motename]['fill']=fill
            if self.data['motes'][motename]['stroke']=='yellow':
                self.data['motes'][motename]['stroke'] = 'blue'
            else:
                self.data['motes'][motename]['stroke'] = 'yellow'
    
    def get_motes(self):
        with self.dataLock:
            return copy.deepcopy(self.data['motes'])

class DataGatherer(threading.Thread):
    
    SNAPSHOT_PERIOD_S             = 10
    
    def __init__(self,serialport):
        
        # store params
        self.serialport           = serialport
        
        # local variables
        self.delaySnapshot        = 1 # wait for banners before first snapshot
        self.goOn                 = True
        
        # start thread
        threading.Thread.__init__(self)
        self.name = 'DataGatherer'
        self.start()
        
        # instantiate JsonManager
        self.jsonManager          = JsonManager.JsonManager(
            autoaddmgr            = False,
            autodeletemgr         = False,
            serialport            = self.serialport,
            configfilename        = None,
            notifCb               = self._notif_cb,
        )
    
    def run(self):
        while self.goOn:
            try:
                if self.delaySnapshot==0:
                    self._triggerSnapshot()
                    self.delaySnapshot = self.SNAPSHOT_PERIOD_S
                self.delaySnapshot -= 1
                time.sleep(1)
            except Exception as err:
                logError(err)
    
    #======================== public ==========================================
    
    def snapshotNow(self):
        self.delaySnapshot = 0
    
    def close(self):
        self.goOn = False
    
    #======================== private =========================================
    
    # === abstract methods
    
    def getStatus(self):
        returnVal = self.jsonManager.status_GET()
        return returnVal
    
    def _triggerSnapshot(self):
        # step 1. get list of managers
        r = self.jsonManager.status_GET()
        managers = [k for (k,v) in list(r['managers'].items()) if v=='connected']
        assert(len(managers)in [0,1])
        # step 2. trigger snapshot for each
        for m in managers:
            self.jsonManager.snapshot_POST(
                manager = m,
            )
    
    # === private
    
    # notifications from networks
    
    def _notif_cb(self,notifName,notifJson):
        if notifName=='notifData':
            self._device_notifData_cb(notifJson)
        else:
            pass # silently drop notification I don't need
    
    def _device_notifData_cb(self,data):
        '''
        {
            'manager': 'COM40',
            'name': 'notifData',
            'fields': {
                'utcSecs':    1025683841,
                'utcUsecs':   562500,
                'macAddress': '00-17-0d-00-00-68-0a-ab',
                'srcPort':    61624,
                'dstPort':    61624,
                'data':       [0],
            },
        }
        '''
        moteName = mote_macAddress2name[data['fields']['macAddress']]
        if data['fields']['data']==[0x00]:
            fill = 'red'
        else:
            fill = 'green'
        AppData().notifData(moteName,fill)
    
    # deleters
    
    def _deleteMotes(self,manager):
        motes = AppData().get('motes')
        numberOfMotesDeleted = 0
        
        # loop through motes
        while True:
            found = False
            for idx in range(len(motes)):
                if  motes[idx]['manager']== manager:
                    found = True
                    motes.pop(idx)
                    numberOfMotesDeleted += 1
                    break
            if not found:
                break
        
        AppData().set('motes',motes)
    
    def _deletePaths(self,moteA=None,moteB=None,manager=None,exceptManager=None):
    
        paths = AppData().get('paths')
        numberOfPathsDeleted = 0
        
        # loop through paths
        while True:
            found = False
            for idx in range(len(paths)):
                
                if   (moteA==None and moteB==None and manager!=None and exceptManager==None):
                    '''
                    delete all paths from for manager 'manager'
                    '''
                    condition = (
                        paths[idx]['manager']         == manager
                    )
                elif (moteA!=None and moteB==None and manager!=None and exceptManager==None):
                    '''
                    delete all paths which have moteA as either 'source' or 'dest'
                    for manager 'manager'
                    '''
                    condition = (
                        paths[idx]['manager']         == manager
                        and
                        (
                            paths[idx]['source']      == moteA
                            or
                            paths[idx]['dest']        == moteA
                        )
                    )
                elif (moteA!=None and moteB==None and manager==None and exceptManager!=None):
                    '''
                    delete all paths which have moteA as either 'source' or 'dest'
                    except for manager 'exceptManager'
                    '''
                    condition = (
                        paths[idx]['manager']         != exceptManager
                        and
                        (
                            paths[idx]['source']      == moteA
                            or
                            paths[idx]['dest']        == moteA
                        )
                    )
                elif (moteA!=None and moteB!=None and manager!=None and exceptManager==None):
                    '''
                    delete all moteA->moteB or moteB->moteA paths
                    for manager 'manager'
                    '''
                    condition = (
                        paths[idx]['manager']         == manager
                        and
                        (
                            (
                                paths[idx]['source']  == moteA
                                and
                                paths[idx]['dest']    == moteB
                            )
                            or
                            (
                                paths[idx]['source']  == moteB
                                and
                                paths[idx]['dest']    == moteA
                            )
                        )
                    )
                else:
                    raise SystemError()
                
                if condition:
                    found = True
                    paths.pop(idx)
                    numberOfPathsDeleted += 1
                    break
            if not found:
                break
        
        AppData().set('paths',paths)

class WebServer(object):
    
    def __init__(self,dataGatherer):
        
        # store params
        self.dataGatherer         = dataGatherer
        
        # web server
        self.websrv   = bottle.Bottle()
        # admin
        self.websrv.route('/',                        'GET',    self._webhandle_root_GET)
        self.websrv.route('/static/<path:path>',      'GET',    self._webhandle_static_GET)
        # museum
        self.websrv.route('/museum',                  'GET',    self._webhandle_museum_GET)
        self.websrv.route('/museum.json',             'GET',    self._webhandle_museumjson_GET)
        self.websrv.route('/museum',                  'POST',   self._webhandle_museum_POST)
        
        # start web interface
        webthread = threading.Thread(
            target = self._bottle_try_running_forever,
            args   = (self.websrv.run,),
            kwargs = {
                'host'          : '0.0.0.0',
                'port'          : DFLT_TCPPORT,
                'quiet'         : True,
                'debug'         : False,
            }
        )
        webthread.name   = 'WebServer'
        webthread.daemon = True
        webthread.start()
    
    #======================== public ==========================================
    
    def close(self):
        pass # nothing to do, thread is daemonic
    
    #======================== admin ===========================================
    
    def _bottle_try_running_forever(self,*args,**kwargs):
        RETRY_PERIOD = 3
        while True:
            try:
                args[0](**kwargs) # blocking
            except socket.error as err:
                if err[0]==10013:
                    print ('FATAL: cannot open TCP port {0}.'.format(kwargs['port']))
                    print ('    Is another application running on that port?')
                else:
                    print (logError(err))
            except Exception as err:
                print (logError(err))
            print ('    Trying again in {0} seconds'.format(RETRY_PERIOD), end=' ')
            for _ in range(RETRY_PERIOD):
                time.sleep(1)
                print ('.', end=' ')
            print ('')
    
    #======================== webhandlers =====================================
    
    # admin
    
    def _webhandle_root_GET(self):
        bottle.redirect("/museum")
    
    def _webhandle_static_GET(self,path):
        return bottle.static_file(
            path,
            root='static',
        )
    
    # museum
    
    def _webhandle_museum_GET(self):
        return bottle.template(
            "museum",
            pagetitle   = 'InriaMuseum',
        )
    
    def _webhandle_museumjson_GET(self):
        '''
        This function needs to create
        
        {
            'motes': {
                'name1': {
                    'fill':   'blue',
                    'stroke': 'red',
                }
        }
        '''
        
        returnVal = {}
        
        #=== motes
        returnVal['motes'] = AppData().get_motes()
        
        return returnVal
    
    def _webhandle_museum_POST(self):
        body = bottle.request.body.read()
        print(body)
        
        data = None
        if   body==b'button_lowpower':
            data = [MSGID_CMD_LOWPOWER]
        elif body==b'button_active':
            data = [MSGID_CMD_ACTIVE]
        elif body==b'button_music1':
            data = [MSGID_CMD_MUSIC]
        elif body==b'button_music2':
            pass
        
        if data:
            for _ in range(4):
                self.dataGatherer.jsonManager.raw_POST(
                    commandArray = ['sendData'],
                    fields       = {
                        'macAddress': [0xff]*8,
                        'priority':   0,
                        'srcPort':    0xf0b8,
                        'dstPort':    0xf0b8,
                        'options':    0,
                        'data':       data,
                    },
                    manager      = 0
                )
    
    #======================== private =========================================

class InriaMuseum(object):
    
    def __init__(self,serialport):
        
        # store params
        self.serialport           = serialport
        
        # DataGatherer
        self.dataGatherer         = DataGatherer(serialport=self.serialport)
        
        # interfaces
        self.webServer            = WebServer(
            dataGatherer          = self.dataGatherer,
        )
        self.cli                  = DustCli.DustCli(
            quit_cb  = self._clihandle_quit,
            versions = {
                'SmartMesh SDK': sdk_version.VERSION,
            },
        )
        self.cli.registerCommand(
            name                  = 'status',
            alias                 = 's',
            description           = 'get the current status',
            params                = [],
            callback              = self._clihandle_status,
        )
        print (f'Web interface started at http://127.0.0.1:{DFLT_TCPPORT}')
        
        # this is the main thread, we don't want it to die
        while True:
            time.sleep(1)
            if self.cli.is_alive()==False:
                break
    
    #========================  CLI handlers ===================================
    
    def _clihandle_quit(self):
        
        self.dataGatherer.close()
        self.webServer.close()
        
        time.sleep(.3)
        print ("bye bye.")
    
    def _clihandle_status(self,params):
        pp.pprint(self.dataGatherer.getStatus())

#============================ main =======================================

def main(args):
    InriaMuseum(**args)

if __name__=="__main__":
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--serialport',        default=DFLT_SERIALPORT)
    args = vars(parser.parse_args())
    main(args)
