var x = true;
disableTopStories();
function disableTopStories(){
   chrome.tabs.executeScript(null, {code: '$(\'div[class="pagedlist_item"]:has(div:contains("Top content on Quora"))\').hide();'})
	};

function enableTopStories(){
   chrome.tabs.executeScript(null, {code: '$(\'div[class="pagedlist_item"]:has(div:contains("Top content on Quora"))\').hide();'})
};

function updateState(){
    if(x==false){
        x=true;
        disableTopStories();
    }else{
        x=false;
        enableTopStories();
    }
};

chrome.browserAction.onClicked.addListener(updateState);
