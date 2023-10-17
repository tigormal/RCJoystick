pip install -r requirements.txt
cp -i ./src/main.py /bin/rcjoystick.py

echo uinput | sudo tee -a /etc/modules
# echo uinput >> /etc/modules-load.d/rcjoystick.conf
crontab -l | { cat; echo "@reboot python /bin/rcjoystick.py &"; } | crontab -
# cp ./rcjoystick.service /etc/systemd/system
