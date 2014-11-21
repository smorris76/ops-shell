#!/opt/gums/bin/python2.7

import cmd, string, sys, argparse
from pysnmp.entity.rfc3413.oneliner import cmdgen

# set command line options
parser = argparse.ArgumentParser()
parser.add_argument("-c", help="SNMP community for device (Default public)")
parser.add_argument("host", help="OPS to connect to")

args = parser.parse_args()

# hardcoded values, these need to change to be read from the CLI
if args.c:
	myComm = args.c
else:
	myComm = 'public'

myHost = args.host

# MIB values
opsFwVer     = '1.3.6.1.4.1.28318.2.1.2.0'   # Firmware Version
opsModSn     = '1.3.6.1.4.1.28318.2.1.3.0'   # Module Serial Number
opsSwMode    = '1.3.6.1.4.1.28318.2.1.4.0'   # Switching Mode
opsActPath   = '1.3.6.1.4.1.28318.2.1.5.0'   # Active Path
opsRevDelay  = '1.3.6.1.4.1.28318.2.1.6.0'   # Reversion Delay
opsSwDelay   = '1.3.6.1.4.1.28318.2.1.7.0'   # Switching Delay
opsLineTxPwr = '1.3.6.1.4.1.28318.2.1.11.0'  # Line TX Power
opsPriTxPwr  = '1.3.6.1.4.1.28318.2.1.12.0'  # Primary TX Power
opsSecTxPwr  = '1.3.6.1.4.1.28318.2.1.13.0'  # Secondary TX Power
opsLineRxPwr = '1.3.6.1.4.1.28318.2.1.14.0'  # Line RX Power
opsPriRxPwr  = '1.3.6.1.4.1.28318.2.1.15.0'  # Primary RX Power
opsSecRxPwr  = '1.3.6.1.4.1.28318.2.1.16.0'  # Secondary RX Power
opsLineAlarm = '1.3.6.1.4.1.28318.2.1.24.0'  # Line RX Alarm Threshold
opsPriAlarm  = '1.3.6.1.4.1.28318.2.1.25.0'  # Primary RX Alarm Threshold
opsSecAlarm  = '1.3.6.1.4.1.28318.2.1.26.0'  # Secondary RX Alarm Threshold
opsPriSwDb   = '1.3.6.1.4.1.28318.2.1.27.0'  # Primary Switch Threshold
opsSecSwDb   = '1.3.6.1.4.1.28318.2.1.28.0'  # Secondary Switch Threshold
opsMainSn    = '1.3.6.1.4.1.28318.2.20.3.0'  # MainBoardSerial Number
opsControl   = '1.3.6.1.4.1.28318.2.20.4.0'  # Local or Remote Control

def opsStatus(opsComm, opsHost):
    opsCmd = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, opsResults = opsCmd.getCmd(
        cmdgen.CommunityData(myComm, mpModel=0),
        cmdgen.UdpTransportTarget((myHost, 161)),
        opsFwVer,     # Index 0
        opsModSn,     # Index 1
        opsSwMode,    # Index 2
        opsActPath,   # Index 3
        opsRevDelay,  # Index 4
        opsSwDelay,   # Index 5
        opsLineTxPwr, # Index 6
        opsPriTxPwr,  # Index 7
        opsSecTxPwr,  # Index 8
        opsLineRxPwr, # Index 9
        opsPriRxPwr,  # Index 10
        opsSecRxPwr,  # Index 11
        opsLineAlarm, # Index 12
        opsPriAlarm,  # Index 13
        opsSecAlarm,  # Index 14
        opsPriSwDb,   # Index 15
        opsSecSwDb,   # Index 16
        opsMainSn,    # Index 17
        opsControl    # Index 18
    )
    myFwVer = opsResults[0][1]
    myModSn = str(int(str(opsResults[1][1]), 16))
    if opsResults[2][1] == '0x30':
        mySwMode = 'Auto-switch (Non-Reverting)'
    elif opsResults[2][1] == '0x40':
        mySwMode = 'Auto-switch (Reverting)'
    elif opsResults[2][1] == '0x50':
        mySwMode = 'Manual'
    else:
        mySwMode = 'Unknown'
    if opsResults[3][1] == 'pri':
        myActPath = 'Primary'
    elif opsResults[3][1] == 'sec':
        myActPath = 'Secondary'
    else:
        myActPath = 'Unknown'
    myRevDelay = opsResults[4][1]
    mySwDelay = opsResults[5][1]
    myLineTxPwr = opsResults[6][1]
    myPriTxPwr = opsResults[7][1]
    mySecTxPwr = opsResults[8][1]
    myLineRxPwr = opsResults[9][1]
    myPriRxPwr = opsResults[10][1]
    mySecRxPwr = opsResults[11][1]
    myLineAlarm = opsResults[12][1]
    myPriAlarm = opsResults[13][1]
    mySecAlarm = opsResults[14][1]
    myPriSwDb = opsResults[15][1]
    mySecSwDb = opsResults[16][1]
    myMainSn = str(int(str(opsResults[17][1]), 16))
    myControl = opsResults[18][1]

    # Check for errors
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and opsResults[int(errorIndex)-1] or '?'
           )
        )
    else:
        print "# System Information #"
        print "System Serial Number:       " + myMainSn
        print "Module Serial Number:       " + myModSn
        print "Firmware Version:           " + myFwVer
        print "System Control:             " + myControl
        print
        print "# Configuration #"
        print "Switching Mode:             " + mySwMode
        print "Switch Delay:               " + mySwDelay
        print "Reversion Delay:            " + myRevDelay
        print "Primary Switch Threshold:   " + myPriSwDb + "dB"
        print "Secondary Switch Threshold: " + mySecSwDb + "dB"
        print "Line Alarm Threshold:       " + myLineAlarm + "dB"
        print "Primary Alarm Threshold:    " + myPriAlarm + "dB"
        print "Secondary Alarm Threshold:  " + mySecAlarm + "dB"
        print
        print "# Optical Status #"
        print "Active Path:                " + myActPath
        print "Line Tx Power:              " + myLineTxPwr + "db"
        print "Line RxPower:               " + myLineRxPwr + "db"
        print "Primary Tx Power:           " + myPriTxPwr + "db"
        print "Primary Rx Power:           " + myPriRxPwr + "db"
        print "Secondary Tx Power:         " + mySecTxPwr + "db"
        print "Secondary Rx Power:         " + mySecRxPwr + "db"

class ops_shell(cmd.Cmd):

    def emptyline(self):
        pass

    def help_set(self):
        print "Sets parameters on OPS"
        print
        print "Possible arugments:"
        print " active-path (primary|secondary)"
        print " switch-mode (revert|no-revert|manual)"
        print " switch-delay <seconds>"
        print " revert-delay <seconds>"
        print " primary-switch <dB>"
        print " secondary-switch <dB>"
        print " primary-alarm <dB>"

    def do_set(self, line):
        ''' set writeable paramters on OPS
            Possible arguments:
                active-path (primary|secondary)'''
        commands = line.split()
        if len(commands) < 2:
            print "Insufficient arguments to set"
            return
        print commands

    def do_status(self, line):
        opsStatus(myComm, myHost)

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        return True

my_shell = ops_shell()
my_shell.prompt = myComm + "@" + myHost + "> "
my_shell.cmdloop()
