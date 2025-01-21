#!/bin/bash

BACKUP_SRC="$HOME"
BACKUP_DIR="/backups/homefolder"
BACKUP_LOG="$BACKUP_DIR/backup.log"

rsync -av --delete "$BACKUP_SRC" "$BACKUP_DIR" >> "$BACKUP_LOG"
echo "Backup COmplete: " $(date '+%Y-%m-%d') >> "$BACKUP_LOG"

