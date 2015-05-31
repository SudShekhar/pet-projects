var x = true;
chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	chrome.tabs.sendMessage(tabs[0].id, {greeting: "start"}, function(response) {});
});

function updateState(tab){
    if(x==false){
        x=true;
		chrome.browserAction.setIcon({path:"favicon.ico",tabId:tab.id});
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	  		chrome.tabs.sendMessage(tabs[0].id, {greeting: "start"}, function(response) {});
		});

    }else{
        x=false;
		chrome.browserAction.setIcon({path:"stop_favicon.ico",tabId:tab.id});
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	  		chrome.tabs.sendMessage(tabs[0].id, {greeting: "end"}, function(response) {});
		});
    }
};

chrome.browserAction.onClicked.addListener(updateState);
/*chrome.browserAction.onClicked.addListener(function(tab) {
	    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	  		chrome.tabs.sendMessage(tabs[0].id, {greeting: "start"}, function(response) {});
		});

});*/
