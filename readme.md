# TUSOME 

This is a project to build a web application to draw a list of bestsellers via the NYTimes API and display them to logged in users, allowing them to make their own reviews on the same. Completely built on Flask .

My aim with this was to be able to learn how to best integrate 3rd party APIs with a web application, handling requests and building a social-like aspect into the application.

## SITE FLOW

https://user-images.githubusercontent.com/20756564/181215067-f91c69db-8ce8-46cd-9bb6-4dc8027994df.mp4

The user, on visiting the site, is brought to the landing page from where they can either register or login. As it stands now, after logging in, they are taken to the bestseller page which contains a lst oof that week's 15 bestsellers in the hardcover-fiction category according to the New York times Books API. They can then click on the Read More button to get the full synopsis of the selected book and also choose to write their own review.


## Future Functionality
***
Future functionality to be added according to roadmap:
1. Genre preference selection after registration.
2. Voting functionality on user reviews.
3. User reputation system.
4. Forum functionality.
5. Google Books API for covers and synopsis.
6. Shift everything to AWS or Heroku. 
***

## Design Philosophy
Built while aiming for a material design look using [MDB](https://mdbootstrap.com)
