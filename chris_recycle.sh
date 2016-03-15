honeypots=( ["101"]="89" ["102"]="94" ["103"]="117")

if [[ $2 != 'now' ]]
then
    #echo $2
    sleep $2
fi
kill $(ps ax | grep "root/$1/var/log" | awk '{$1=$1};1' |  cut -d ' ' -f1)
#kill $(ps ax | grep 'root/101/var/log' | cut -d ' ' -f1)
folder=$(date "+%m.%d.%y")
fol=$(date "+%H:%M:%S")
mkdir -p /data/$1/$folder
mkdir -p /data/$1/$folder/$fol
mkdir -p /data/$1/$folder/$fol/logs
cp -r /vz/root/$1/etc/honssh-master/sessions/ /data/$1/$folder/$fol
cp -r /vz/root/$1/etc/honssh-master/logs/ /data/$1/$folder/$fol
cp /data/$1/tmp/* /data/$1/$folder/$fol/logs
rm -f /data/$1/tmp/*

vzctl stop $1
vzctl destroy $1

vzrestore /vz/dump/vzdump-openvz-101-2016_03_13-20_19_41.tar $1

vzctl set $1 --netif_add eth0,,,,vzbr0 --save

vzctl start $1

sleep 1
#vzctl set 102 --netif_add eth0,,veth102.0,,br0
#sudo vzctl set $1 --netif_add eth0 --save
sudo vzctl exec $1 ifconfig eth0 128.8.238.${honeypots[$1]} netmask 255.255.255.192
sudo vzctl exec $1 route add default gw 128.8.238.65
sudo vzctl set $1 --nameserver 128.8.238.65
brctl addif br0 veth$1.0

vzctl set $1 --hostname records

sleep 15

vzctl exec $1 ping 8.8.8.8 -c 5

#echo 'touch /tmp/tmp' >> /vz/root/101/root/.bashrc
vzctl exec $1 "cd /etc/honssh-master ; /etc/honssh-master/honsshctrl.sh start" &> /dev/null &
vzctl exec $1 rm -f /tmp/*
file=$(date "+%s")

touch /data/$1/tmp/$file.log
cat /root/bash.bashrc > /vz/root/$1/etc/bash.bashrc
tail -f /vz/root/$1/var/log/auth.log >> /data/$1/tmp/$file.log &
