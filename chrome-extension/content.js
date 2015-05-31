var timer;
var func = function(){$('div[class="pagedlist_item"]:has(div:contains("Top content on Quora"))').hide();};

chrome.runtime.onMessage.addListener(
		  function(request, sender, sendResponse) {
			console.log("In content "+request.greeting);
				if (request.greeting == "start"){
	      			timer = setInterval(func, 10000);
				}
				else{
					clearTimeout(timer);
				}
				sendResponse({greeting:"Done"});
});
