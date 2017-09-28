import FileOps,sys
print(sys.path)
file = FileOps.File()


def test_fetch_old_config():
    data = file.fetch_old_config()
    assert list(data.values())[0] != "" and list(data.values())[1] != ""


def test_prompt_config():

    new_config = {'db_host' : "", 'db_name':'', 'db_user':'', 'db_password':'', 'remote_db_host':'127.0.0.1',
                  'remote_db_user': 'root', 'remote_db_password':'dummy','localhost_url':'http://localhost/site_name',
                  'site_url':'http://www.example.com', 'sshhostname':'127.0.0.1','sshuser':'root','sshpassword':'dummy',
                  'ftphostname':'127.0.0.1', 'ftp_user':'root','ftp_pass':'dummy', 'remote_dir_path':'/var/www/html',
                  'table_prefix':"wp_"}
    data,data2 = file.prompt_config(new_config)
    assert list(data.values())[0] != "" and list(data.values())[1] != ""
    assert data2['remote_db_host'] != "" and data2['remote_db_user'] != "" and data2['remote_db_password'] != "" and \
        data2['localhost_url'] != "" and data2['site_url'] != "" and data2['sshhostname']!="" and\
           data2['sshuser']!="" and data2['sshpassword']!="" and data2['ftphostname']!="" and data2['ftp_user']!="" and\
        data2['ftp_pass']!="" and data2['remote_dir_path']!="" and data2['table_prefix'] !=""


def test_create_config():
    new_config = {'db_host': "", 'db_name': '', 'db_user': '', 'db_password': '', 'remote_db_host': '127.0.0.1',
                  'remote_db_user': 'root', 'remote_db_password': 'dummy',
                  'localhost_url': 'http://localhost/site_name',
                  'site_url': 'http://www.example.com', 'sshhostname': '127.0.0.1', 'sshuser': 'root',
                  'sshpassword': 'dummy',
                  'ftphostname': '127.0.0.1', 'ftp_user': 'root', 'ftp_pass': 'dummy',
                  'remote_dir_path': '/var/www/html',
                  'table_prefix': "wp_"}
    data = file.create_config(new_config)
    assert data == 1


