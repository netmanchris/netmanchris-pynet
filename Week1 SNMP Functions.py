
def gather_devices():
    global list_of_devices
    # Function to gather user input for a list of IP addresses and SNMP strings
    list_of_devices = []
    more = ('''Y''')
    while more == 'Y':
        #gathers user input to populate list_of_devices list of dictionies
        #loops until user answers 'N'
        device=input('''What is the IP address of the device you wish to work with?''')
        SNMP_String=input('''What is the SNMP read String for this device?''')
        device_dict = {'DeviceIP':device,'String':SNMP_String}
        list_of_devices.append(device_dict)
        more = input('''Do you wish to add more devices? Y/N''')
    else:
        return list_of_devices
        

def snmp_lab1(list):
    #takes the list generated from the gather_devices function and iterates over
    #the list using the SNMP String and IP address as inputs to gather the sysname 
    #and sysdesc over SNMP. Prints out the sysdesc and sysname for each item in the list
    for i in list:
        COMMUNITY_STRING = i['String']
        IP = i['DeviceIP']
        SNMP_PORT = 161
        a_device = (IP, COMMUNITY_STRING, SNMP_PORT)
        sysnameoid = ".1.3.6.1.2.1.1.5.0"
        sysdescoid = ".1.3.6.1.2.1.1.1.0"
        snmp_sysname = (snmp_get_oid(a_device, oid=sysnameoid))
        sysname = snmp_extract(snmp_sysname)
        snmp_sysdesc = (snmp_get_oid(a_device, oid=sysdescoid))
        sysdesc = snmp_extract(snmp_sysdesc)
        print (sysname + sysdesc + '\n\n\n\n')
        

                        
        
        
        



