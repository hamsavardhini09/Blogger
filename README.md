##Blogger (Python, Google App Engine)##


This is a blog project in python on google app engine. It has basic blog features like New post submission,
view posts, Google Login and Logout.


Please use the below url to access application


http://blogger-gae.appspot.com


Without login users can just view/read blog posts as Guests. To post, users should go through login
functionality provided by google App engine.


####App engine services used####


*App Engine Datastore<br>
*Google User Management


When application is running Data store index will be created that contains status of index that is used.
A data store index must be created when query is used to order while querying from .


https://console.cloud.google.com/datastore/indexes?project=blogger-gae


This simple blogger can be extended to match with bloggers blogger.com,wordpress.com,joomla.com.
Future work includes adding comments to posts,page nation, Social media sharing for posts, showing Recent posts on tabs, RSS feeds, etc.