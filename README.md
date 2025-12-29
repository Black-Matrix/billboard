# **Billboard**
#### Video Demo:  [Youtube Video](https://youtu.be/1KsMnA_OnMc?si=Grba49jfH7stS5OH)
#### Description: A web application to make Public/Anonymous posts that every user can see irrespective of registration.
## Inspiration
I always wanted for people to have a platform where they can voice their thoughts both publicly and anonymously. This led me to create this web app.
## How does it work
As a user you are first shown a Feed/Homepage which is common for everyone. This feed consists of posts made by users which can be made public, i.e username is shown or anonymous.

For someone to make a post, they must register and create a profile. The user can then start making posts right away.

This website can be useful when you want the people at your workplace/school to have a medium where they can be their true selves and be socially acceptable at the same time

## Technical overview
This app is built using Flask for the backend, with HTML, CSS, and a bit of JavaScript on the frontend, and Jinja for templating.

```
├── app.py
├── final.db
├── helpers.py
├── README.md
├── requirements.txt
├── static
│   └── bootstrap.min.css
└── templates
    ├── apology.html
    ├── create.html
    ├── index.html
    ├── layout.html
    ├── login.html
    ├── posts.html
    ├── profile.html
    └── register.html
```
For the styling of this project I have borrowed a styling template from bootswatch.

Coming to the structure of the project, firstly I want to talk about the HTML templates that I have created.

## Templates
### index.html
This file as the name might suggest is the homepage of this app. This is a shared feed for everyone including those who haven't logged in or registered.

This page consists of all the posts made by every user, both public and anonymous. The username for anonymous posts is not shown and the word *Anonymous* is shown in the place of the username

If a post is clicked on, the user is redirected to **posts.html**

### posts.html
This file is used to display a particular post. Each post has a uniquely generated **post_id** used internally.

The route is handled in the form of ***/posts/<post_id>***

When redirected to this page, the user can see the title, poster's name (Anonymous is shown if the post was made anonympusly), the date and time the post was made on, and the contents are shown below the header containing the other information.

### profile.html
This file is used to display the info of a user and the posts made by them. The anonymous posts are also shown if you are the owner of that profile and logged in while viewing.

From here you can scroll through a user's posts and view them by clicking on.

If the owner of the profile is logged in and viewing this page, can be accessed through the "My Profile" button on the navbar, this page also gives you functionality to update your bio, change your password and delete your posts. And to make a new post you can use the button on the navbar which says "Create Post".

### create.html
This page can be used by a logged in user to create a post. This page also gives the user an option to choose between public and anonymous posts and submit them to the Feed.

### login.html and register.html
These are self-explanatory

## Backend
The backend or app.py file contains the core of this website, where all the routes exposed by the backend are written. I have made sure to write code that handles db calls well and also handeld edge cases.

All of the backend, as mentioned earlier, is written using Flask because of the experience I've earned through this course.

helpers.py contains the functions which are abstracted away from app.py but help implement the functionality of the application as a whole.

## Database
The database final.db is written using sqlite and consists of 2 tables: users and posts.

## Components I have borrowed from CS50
The Login function, a part of the apology utility function, @login_required decorator and of course the CS50 library.
## How to host this yourself
Simply clone the repo and run the below commands:

1. Install the dependencies with

    ```
    pip install -r requirements.txt
    ```
2. In the directory where app.py exists, run

    ```
    flask run
    ```
## Note from me
Please feel free to go through the whole source code and help me make my project better or even criticism also helps.

Made with ❤️ by Black-Matrix
