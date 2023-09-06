pip install -r requirements.txt
cp -i ./src/main.py /bin/remotegamepad.py

echo uinput | sudo tee -a /etc/modules
crontab -l | { cat; echo "@reboot python /bin/remotegamepad.py &"; } | crontab -
