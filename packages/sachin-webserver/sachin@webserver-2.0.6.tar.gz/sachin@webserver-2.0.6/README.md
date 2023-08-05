# webserver
This is simple webserver that uses PHP development Environments.  
This helps you to use local-webserver for your developement environment.  
This feature comes along with the PHP you have on you computer.  
This program just help to access it with single command.  
This is a Command-Line Tool  

----------------------------------------------------
## Installation
(Note: To use this module, you must have PHP installed in your device [which you can download from here](https://www.php.net/downloads)  
add it in your system path variable)  
You can find .whl(wheel) file in dist folder.  
Navigate to dist folder and hit the following command  
````cmd
python -m pip install wheel_file_name ; try pip3 if pip didn't work.  
````
## Warning
For Python version above or equals to 3.10, only version 3 (webserver-1.0.3-py3-none-any.whl) will work.  
I don't know but I find it hard to install pathlib in these versions of python which is essential package for webserver.  
However, version 3 (webserver) uses pathlib2 so it is good to go.  

There is no difference between v2 and v3 otherthan pathlib packages
## Usages
1. Basic Command
````powershell
    server --help
````
This displayes all the options

2. Starting Server
````powershell
    server
````
This start server on port 8000
URL: http://localhost:8000

3. Passing Options
host: your hostname. Default localhost or 127.0.0.1  
port your port. Default 8000  
````powershell
    server --host hostname --port port_number # These are optional parameter. These are not manditory
````
If --update is passed along with the above flags, Host and Port will be added to settings.json

4. Opening PHPMYADMIN
````powershell
    server --admin
````
This opens phpmyadmin.  
cannot use this with --admin  
It opens PhpMyAdmin under the port and host found in settings.json in installed folder or  
The PORT and HOST passed with flag --port and --host previously.  
To Access and edit this file, --set can be use as a flag.  
````powershell
    server --set
````

[More](webserver/README.md)
