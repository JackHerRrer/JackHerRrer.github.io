# Network configuration of the raspberry pi
On a Raspberrypi 2 with Raspbian Bookworm
[network tuto](https://raspberrytips.com/access-point-setup-raspberry-pi/)

## Set the access point
Create a hidden hotspot named `hotspot_cave`

```bash
sudo nmcli con add con-name hotspot ifname wlan0 type wifi ssid "hotspot_cave"
sudo nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify hotspot wifi-sec.psk "raspberry"
sudo nmcli con modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
sudo nmcli con modify hotspot wifi.hidden on
```

## share internet between eth0 and wlan0
Edit `/etc/sysctl.conf`
```bash
sudo nano /etc/sysctl.conf
```
and uncomment : `#net.ipv4.ip_forward=1`

## Set firewall
```bash
sudo apt install iptables iptables-persistent
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```
## "graphic" configuration 
available once base configuration is done
```
sudo nmtui
```