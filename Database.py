import os
import MySQLdb as mdb
import paramiko


class Database:
    def __init__(self):

        self.backup_file = "backup.sql"
        self.backup_file_local = "backup_local.sql"

    def backuptoedit(self, username, password, database):
        exec_code = ""

        if password == "":
            exec_code = "mysqldump"+" -u "+username+" "+database+" > "+self.backup_file_local
        else:
            exec_code = "mysqldump"+" -u " + username + " -p"+password+" " + database + " > "+self.backup_file_local

        print("Duplicating Database '" + database+"'")
        os.system(exec_code)

        if int(os.stat(self.backup_file_local).st_size) > 0:
            print("Database Duplicated :)")

    def restoretoedit(self, username, password, database):
        if password == "":
            exec_code = "mysqladmin -u "+username+" create "+database+"_wp_deploy_backup"
        else:
            exec_code = "mysqladmin -u " + username + " -p"+password+" create "+database+"_wp_deploy_backup"

        os.system(exec_code)

        if password == "":
            exec_code = "mysql -u " + username +" " + database + "_wp_deploy_backup < " + self.backup_file_local
        else:
            exec_code = "mysql -u " + username + " -p" + password + " " + database + "_wp_deploy_backup < " + self.backup_file_local

        os.system(exec_code)

    def change_rows(self, host, username, password, database, table_prefix, localhost_url,site_url):
        database = database+"_wp_deploy_backup"
        con = mdb.connect(host, username, password, database)
        cur = con.cursor()
        # Update site_url and home in _options table
        table_name = table_prefix+"options"
        cur.execute("UPDATE "+table_name+" SET option_value=%s WHERE option_name=%s", (site_url, "siteurl"))
        cur.execute("UPDATE " + table_name + " SET option_value=%s WHERE option_name=%s", (site_url, "home"))
        con.commit()

        # Update images and broken links
        table_name = table_prefix+"posts"
        cur.execute("UPDATE "+table_name+" SET post_content = REPLACE(post_content, %s, %s)", (localhost_url+"/", site_url+"/"))
        con.commit()

        print("Updated DB Rows for Migration...")

    def backuptoexport(self,username, password, database):
        print("Creating Database backup '" + database + "'")
        database = database+"_wp_deploy_backup"

        if password == "":
            exec_code = "mysqldump" + " -u " + username + " " + database + " > " + self.backup_file
        else:
            exec_code = "mysqldump" + " -u " + username + " -p" + password + " " + database + " > " + self.backup_file

        os.system(exec_code)

        if int(os.stat(self.backup_file).st_size) > 0:
            print("Database Backup Created :)")

    def restorebackup(self, sshhostname, sshuser, sshpassword, dbuser, dbpass, dbname, filepath="/var/www/html/"):
        backup_file_path = filepath+self.backup_file
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(sshhostname, username=sshuser, password=sshpassword)
        if dbpass == "":
            print("Restoring Database '"+dbname+"'")
            stdin, stdout, stderr = ssh.exec_command("mysqladmin -u "+dbuser+" create "+dbname)
            stdin, stdout, stderr = ssh.exec_command("mysql -u "+dbuser+" "+dbname+"< "+backup_file_path)
            print("Database Restored")
        else:
            print("Restoring Database '" + dbname + "'")
            stdin, stdout, stderr = ssh.exec_command("mysqladmin -u "+dbuser+" -p"+dbpass+"create "+dbname)
            stdin, stdout, stderr = ssh.exec_command("mysql -u " + dbuser + " -p"+dbpass+" "+dbname+"  < "+backup_file_path)
            print("Database Restored")
        ssh.close()

