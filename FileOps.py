import json


class File:

    def __init__(self):
        ignore_list = ['site.zip','','deploy-config.json']

    def fetch_old_config(self):
        # Fetches old WP Configurations from wp-config.php
        configs = {}
        data = []
        filename = "wp-config.php"
        file = open(filename)
        for line in file:
            if "define" in line:
                data = line.split("'")
                configs[data[1]] = data[3]
            if "NONCE_SALT" in line:
                break
        file.close()
        return configs

    def prompt_config(self):
        # Prompts user to enter new configurations info
        old_config = self.fetch_old_config()
        new_config = {}
        print("Please input the following details or press enter to keep old values...")
        new_config['db_host'] = raw_input("Remote Host Name (Old Value:'"+old_config['DB_HOST']+"'): ")
        new_config['db_name'] = raw_input("Database Name (Old Value:'"+old_config['DB_NAME']+"'): ")
        new_config['db_user'] = raw_input("DB User Name (Old Value:'"+old_config['DB_USER']+"'): ")
        new_config['db_password'] = raw_input("DB Password (Old Value:'"+old_config['DB_PASSWORD']+"'): ")
        new_config['site_url'] = raw_input("Remote Site URL : ")
        new_config['ftp_user'] = raw_input("FTP Username : ")
        new_config['ftp_pass'] = raw_input("FTP Password : ")

        return old_config,new_config

    def create_config(self):
        # Creates deploy-config.json file to use in deployment stage
        old_config, new_config = self.prompt_config()
        for key, value in new_config.iteritems():
            if value == "":
                try:
                    new_config[key] = old_config[key.upper()]  # getting values from old configs
                except:
                    print "Some details are missing to continue the process. Please re-enter them"
                    self.prompt_config()
        file = open("deploy-config.json", "w")
        file.write(json.dumps(new_config))
        file.close()
        print "Config Created"







import os
os.chdir("D:\\xampp\\htdocs\\wordpress")
f = File()
f.create_config()
