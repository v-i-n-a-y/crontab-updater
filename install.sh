#!/bin/bash
#


python3 generate.py
mkdir -p $HOME/.local/bin
cp update.sh $HOME/.local/bin
chmod +x $HOME/.local/bin/update.sh
touch $HOME/update.log

CRON_JOB="0 2 1 * * $HOME/.local/bin/update.sh"

crontab -l > ~/crontab_backup.txt 2>/dev/null

if crontab -l | grep -Fxq "$CRON_JOB"; then
				echo "The cron job is already configured."
else
				echo "Adding ${CRON_JOB} to crontab"
				(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
				echo "Cron job added successfully."
fi

echo "Crontab updated, here is the updated one:"
crontab -l

