import platform
import json
import os

CONFIG_FILE = "commands.json"
OUTPUT_FILE = "update.sh"

def header(system: str):

    with open(OUTPUT_FILE, "w") as file:
        file.write("#!/bin/bash\n")
        file.write("# AUTOGENERATED FILE\n")
        file.write('LOGFILE="$HOME/update.log"\n')
        file.write("TMPFILE='/tmp/update_temp.log'\n")
        file.write("BOT_TOKEN=\"7261881445:AAGWoDqiHzpWGqtTyKAccAQpsOrXAjL_i3o\"\n")
        file.write("CHAT_ID=\"8146423828\"\n")
        file.write("COMPUTER=\"$(hostname)\"\n")
        file.write("MESSAGE=\"Automated Update Results for $COMPUTER:\"\n")
        file.write("run () {\n")
        file.write("    command=$1\n")
        file.write("    echo \"$(date)\" >> $TMPFILE 2>&1\n")
        file.write("    echo \"Running $command\" >> $TMPFILE 2>&1\n")
        file.write("    $command >> $TMPFILE 2>&1\n")
        file.write("    command_status=$?\n")
        file.write("    if grep -q 'password' $TMPFILE; then\n")
        file.write("        echo 'Password required. Opening terminal...'\n")

        match system:
            case "linux":
                file.write("        gnome-terminal -- bash -c \"sudo $command; exec bash\"\n")
            case "darwin":
                file.write("        osascript -e 'tell application \"Terminal\" to do script \"sudo $command\"'\n")
        file.write("    fi\n")
        file.write("    cat $TMPFILE >> $LOGFILE\n")
        file.write("    MESSAGE=\"$MESSAGE $(cat $TMPFILE)\"\n")
        file.write("    if [[ $command_status -ne 0 ]]; then\n")
        file.write("    MESSAGE=\"$MESSAGE UPDATE FAILED\"\n")
        file.write("    notify command_status\n")
        file.write("    rm $TMPFILE\n")
        file.write("    exit 1\n")
        file.write("    fi\n")
        file.write("    rm $TMPFILE\n")
        file.write("}\n\n")
        file.write("notify(){\n")
        file.write("    TITLE=\"Automatic Updates\"\n")
        file.write("    if [[ $1 -ne 0 ]]; then\n")
        file.write("    MSSG=\"Update failed\"\n")
        file.write("    else\n")
        file.write("    MSSG=\"Update completed\"\n")
        file.write("fi\n")
        match system:
            case "linux":
                file.write('    notify-send "$TITLE" "$MSSG"\n')
            case "darwin":
                file.write('osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"\n')
        file.write("    # Send message to Telegram\n")
        file.write("    response=$(curl -s -w \"%{http_code}\" -o /dev/null -X POST \"https://api.telegram.org/bot$BOT_TOKEN/sendMessage\" \\\n")
        file.write("        -d chat_id=\"$CHAT_ID\" -d text=\"$MESSAGE\")\n")
        file.write("    # Check if the curl command was successful\n")
        file.write("    if [ \"$response\" -ne 200 ]; then\n")
        file.write("        echo \"Failed to send message to Telegram. HTTP response code: $response\" >> $LOGFILE\n")
        file.write("    else\n")
        file.write("        echo \"Update message sent to Telegram successfully.\" >> $LOGFILE\n")
        file.write("    fi\n")
        
        file.write("}\n\n")



def append_commands(system: str, commands: dict):
    with open(OUTPUT_FILE, "a") as file:
        for command in commands.get(system, []):
            user_input = input(f"Do you want to include '{command['description']}: {command['command']}'? (y/n)").strip().lower()
            if user_input == "y":
                file.write(f"run \"{command['command']}\"\n")
        file.write("notify\n")
        file.write("exit 0\n")

def main():
    print("Generating update.sh")

    system = platform.system().lower()

    with open(CONFIG_FILE, "r") as f:
        commands = json.load(f)

    if system not in ["linux", "darwin"]:
        print("Unsupported OS, only Linux and macOS are supported. Exiting...")
        exit(1)

    print(f"{system.capitalize()} detected...")
    header(system)
    append_commands(system, commands)

    print(f"Shell script {OUTPUT_FILE} has been generated.")

    os.system(f"cat {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

