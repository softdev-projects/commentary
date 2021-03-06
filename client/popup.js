// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the URL of the current tab
 *   is found.
 **/
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });

  // Most methods of the Chrome extension APIs are asynchronous. This means that
  // you CANNOT do something like this:
  //
  // var url;
  // chrome.tabs.query(queryInfo, function(tabs) {
  //   url = tabs[0].url;
  // });
  // alert(url); // Shows "undefined", because chrome.tabs.query is async.
}

function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;

}

//list is a JSON list : comments [ user_id, comment, date ]
// {comment} posted by {user_id} on {date} \n
function commentify(list) { 
    var text = "";
    for (i=0;i<list["comments"].length;i++){
	var user_id = list["comments"][i]['user_id'];
	var comment = list["comments"][i]['content'];
	//var date = s['date']
	text = text + comment + " ";
    }
    return text;
}

function getURL(list) {
    return list['url'];
}

   
function renderComments(commentText) { 
    document.getElementById('comments').textContent = commentText;
}

function renderCommentsURL(url) {
    document.getElementById('commentsURL').textContent = url;
}


function submitComment(commentData) {
  console.log(commentData);
  var xhr = new XMLHttpRequest();
  var url = commentData[url];
  xhr.open('POST', 'http://127.0.0.1:5000/comments/new');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(commentData));
}

function retrieveComments(url) { 
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
	if (xhr.readyState == 4) {
	    //console.log(xhr.responseText);
	    var list = xhr.responseText;
	    //console.log(list);
	}
    }
    var server = 'http://127.0.0.1:5000/comments?url=' + url;
    xhr.open('GET',server);
    xhr.setRequestHeader('Content-Type','text/html; charset=utf-8');
    xhr.send(null);
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('send_button').addEventListener('click',
          function() {
            getCurrentTabUrl(function(url) {
              renderStatus(url);
              var comment = document.getElementById('comment');
              console.log(comment.value);
              var data = {
                user_id: 1,
                url: url,
                comment: comment.value
              }
              submitComment(data);
            });
        });
  document.getElementById('receive_button').addEventListener('click',
	  function() { 
	      getCurrentTabUrl(function(url) {
		  var xhr = new XMLHttpRequest();
		  xhr.onreadystatechange = function() {
		      if (xhr.readyState == 4) {
			  var list = JSON.parse(xhr.responseText);
			  console.log(renderComments(commentify(list)));
			  
		      }
		      //renderComments(commentify(list));
		  }
		  var server = 'http://127.0.0.1:5000/comments?url=' + url;
		  xhr.open('GET',server);
		  xhr.setRequestHeader('Content-Type','text/html; charset=utf-8');
		  xhr.send(null);
	      });
	      //renderCommentsURL(getURL(list));
	      
	  });
});
