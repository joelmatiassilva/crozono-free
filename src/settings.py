"""
Global variables and default config values, all set in one place.
Just import the module somewhere and use it's values.

Values set to None are meant to be overriden. Careful with those.
Backtracking who modifies those can be a pain.
"""

#TIME TO WAIT BEFORE STARTING
DELAY = 0

# Interface to be used across functions.
# Meant to be set only once.
INTERFACE = None
INTERFACE_MON = None
NEW_MAC = None

# Paths
OS_PATH = ''
LOG_FILE = OS_PATH + '/log_temp'

# WiFi Target
TARGET_ESSID = None
TARGET_KEY = None
TARGET_BSSID = None
TARGET_CHANNEL = None
TARGET_PRIVACY = None

# LAN Target
IP_LAN = None
LAN_RANGE = None

# WiFi Attacks Timings
AIRODUMP_SCAN_TIME = 45
WEP_AIREPLAY_TIME = 300
WPA_EXPECT_HANDSHAKE_TIME = 80
WASH_SCAN_TIME = 30
REAVER_TIMEOUT = 60

# Attacker
IP_ATTACKER = None
PORT_ATTACKER = 1337

# LAN Discovery & Attacks
LAN_DISCOVERY = None
ATTACK = None
GATEWAY = None
TARGET_MITM = None
EVILGRADE_ATTACK_TIME = 300
