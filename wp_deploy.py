import argparse
import json
import FileOps
import Database
file = FileOps.File()
database = Database.Database()


def main():
    app_name = "wp_deploy"
    parser = argparse.ArgumentParser()
    parser.add_argument('operation',
                        help='What you need to do? (init/deploy)')

    args = parser.parse_args()


    if args.operation == "init":
        print(''' __      ____________          ________  _____________________.____    ________ _____.___.
/  \    /  \______   \         \______ \ \_   _____/\______   \    |   \_____  \\__  |   |
\   \/\/   /|     ___/  ______  |    |  \ |    __)_  |     ___/    |    /   |   \/   |   |
 \        / |    |     /_____/  |    `   \|        \ |    |   |    |___/    |    \____   |
  \__/\  /  |____|             /_______  /_______  / |____|   |_______ \_______  / ______|
       \/                              \/        \/                   \/       \/\/       

PREREQUISTITES
====================================
1. Make sure your mysql binary files are in PATH
2. This application can only be used for deploying in Servers which support SSH.
====================================
     
       ''')
        user_input = input("Type Y and Press Enter to Continue or Press any other key to exit :")
        if user_input == "Y" or user_input=="y":
            while not file.create_config():
                file.create_config()
            print("Please run "+app_name+" deploy to deploy files to the server")
        else:
            exit()
    if args.operation == "run":
        try:
            config_file = open('deploy-config.json', 'r')
            config = json.loads(config_file.readlines()[0])
            database.backuptoedit(username=config['db_user'], password=config['db_password'], database=config['db_name'])
            database.restoretoedit(username=config['db_user'], password=config['db_password'], database=config['db_name'])
            database.change_rows(host=config['db_host'], username=config['db_user'], password=config['db_password'],
                                 database=config['db_name'], table_prefix=config['table_prefix'],
                                 localhost_url=config['localhost_url'], site_url=config['site_url'])
            database.backuptoexport(username=config['db_user'], password=config['db_password'], database=config['db_name'])
            file.changewpconfig()
            try:
                file.ftp_transfer(host=config['ftphostname'], username=config['ftp_user'], password=config['ftp_pass'],
                                   remote_dir_path=config['remote_dir_path'])
            except:
                file.sftp_transfer(host=config['ftphostname'], username=config['ftp_user'], password=config['ftp_pass'],
                                   remote_dir_path=config['remote_dir_path'])

            database.restorebackup(sshhostname=config['sshhostname'], sshuser=config['sshuser'], sshpassword=config['sshpassword'],
                                   dbuser=config['remote_db_user'], dbpass=config['remote_db_password'],
                                   dbname=config['db_name'], filepath=config['remote_dir_path'])
            file.resetwpconfig()
            print("Your site is Live at "+config['site_url'])

        except:
             print("deploy-config.json could not be found. Please run "+app_name+" init to create")




if __name__ == '__main__':
    main()
