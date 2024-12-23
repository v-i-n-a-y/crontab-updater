#!/bin/bash
#
# macOS crontab Updater
#
# The family doesn't know how to use computers...... :(


CRON_JOB="0 2 1 * * /bin/bash -c 'brew update && brew upgrade -y && softwareupdate -ia' > ~/update_log.txt 2>&1"

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

