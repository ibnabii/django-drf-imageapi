# Image API
![python](./docs/python.svg)
![django](./docs/django-icon.svg)
![sqlite](./docs/sqlite.svg)
## Installation
- create python virtual environment
- execute following commands in terminal:
```shell
git clone https://github.com/ibnabii/django-drf-imageapi
cd .\django-drf-imageapi\      
pip  install -r .\requirements.txt         
python manage.py migrate
python manage.py loaddata .\data.json                           
```
## User & plans management
### User management is done via Django Admin panel available under admin/ url.
- User Admin page have 'PROFILE' tab added at the bottom of the screen to select which Service Plan they use.
- API users should be created with 'Staff status' unchecked.
- Staff users can have null Profile. Note that users with null Profile will be allowed to upload images, but no links will be provided
### Serivce Plan management is done via Django Admin panel available under admin/ url
For each service plan multiple (or none) number of thumbnail sizes may be defined, as well as if:
- plan allows linking to the original image
- user can create an expiring link to the image

Note that redefining plan's thumbnail settings or changing plan
assigned to a user triggers a procedure that re-renders thumbnails of 
images affected by the change. This is done for demo purposes. In real
life environment, this should be unhooked and run as night processing
or other way that will not cause performance issues.
### Preconfigured service plans for demo purposes
As defined in task (Basic, Premium, Enterprise)
### Preconfigured users for demo purposes
#### planadmin/planadmin
Has power over plans (and users to assign plans to them)
#### user1/user1, user2/user2
API users
- user1 has Basic plan assigned
- user2 has Enterprise plan asigned
## Creating temporary img links
To create temporary img link update *temp_link_longevity* 
field of an image with number of seconds indicating how long the link should
live (within 300-30000 range). 
- *temp_link_longevity* will be set to 0
- link will be created in *temp_link*
- link expiring timestamp will be stored in *temp_link_expire_time*
