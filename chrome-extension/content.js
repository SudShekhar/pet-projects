var timer;
function fun(){
	chrome.storage.sync.get("block_stories", function(data){
		if(data["block_stories"]){
			$('div[class="pagedlist_item"]:has(div:contains("Top content on Quora"))').hide();
		}
	});
}
var scrollfun= _.debounce(fun, 50);
document.addEventListener("scroll", scrollfun);
