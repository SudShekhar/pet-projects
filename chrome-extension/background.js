/*var x = true;
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

chrome.runtime.onInstalled.addListener(function(details){
	chrome.storage.sync.set({block_stories : true});
});

chrome.tabs.onUpdated.addListener(function(id,info,tab){
	if(tab.url.toLowerCase().indexOf("quora.com") > -1){
		chrome.pageAction.show(tab.id);
		chrome.pageAction.setIcon({path:"favicon.ico",tabId:tab.id});
	}
});

chrome.storage.onChanged.addListener(function(changes, areaName){
	chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
		var tab = tabs[0];
		if(tab.url.toLowerCase().indexOf("quora.com") > -1){
			alert("changed settings");
			chrome.storage.sync.get("block_stories", function(data){
				if(data["block_stories"])
					chrome.pageAction.setIcon({path:"favicon.ico",tabId:tab.id});
				else 
					chrome.pageAction.setIcon({path:"stop_favicon.ico",tabId:tab.id});
			});
		}
	});
});
