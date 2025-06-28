#! /bin/bash

PATH="$PATH:/sbin/"


echo 'hello' | systemd-cat -t monitoring
