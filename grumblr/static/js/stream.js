var isTyping = false;
var stream_data = {}

$( document ).ready(function() {

	get_stream_json(true);
	setInterval(get_stream_json, 5000, false);

});

function get_stream_json(flag){
	if(isTyping == false || flag){
		$.getJSON( "json/", function( data ) {
			diff = filter(stream_data,data);
			console.log(diff.length);
			stream_data = data;
			if(flag || diff.length > 0){
				load_stream(diff, flag);
			}
			
		});
	}

	
}

function load_stream(posts, flag){
	var post_list = document.getElementById('post-list');
	//post_list.innerText = '';
	if(posts.length == 0){
		var tmpl = document.getElementById('post-template').content.cloneNode(true);
		tmpl.querySelector('.card-text').innerText = 'Nothing going on!';
		tmpl.querySelector('.post-image-div').remove();
		tmpl.querySelector('.card-bottom-overlay').remove();
		tmpl.querySelector('.card-comment-container').remove();

		post_list.appendChild(tmpl);
	}
	else{

		for (var i = 0; i < posts.length; i++) {
			var post = posts[i];
			var tmpl = document.getElementById('post-template').content.cloneNode(true);
			if(post.attachment != undefined){
				tmpl.querySelector('.post-image').src =  post['attachment'];
			}else{
				tmpl.querySelector('.post-image').remove();
			}

			tmpl.querySelector('.card-text').innerText = post.desc;
			if(post['userprofile']['avatar'] != undefined){
				tmpl.querySelector('#post-user-avatar').src =  post['userprofile']['avatar'];

			}else{
				tmpl.querySelector('#post-user-avatar').src = static_url + "images/default-avatar.png";

			}

			//set card id as post id
			tmpl.querySelector('.card').id = post['id'];
			tmpl.querySelector('#post-user-link').href = profile_url.replace (999, post['userprofile']['user']['id']);
			tmpl.querySelector('#post-user').innerText = post['userprofile']['user']['first_name'];
			tmpl.querySelector('.date-time').innerText = UTCToLocalTime(post.timestamp);
			tmpl.querySelector('#comment-post-id').value = post['id'];
			tmpl.querySelector('#comment-form').addEventListener("submit", function(e){
			    e.preventDefault();
			    var url = comment_url;
			    var formData = {};
			    $(this).find("input[name]").each(function (index, node) {
			        formData[node.name] = node.value;
			    });
			    $.post(url, formData).done( function(msg) { 
			    	//console.log("added comment");
			    	get_stream_json(true);

			     } ).fail( function(xhr, textStatus, errorThrown) {
			        console.log(xhr.responseText);
			    });

			    return false;
			});

			tmpl.querySelector('.comment-input').addEventListener("focus", function(){
			   		isTyping = true;
				});
			tmpl.querySelector('.comment-input').addEventListener("blur", function(){
			   		isTyping = false;
				});


			//comments
			var comments = post["comments"];
			var comment_list = tmpl.querySelector('#comments');
			comment_list.innerText = '';
			for (var j = 0; j < comments.length; j++) {
				var comment = comments[j];
				var ctmpl = document.getElementById('comment-template').content.cloneNode(true);
				ctmpl.querySelector('#comment-user-link').href = profile_url.replace (999, comment['userprofile']['user']['id']);
				ctmpl.querySelector('#comment-user').innerText = comment['userprofile']['user']['first_name'];
				ctmpl.querySelector('.comment-time').innerText = UTCToLocalTime(comment.timestamp);
				ctmpl.querySelector('#comment').innerText = comment.desc;
				if(comment['userprofile']['avatar'] != undefined){
					ctmpl.querySelector('#comment-user-avatar').src =  comment['userprofile']['avatar'];

				}else{
					ctmpl.querySelector('#comment-user-avatar').src = static_url + "images/default-avatar.png";

				}

				comment_list.appendChild(ctmpl);
			}

			if ( $('#'+post['id']).length > 0 ) {
			  	//post already exists so replace with new one
			  	$('#'+post['id']).replaceWith(tmpl);
			}
			else{
				$("#post-list").prepend(tmpl);
			}
			
		}

		
		
	}

}

//this method checks difference between two json objects and returns diffs
function filter(obj1, obj2) {
    var map = {};
    var str1 = JSON.stringify(obj1);
    var str2 = JSON.stringify(obj2);
    
    for(var i=0;i<obj1.length;i++){
    	var item = obj1[i];
        var item_str = JSON.stringify(item);
    	if(str2.indexOf(item_str) == -1){
        	map[item['id']] = item;
        }
    }
    
    for(var i=0;i<obj2.length;i++){
    	var item = obj2[i];
        var item_str = JSON.stringify(item);
        if(str1.indexOf(item_str) == -1){
        	map[item['id']] = item;
        }
    }
    
    var result = [];
    for (var key in map){
    	result.push(map[key]);
	}
    return result;
}


function UTCToLocalTime(d) {
	  d = new Date(d);
      var hour = d.getHours();
	  var minute = d.getMinutes();
	  var amPM = (hour > 11) ? " PM" : " AM";
	  if(hour > 12) {
	    hour -= 12;
	  } else if(hour == 0) {
	    hour = "12";
	  }
	  if(minute < 10) {
	    minute = "0" + minute;
	  }
	  
    return d.toUTCString().slice(0, 12) + hour + ":" + minute + amPM;
   
}