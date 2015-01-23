#original located at https://github.com/ktbyers/pynet/blob/master/snmp/snmp_helper.py
#edited to work with Python 3.x

'''
Requires the pysnmp version4 library

Example usage:

>>> from snmp_helper import snmp_get_oid,snmp_extract
>>> 
>>> COMMUNITY_STRING = '<COMMUNITY>'
>>> SNMP_PORT = 161
>>> a_device = ('1.1.1.1', COMMUNITY_STRING, SNMP_PORT)

Use the MIB-2 sysDescr as a test
>>> snmp_data = snmp_get_oid(a_device, oid='.1.3.6.1.2.1.1.1.0', display_errors=True)
>>> snmp_data

[(MibVariable(ObjectName(1.3.6.1.2.1.1.1.0)), DisplayString(hexValue='436973636f20494f5320536f6674776172652c204338383020536f667477617265202843383830444154412d554e4956455253414c4b392d4d292c2056657273696f6e2031352e302831294d342c2052454c4541534520534f4654574152452028666331290d0a546563686e6963616c20537570706f72743a20687474703a2f2f7777772e636973636f2e636f6d2f74656368737570706f72740d0a436f707972696768742028632920313938362d3230313020627920436973636f2053797374656d732c20496e632e0d0a436f6d70696c6564204672692032392d4f63742d31302030303a30322062792070726f645f72656c5f7465616d'))]

>>> output = snmp_extract(snmp_data)
>>> print output
Cisco IOS Software, C880 Software (C880DATA-UNIVERSALK9-M), Version 15.0(1)M4, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2010 by Cisco Systems, Inc.
Compiled Fri 29-Oct-10 00:02 by prod_rel_team

'''

from pysnmp.entity.rfc3413.oneliner import cmdgen


def snmp_get_oid(a_device, oid='.1.3.6.1.2.1.1.1.0', display_errors=False):
    '''
    Retrieve the given OID

    Default OID is MIB2, sysDescr

    a_device is a tuple = (a_host, community_string, snmp_port)
    '''

    a_host, community_string, snmp_port = a_device
    snmp_target = (a_host, snmp_port)

    # Create a PYSNMP cmdgen object
    cmd_gen = cmdgen.CommandGenerator()

    (error_detected, error_status, error_index, snmp_data) = cmd_gen.getCmd(
        cmdgen.CommunityData(community_string),
        cmdgen.UdpTransportTarget(snmp_target),
        oid,
        lookupNames=True, lookupValues=True
    )

    if not error_detected:
        return snmp_data
    else:
        if display_errors:
            print ('ERROR DETECTED: ')
            print ('    %-16s %-60s' % ('error_message', error_detected))
            print ('    %-16s %-60s' % ('error_status', error_status))
            print ('    %-16s %-60s' % ('error_index', error_index))
        return None


def snmp_extract(snmp_data):
    '''
    Unwrap the SNMP response data and return in a readable format

    Assumes only a single list element is returned
    '''

    if len(snmp_data) > 1:
        raise ValueError("snmp_extract only allows a single element")

    if len(snmp_data) == 0:
        return None
    else:
        # Unwrap the data which is returned as a tuple wrapped in a list
        return snmp_data[0][1].prettyPrint()





def gather_devices():
    ''' Gathers user input of IP_ADDRESS and SNMP_STRING and appends them as a dictionary
    into the DEV_LIST list.'''
    global DEV_LIST

    #initializes function variables
    DEV_LIST = []
    more = ('''Y''')
    
    while more == "Y" or more == "y":
        '''gathers user input to populate list_of_devices list of dictionies
        loops until user answers 'N''''
        IP_ADDRESS=input('''What is the IP address of the device you wish to connect to : ''')
        SNMP_STRING=input('''What is the SNMP read String for this device?: ''')

        #creates dictionary DEV_DICT from IP_ADDRESS and SNMP_STRING VARs.
        DEV_DICT = {'DeviceIP':IP_ADDRESS,'String':SNMP_STRING}

        #appends DEV_DICT
        DEV_LIST.append(DEV_DICT)
        more = input('''Do you wish to add more devices? Y/N: ''')
    else:
        return DEV_LIST
      

def lab3(get_snmp_info=None):
    '''Takes the list generated from the gather_devices function and iterates over
    the list using the SNMP String and IP address as inputs to gather the sysname 
    and sysdesc over SNMP. Prints out the sysdesc and sysname for each item in the list'''


    #sets get_snmp_info to global DEV_LIST generated from gather_devices() function
    if get_snmp_info == None:
        get_snmp_info = DEV_LIST

        
    print("\n------------------------------------------------------------------------------------------\n\n")

    #Function 
    for DEVICE in DEV_LIST:
        #sets function variables
         IP_ADDRESS = DEVICE['DeviceIP']
        COMMUNITY_STRING = DEVICE['String']
        SNMP_PORT = 161

        #creates a combined variable from 
        a_device = (IP, COMMUNITY_STRING, SNMP_PORT)

        #This section sets the SNMP SYSOIDS we are going to use 
        SYSNAME_OID = ".1.3.6.1.2.1.1.5.0"
        SYSDESC_OID = ".1.3.6.1.2.1.1.1.0"
        snmp_sysname = (snmp_get_oid(a_device, oid=SYSNAME_OID))
        SYSNAME = snmp_extract(snmp_sysname)
        snmp_sysdesc = (snmp_get_oid(a_device, oid=SYSDESC_OID))
        SYSDESC = snmp_extract(snmp_sysdesc)

        if "Cisco" in SYSDESC:
            # Uptime when running config last changed    
            ccmHistoryRunningLastChangedoid = '1.3.6.1.4.1.9.9.43.1.1.1.0'   
            # Uptime when running config last saved (note any 'write' constitutes a save)
            ccmHistoryRunningLastSavedoid = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
            # Uptime when startup config last saved   
            ccmHistoryStartupLastChangedoid = '1.3.6.1.4.1.9.9.43.1.1.3.0'
            snmpRunChange = (snmp_get_oid(a_device, oid=ccmHistoryRunningLastChangedoid))
            RunChange = snmp_extract(snmpRunChange)
            snmpStartChange = (snmp_get_oid(a_device, oid=ccmHistoryRunningLastSavedoid))
            StartChange = snmp_extract(snmpStartChange)
            snmpRunSave = (snmp_get_oid(a_device, oid=ccmHistoryStartupLastChangedoid))
            RunSave = snmp_extract(snmpRunSave)
            #print (str(snmpRunSave) + ("\n\n\n\n\n"))
            if RunSave == '0':
                print("This device has not been saved since the last reboot")
            print (sysname +"\n"+ sysdesc +"\n\n")
            if RunSave == '0':
                print("This device has NOT been saved since the last reboot")
                print ("\n Running Config Last Saved at:" + str(RunSave)+"\n")
            print("\n------------------------------------------------------------------------------------------\n\n")
        else:
            print (sysname + sysdesc + '\n\n\n')
            print("\n------------------------------------------------------------------------------------------\n\n")
        
        




        
        
        



