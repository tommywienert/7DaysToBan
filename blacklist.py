import xml.dom.minidom as minidom
import re
import os
import glob
import json
import shutil

def load_config():
    config_file = 'config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        print("Paths missing, enter the paths (you only have to do this once)")
        log_dir = input("Enter the directory of the log files (usually <7daysServer directory>/7DaysToDieServer_Data): ")
        server_admin_file = input("Enter the directory of the serveradmin.xml file (usually <7Days UserDataFolder>/Saves): ")
        config = {'log_dir': log_dir, 'server_admin_file': server_admin_file + '/serveradmin.xml'}
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return config

def find_user_info(log_dir):
    user_info = {}
    for file in glob.glob(os.path.join(log_dir, 'output_log_*')):
        with open(file, 'r') as f:
            for line in f:
                match = re.search(r"PltfmId=\'([^\']+)\',\s*CrossId=\'([^\,]+)\',\s*OwnerID=\'([^\,]+),\sPlayerName=\'([^\']+)\'", line)
                if match:
                    platform_id, cross_id, owner_id, username = match.groups()
                    user_info[username] = {'platform_id': platform_id, 'cross_id': cross_id, 'owner_id': owner_id}
    return user_info

def create_backup(server_admin_file):
    backup_file = f"{server_admin_file}.bak"
    shutil.copyfile(server_admin_file, backup_file)
    print(f"Backup created: {backup_file}")

def is_user_banned(username, doc):
    blacklist_element = doc.getElementsByTagName('blacklist')[0]
    for blacklisted_element in blacklist_element.getElementsByTagName('blacklisted'):
        if blacklisted_element.getAttribute('name') == username:
            return True
    return False

def update_blacklist(username, platform_id, cross_id, doc, server_admin_file):
    if not is_user_banned(username, doc):
        blacklist_element = doc.getElementsByTagName('blacklist')[0]
        blacklisted_element = doc.createElement('blacklisted')
        blacklisted_element.setAttribute('platform', platform_id)
        blacklisted_element.setAttribute('userid', cross_id)
        blacklisted_element.setAttribute('name', username)
        blacklisted_element.setAttribute('reason', 'added via 7DaysToBan')
        blacklist_element.appendChild(doc.createTextNode('  '))
        blacklist_element.appendChild(blacklisted_element)
        blacklist_element.appendChild(doc.createTextNode('\n  '))
        with open(server_admin_file, 'w') as f:
            doc.writexml(f, encoding='utf-8', indent='', addindent='', newl='')
        print(f"User {username} has been banned!")
    else:
        print(f"User {username} is already banned!")

def main():
    config = load_config()
    log_dir = config['log_dir']
    server_admin_file = config['server_admin_file']
    create_backup(server_admin_file)
    doc = minidom.parse(server_admin_file)
    user_info = find_user_info(log_dir)
    print("Select a user to ban:")
    for i, (username, info) in enumerate(user_info.items()):
        print(f"{i+1}. {username}")
    choice = int(input("Enter the number of the user: ")) - 1
    username_to_ban = list(user_info.keys())[choice]
    platform_id = user_info[username_to_ban]['platform_id']
    cross_id = user_info[username_to_ban]['cross_id']
    update_blacklist(username_to_ban, platform_id, cross_id, doc, server_admin_file)

if __name__ == '__main__':
    main()
