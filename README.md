# Winebow

Winebow is A platform system that considers the scalability of the wine information integration service based on the establishment of an online basis for domestic wine trading.

## Development Environment

|Category| - |
| --- | --- |
|Language|python v3.8.13|
|Web Framework|Django v3.2.13|
|UI Template|NiceAdmin v2.2.2, Delicious v4.7.1|
|Built with|Bootstrap v5.1.3|

## How to Execute

Execute the following lines to properly clone and run the project.

config.yaml file is required.

```
$ git clone https://github.com/winebowray/winebow.git
add config.yaml to /winebow/config 
$ conda create -n ["env"] python=3.8
$ conda activate ["env"]
$ cd winebow
$ pip install -r requirements.txt
$ python manage.py runserver

