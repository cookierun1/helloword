# winebow


## Development Environment

- python=3.8.13
- django=3.2.13

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

