# WP-DEPLOY
> Wordpress Deployment Solution for Servers with SSH access

Sometimes it is so harder to deploy your local wordpress site to a remote server. wp-deploy will 
definitely make it easier for you to deploy your local site into a remote server without any hassle

![](header.png)

## Requirements
* **Python 3.0 or higher**
* **Operating Systems:** Windows, Linux or OSX
* **PATH Variables:** mysql path variables should be set
* **Supported Hosts:** Any server with SSH and FTP Access 

## Usage
1. Install Dependencies
```
$ pip install -r requirements.txt
```
OR 
```
$ pip3 install -r requirements.txt
```
2. Go to the directory which has the local wordpress site

3. Create deploy-config.json file
```
python3 wp_deploy.py init
```


4. Create database backups and deploy to the server

```
python3 wp_deploy.py run
```

## Create Standalone app
run the below command
```
pyinstaller wp_deploy
```
Your app will be placed at *dist/wp_deploy* 

## Release History

* 1.0.0
    * Initial Release



## Contributing

Since this is an open source project, we would like to see you contribute to this project to enhance
the features and reduce bugs. If you'd like to contribute, the steps are as follows.

1. Fork it (<https://github.com/99xt/wp-deploy/>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -m 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

Happy Contributing :)

## Acknowledgement
I would like to thank @rehrumesh ,@thinkholic @lakindu95 for metoring me and guiding me through this
two weeks to create this awesome tool which was initiated through **Hacktitude** by Dotitude, 99x
Technology.

