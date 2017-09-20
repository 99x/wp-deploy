import json
import zipfile
import os
from colorama import *
import tarfile
from tqdm import tqdm
import ftplib
import pysftp
import warnings
warnings.filterwarnings("ignore")


class File:
    def __init__(self):
        init()
        ignore_list = ['site.zip', '', 'deploy-config.json']

    def fetch_old_config(self):
        # Fetches old WP Configurations from wp-config.php
        configs = {}
        data = []
        keys = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'table_prefix']
        filename = "wp-config.php"
        file = open(filename)
        for line in file:
            if "define" in line:
                data = line.split("'")
                if data[1] in keys:
                    configs[data[1]] = data[3]
            elif "$" in line:
                data = line[1:].split("  = ")
                configs[data[0].upper()] = data[1][1:-3]
        file.close()
        return configs

    def prompt_config(self):
        # Prompts user to enter new configurations info
        old_config = self.fetch_old_config()
        new_config = {}
        print("Please input the following details or press enter to keep old values...")
        print(Style.BRIGHT)
        new_config['db_host'] = input("Remote Host Name (Old Value:'" + old_config['DB_HOST'] + "'): ")
        new_config['db_name'] = input("Database Name (Old Value:'" + old_config['DB_NAME'] + "'): ")
        new_config['db_user'] = input("DB User Name (Old Value:'" + old_config['DB_USER'] + "'): ")
        new_config['db_password'] = input("DB Password (Old Value:'" + old_config['DB_PASSWORD'] + "'): ")
        new_config['site_url'] = input("Remote Site URL : ")
        new_config['ftp_user'] = input("FTP Username : ")
        new_config['ftp_pass'] = input("FTP Password : ")
        new_config['remote_dir_path'] = input("Enter Remote Directory path to transfer files : ")
        print(Style.RESET_ALL)

        return old_config, new_config

    def create_config(self):
        # Creates deploy-config.json file to use in deployment stage
        # Returns 1 if config created successfully ELSE 0
        strings = {'db_host': 'Remote Host Name', 'db_name': "Database Name", 'db_user': "Database User Name",
                   'db_password': "Database Password", 'site_url': "Remote Site URL", "ftp_user": "FTP User name",
                   "ftp_pass": "FTP Password"}
        is_completed = 0
        old_config, new_config = self.prompt_config()
        for key, value in new_config.items():
            if value == "":
                try:
                    new_config[key] = old_config[key.upper()]  # getting values from old configs
                    is_completed = 1
                except:
                    print(Fore.RED + Back.WHITE + "\n" + strings[
                        key] + " is missing to continue the process. Please re-enter them\n" + Fore.RESET + Back.RESET)

                    is_completed = 0
                    break
        if is_completed:
            file = open("deploy-config.json", "w")
            file.write(json.dumps(new_config))
            file.close()
            print("Config Created")
            return 1
        else:
            return 0

    def archive_site_zip(self):
        file_path = ""
        compression = ""
        root_dir = os.getcwd()
        ignore_list = ["site.zip"]
        zf = zipfile.ZipFile(ignore_list[0], mode='w')

        try:
            import zlib
            compression = zipfile.ZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED

        print("Archiving the site...")

        for dirName, subdirList, fileList in os.walk(root_dir):
            for fname in fileList:
                if fname not in ignore_list:
                    file_path = os.path.join(dirName, fname)
                    zf.write(file_path, os.path.relpath(file_path), compression)

        zf.close()

    def archive_site_tar(self):
        root_dir = os.getcwd()+"/"
        with tarfile.open("site.tar.gz", "w:gz") as tar:
            print("Archiving the site...")
            tar.add(root_dir, arcname=os.path.basename(root_dir))
            tar.close()

    def ftp_transfer(self, host, username, password, remote_dir_path):
        root_dir = os.getcwd()
        ftp = ftplib.FTP(host, username, password)
        print("Transferring Files to "+host)
        for dirName, subdirList, fileList in os.walk(root_dir):
            if os.path.isdir(os.path.relpath(dirName)):
                try:
                    ftp.mkd(os.path.join(remote_dir_path, os.path.relpath(dirName).replace("\\", "/")))
                except:
                    pass
            for fname in fileList:
                file_path = os.path.join(dirName, fname)
                filesize = os.path.getsize(file_path)
                file = open(file_path, 'rb')

                with tqdm(unit='blocks', unit_scale=True, leave=False, miniters=1, desc=fname,
                          total=filesize) as tqdm_instance:
                    if os.path.isdir(os.path.relpath(dirName)):
                        ftp.storbinary(
                            'STOR ' + os.path.join(remote_dir_path, os.path.relpath(dirName), fname).replace("\\", "/"),
                            file, 2048, callback=lambda sent: tqdm_instance.update(len(sent)))
                    else:
                        ftp.storbinary('STOR ' + os.path.join(remote_dir_path, fname), file, 2048,
                                       callback=lambda sent: tqdm_instance.update(len(sent)))
        print("File Transfer to "+host+" Completed:)")

    def sftp_transfer(self, host, username, password, remote_dir_path):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        srv = pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
        root_dir = os.getcwd()
        print("Transferring files to "+host)
        for dirName, subdirList, fileList in os.walk(root_dir):
            if os.path.isdir(os.path.relpath(dirName)):
                try:
                    srv.mkdir(os.path.join(remote_dir_path, os.path.relpath(dirName).replace("\\", "/")))
                except:
                    pass

            for fname in fileList:
                file_path = os.path.join(dirName, fname)
                filesize = os.path.getsize(file_path)

                with tqdm(unit='blocks', unit_scale=True, leave=False, miniters=1, desc=fname,
                          total=filesize) as tqdm_instance:
                    if os.path.isdir(os.path.relpath(dirName)):
                        srv.put(file_path,
                                os.path.join(remote_dir_path, os.path.relpath(dirName), fname).replace("\\", "/"),
                                callback=lambda sent, total: tqdm_instance.update(sent))
                    else:
                        srv.put(file_path, os.path.join(remote_dir_path, fname),
                                callback=lambda sent, total: tqdm_instance.update(sent))

        print("File Transfer to " + host + " Completed:)")

