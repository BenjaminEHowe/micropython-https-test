import gc
import network
import ntptime
import sys
import time
import ubinascii

# the below files must be saved on the microcontroller
import config


def connect_wifi(wifi):
    wifi.active(True)
    networks = wifi.scan()
    networks.sort(key=lambda x:x[3], reverse=True) # sorted on signal strength / RSSI
    found_network = None
    for seen_network in networks:
        for configured_network in config.NETWORKS:
            if seen_network[0].decode() == configured_network[0]:
                print("Found network", configured_network[0])
                found_network = configured_network
                break
        if found_network:
            break
    if not found_network:
        raise RuntimeError("WiFi: unable to find a configured network")
    wifi.connect(found_network[0], found_network[1])
    max_wait_seconds = 10
    while max_wait_seconds > 0:
        status = wifi.status()
        if status == network.STAT_GOT_IP:
            ip = wifi.ifconfig()[0]
            return {"SSID": found_network[0], "IP": ip}
        if status == network.STAT_WRONG_PASSWORD:
            raise RuntimeError("WiFi: PSK appears incorrect")
        if status == network.STAT_NO_AP_FOUND:
            raise RuntimeError("WiFi: access point not found")
        if status == network.STAT_CONNECT_FAIL:
            raise RuntimeError("WiFi: failed to connect")
        max_wait_seconds -= 1
        print("WiFi: connecting...")
        time.sleep(1)
    raise RuntimeError("WiFi: connect timed out")


def get_mac_address(wifi):
    mac = ubinascii.hexlify(wifi.config('mac')).decode().upper()
    formatted_mac = ""
    for i in range(0, len(mac), 2):
        if (i == len(mac) - 2):
            formatted_mac = formatted_mac + mac[i] + mac[i+1]
        else:
            formatted_mac = formatted_mac + mac[i] + mac[i+1] + ":"
    return formatted_mac


def ms_to_dhms(ms):
    formatted_str = ""
    days = 0
    hours = 0
    minutes = 0
    seconds = ms // 1000
    if seconds > 60:
        minutes = seconds // 60
        seconds = seconds % 60
    if minutes > 60:
        hours = minutes // 60
        minutes = minutes % 60
    if hours > 24:
        days = hours // 24
        hours = hours % 24
    if days:
        formatted_str += "{}d ".format(days)
    if hours:
        formatted_str += "{}h ".format(hours)
    if minutes:
        formatted_str += "{}m ".format(minutes)
    formatted_str += "{}s ".format(seconds)
    return formatted_str[:-1]


def setup_board():
    global network
    print("{} running {} {}, conforms to Python {}".format(
        sys.implementation._machine,
        sys.implementation.name,
        ".".join(str(i) for i in sys.implementation.version),
        ".".join(str(i) for i in sys.version_info)
    ))
    wifi = network.WLAN(network.STA_IF)
    print("My MAC address is {}".format(get_mac_address(wifi)))
    network = connect_wifi(wifi)
    print("My IP address is {}".format(network["IP"]))
    ntptime.host = "time.cloudflare.com"
    ntptime.settime()
    print("The time is {}".format(ts_to_iso8601(time.time())))


def ts_to_iso8601(ts):
    localtime = time.gmtime(ts)
    year = localtime[0]
    month = localtime[1]
    day = localtime[2]
    hour = localtime[3]
    minute = localtime[4]
    second = localtime[5]
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)    
