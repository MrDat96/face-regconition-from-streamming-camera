# Local Server

** This is project develop for getting access permission to go in private place **

## Getting Started
These instructions will get you a copy of the propject up and running on your local machine for develop and testing.

## PROJECT STRUCTURE

This respository consists 2 main part: Camera Streamming and SAP AI

### Part 1: Camera Streamming: All code in camera_streamming directory
    * Consists a file called "streamming.py":
    ```-This file run as a process that do 2 main works:
            1. Get streamming from camera
            2. With every streamming frame, this will use "SSD algorithm" to detect real time to answer the question: "Do have anyone in that frame"
            3. With frame detected someone in that picture, it will send that frame to "Server" for "Recognization"```

### Part 2: Web application server: All code in sap_ai folder
    * Consists a structure of web server:
        ```- sap_ai: directory of web server
            - app 
                - ai_modules  # Collections of ai modules (recognition face, detect fire, ..) (Only recognition for now) 
                    - recognition.py # Faces recognition
                - models    # Consist models that for create instance and store data to database 
                    - camera.py
                    - check_in_status.py
                    - checkin.py
                    - role.py
                    - room.py
                    - user.py
                - routers   # Responsive for come in requests and navigate
                    - camera_api.py
                    - checkin_api.py
                    - recognition_api.py
                    - role_api.py
                    - room_api.py
                    - users_api.py
                - static    # Consist of file that use for buidling GUI
                    - css
                    - front-awesome
                    - fonts
                    - js
                - template   # Consist of html file for views data and show by GUI
                - __init__.py   # Help to initial App, db and configurations to run server
            - data
                - encode_data   # Consist of .fev are encode file, that file is model of a person is trainned.
                - images_data   # Save image sent from camera streamming process above.
            - instance
                - config.py     # Help for building environment variales for server
            - mqtt
                - client_sub.py # Testing only
                - publisher.py  # responsive for publish information of User detected
            - .env  # Environments variable
            - manage.py #  Manage version for DB
            - run.py    # Initial app, place app start to run```


## INSTALLS
    Installation devides to two part: Installs one for running web server and another for process of detect, recognition faces
### Install for running web server
* Update your os system
``` sudo apt-get update ```
* Create a virtual environment for python ( required python 3.6.x ). This environment will separate will globale environment. If something wrong in this envirment, it does not effect to global environment. We can easily remove this environment.
``` python3 -m venv ENV_FAS ```
* Access to ENV_FAS environment
``` source ENV_FAS/bin/activate ```
* Install library required in that enviroinment
``` pip install flask flask_script flask-sqlalchemy psycopg2-binary flask-migrate ```
* Now you can go to *sap_ai* folder and run:
``` python3 run.py ``` 
* Now you can go to browser and enter: http://localhost:5001/. But for now, your local don't have database to run get data.
    So next steps, you need to install Database in your local. I recommend: MySQL or PostgreSQL
[Postgre SQL in ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
If you use MySQL, you should change DATABASE_URL in .env to "DATABASE_URL="mysql:///sap_api"
* Oke, now you can go to http://localhost:5001 to view all user, cameras,..., add more one of thems,...

### Install for running recognition faces. Make sure that you are still in Virtual environment ENV_FAS
* First you need to download fas-recognition repository to you disk. You need permission for this step
``` git clone https://gitlab.com/facial-attendance-system/fas-recognition.git ```
Or you can clone from my fork
``` git clone https://gitlab.com/ngothucdat96/fas-recognition.git ```
* After you clone fas-recognition, you need *cd* to go that respo:
``` cd fas-recognition ```
* Install depenencies packages
``` python3 -m setup.py install ```

### Finishing install
* Now, go to check your face and run regconition

## Authors
    MrDAT - Ngo Thuc Dat - SE62120

## License
    This is private project is developed for learning and studying at FPT_University HN, VietNam