cp -i ./src/main.py /bin/remotegamepad.py
# crontab -l > .tmpcron
crontab -l | { cat; echo "@reboot python /bin/remotegamepad.py &"; } | crontab -
# echo "@reboot python /bin/remotegamepad.py &" >> .tmpcron
# crontab .tmpcron
# rm .tmpcron