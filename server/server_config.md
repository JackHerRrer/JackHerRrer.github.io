# Raspberry pi configuration

## Wifi configuration

https://raspberrytips.com/access-point-setup-raspberry-pi/

### Set the access point
```bash
# Add a wifi hotspot with SSID "LaCave"
sudo nmcli con add con-name hotspot_cave ifname wlan0 type wifi ssid "LaCave"
# Configure it to use wpa-psk
sudo nmcli con modify hotspot_cave wifi-sec.key-mgmt wpa-psk
# Set the password
sudo nmcli con modify hotspot_cave wifi-sec.psk "raspberry"
sudo nmcli con modify hotspot_cave 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
# Hide the SSID
sudo nmcli con modify hotspot_cave wifi.hidden on
```

### share internet between eth0 and wlan0
```bash
sudo nano /etc/sysctl.conf
```
uncomment : #net.ipv4.ip_forward=1


### Set firewall
```bash
sudo apt install iptables iptables-persistent
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

### "graphic" configuration 
Availabe once base configuration is done
```bash
sudo nmtui
```



## Server installation

python3-pip