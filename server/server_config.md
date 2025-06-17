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
uncomment: `#net.ipv4.ip_forward=1`


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

```bash
sudo apt install python3-venv
sudo python3 -m venv /opt/venv/

sudo chown -R pi /opt/venv/
export PATH=/opt/venv/bin:$PATH
pip install --upgrade pip wheel
pip install -r requirements.txt
```

## Simple connection to raspberry

1. On, the host machine, add the host to `~/.ssh/config`
```
Host cave
    Hostname raspberrypi.local
    User pi

```
2. Copy your ssh pub key on the raspberry
```bash
# On the host machine
ssh-copy-id cave

```