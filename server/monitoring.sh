#! /bin/bash

# nmcli device status | grep wlan0
# nmcli device status | grep wlan1

# sudo iw dev wlan1 station dump


check_device_status(){
     # check the status of the device from the network manager perspective
    if nmcli device status | grep $1 | grep -Pq '\bconnected'; then
        echo "$1 connected"
        return 0
    else
        if nmcli device status | grep $1 | grep -Pq '\bconnecting'; then
            echo "$1 is connecting"
            logger -t net_monit "$1 is connecting"
            return 0
        else
            echo "$1 not connected"
            logger -t net_monit "$1 not connected"
            return 1
        fi
    fi
}

check_hotspot(){
    if check_device_status "wlan1"; then 
        echo "hotspot (wlan1) running"
        return 0
    else
        echo "hotspot (wlan1) NOT running"
        return 1
    fi
}

check_internet(){

    if ! check_device_status "wlan0"; then
        return 1
    fi

    if ping -I wlan0 google.com -c 1 -W 1 -q > /dev/null 2>&1; then
        echo 'ping to google succesfull'
        logger -t net_monit 'ping to google succesfull'
        return 0
    else
        echo 'failed to ping google'
        logger -t net_monit 'failed to ping google'
        return 1
    fi
}

check_received_data(){
    return journalctl --since -10min --boot -t iSpindleServer | grep "name" -q
}

repair_internet_connection(){
    sudo systemctl stop NetworkManager
    sudo ip link set wlan0 down
    sudo ip addr flush dev wlan0
    sudo ip link set wlan0 up
    sudo systemctl start NetworkManager
    sudo systemctl restart iSpindleServer.service

    logger -t net_monit 'Internet connection (wlan0) and Network Manager restarted'
}

repair_hotspot()
{
    sudo systemctl stop NetworkManager
    sudo ip link set wlan0 down
    sudo ip link set wlan1 down
    sudo ip addr flush dev wlan0
    sudo ip addr flush dev wlan1
    sudo /sbin/modprobe -r rt73usb
    sudo /sbin/modprobe rt73usb
    sudo ip link set wlan0 up
    sudo ip link set wlan1 up
    sudo systemctl start NetworkManager
    sudo systemctl restart iSpindleServer.service

    logger -t net_monit 'hotspot (wlan1) and Network Manager restarted'
}

# if hotspot not working reboot
if ! check_hotspot; then
    #repair_hotspot
    sudo reboot
fi

# if no internet connection, try to repair it
if ! check_internet; then
    repair_internet_connection
    exit
fi

# if no data since 10 min, restart server
if ! check_received_data: then
    sudo systemctl restart iSpindleServer.service
fi




# journalctl --since -30min --boot -t net_monit -t iSpindleServer