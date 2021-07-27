# Neighborhood
## Author
Nicholas Ngetich
*****
### Description
This is a Django web application where users can set profile about them and a general location and their neighborhood name. The user can find a list of different businesses in the neighborhood, contact information for the health department and Police authorities near the neighborhood.A user can also create posts that will be visible to everyone in the neighborhood.
*****
### Home page
A user is required to register and login to the application. Upon successful authentication the user is redirected to home page where a user can see available neighborhoods. The user can then choose a neighborhood to move in or create a new neighbor by clicking Create Neighborhood button in the navbar
*****
![alt text](https://res.cloudinary.com/dbos9xidr/image/upload/v1627376287/screencapture-nick-neighbor-app-herokuapp-2021-07-27-11_42_31_rpwg0b.png)
*****
### User Profile
Every user registered in the application has profile associated with their account. Profile contains personal details of individual user. When a user click on name of other users in their neighborhood(People column), the profile of that particular user is displayed.
*****
![alt text](https://res.cloudinary.com/dbos9xidr/image/upload/v1627376253/screencapture-nick-neighbor-app-herokuapp-accounts-profile-2021-07-27-11_54_51_zx6jir.png)
*****
### Search Function
A user can search businesses in their neighborhhod and it will return the businesses matching the search term or display "Found 0 results if no match found by the search function.
*****
![alt text](https://res.cloudinary.com/dbos9xidr/image/upload/v1627376603/screencapture-nick-neighbor-app-herokuapp-search-2021-07-27-12_02_21_kgycqc.png)
*****
### Prerequisites
* Text editor eg Visual Studio Code
* You need to have git installed. You can install it with the following command in your terminal
`$ sudo apt install git-all`
*****
## Setup Instruction
To access this project on your local files, you can clone it using these steps
1. Open your terminal
1. Use this command to clone $ git clone https://github.com/ngetichnicholas/Neighborhood.git
1. This will clone the repositoty into your local folder
*****
## Dependencies
* django-bootstrap
* Pillow
* cloudinary
* psycopg2
* django-registration
* python-decouple
* Python Venv
* whitenoise
* gunicorn
*****
## Technologies Used
* HTML
* Python 3
* JavaScript
* CSS
******
### Live Link
Or you can access the web application directly via this [LIVE LINK](http://nick-neighbor-app.herokuapp.com/).
*****
### License
This project is under:  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE)

