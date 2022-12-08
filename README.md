# Installation
Assuming git and python are installed. Open a command line and navigate to the directory the sample is to be run from:

## Create the python virtual environment
Create a separate python instance called a virtual environment to not accidentally install random packages into your core python instance  
`pyton -m venv glider_reader_env`

## Start the python virtual environment
`.\glider_reader_env\Scripts\activate`

## Clone the project
`git clone https://github.com/upsonp/glider_reader.git`  

## update the python virtual environment's packages
`cd glider_reader`  
`python -m pip install -r requirements.txt`

## Run Django migrations to create the database
`python .\manage.py migrate`

## Access the Django shell
`python .\manage.py shell`

## Create a mission
```
# import the specific django model we're using
from glider_reader import models

# Create a mission object
m = models.Mission(mission_number=59)
m.save()

# add some gliders to it
g = models.Glider(mission=m, label="SEA019")
g.save()
g = models.Glider(mission=m, label="SEA020")
g.save()
g = models.Glider(mission=m, label="SEA021")
g.save()

# Create another mission
m = models.Mission(mission_number=60)
m.save()

# Add some glidrs to it
g = models.Glider(mission=m, label="SEA019")
g.save()

g = models.Glider(mission=m, label="SEA015")
g.save()

# list the missions:
models.Mission.objects.all()

# list the gliders:
models.Glider.objects.all()

# get all gliders from mission 59
models.Mission.objects.get(mission_number=59).gliders.all()

# get the Missions with a glider labeled 'SEA019' attached
gliders = models.Glider.objects.filter(label='SEA019')
for glider in gliders:
 print(f"Mission: {glider.mission.mission_number} has a 'SEA019' Glider")

# Get only missions that have a 'SEA015' glider
for mission in models.Mission.objects.filter(gliders__label='SEA015'):
 print(f"Mission: {mission.mission_number} has a glider named 'SEA015'")

# Hit enter to delete all the missions along with gliders attached to them
# to start with an empty database. Or don't and play with the data
models.Mission.objects.all().delete()

