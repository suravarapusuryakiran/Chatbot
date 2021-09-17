# Read Me before starting THE BOT

* Python version is 3.8.10

* Rasa version is 2.7.1

* rasa x runs on port - 5002 but we are changing it to  (5000)
  * rasa x --rasa-x-port 5000
* rasa actions - 5055
* rasa server - 5005


* To enable rasa api calls    rasa x -m models --enable-api --cors "*" --debug  

* installing certbot (sudo apt-get install certbot)
* To create a certificate from scratch for your domain (sudo certbot certonly)

* Do not install Jupyter Notebook 

* pip version should only be 21.1.2

* Install Panda
  ```bash
  pip install pandas==1.2.5
  ```

* Before training Bot please clear/delete cache from actions/_pycache_ and tests/_pycache_ (for the the first time only)

* Create folder in CAD_CHATBOT/cache/windchill

* To read excel data 
  * Use the package manager pip to install 
    ```bash
    pip install xlrd==1.2.0 
    ```
  * if you are not able read excel sheet after adding above package then try  to install this package
    ```bash
    pip install openpyxl
    ``` 
