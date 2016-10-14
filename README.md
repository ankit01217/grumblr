General Notes for Hw5 - Grumblr Application


Rest_Framework Module for Serializers
-------------------------------------------------------------------------------------------
I have used django rest_framework module for nested serilizing using serializer classes. All classes are in grumblr/serialzers.py file  
	1) PostSerializer
	2) UserSerializer
	3) UserProfileSerializer
	4) CommentSerializer

Ajax updates 
-------------------------------------------------------------------------------------------
I have used grumblr.js for loading posts after every 5 seconds. Also i have added filter method which basically compares new posts and old posts data and only update new posts instead of reloading whole page
	1) Jquery Ajax method($.getJSON) is used to fetch json data 
	2) Jquery Ajax method($.post) is used to add comment in post
	3) Both post and comments are updated asynchromously without page refresh


<template> element for reusable client template
-------------------------------------------------------------------------------------------
I have used "post_template.html" template which is used by grumblr.js to dynamically load content from json data
	1) reusable template element makes it easy to maintain 
	2) post_template is used in muliple pages (profile, friendstream, global stream) for all posts	

	
AJAX data loading
-------------------------------------------------------------------------------------------
I am using grumblr.js to load json data after every 5 seconds. 
	1) "get_stream_json" function in grumblr.js stores previous loaded data and checks difference between new data and old data using "filter" mehtod in grumblr.js
	2) Based on difference, if there are any changes to old data, it will add only posts or updated posts since last request instead of entire page reload	


