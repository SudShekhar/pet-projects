alert("Hello");
var disable=1;
var myFunction = function(){$('div[class="pagedlist_item"]:has(div:contains("Top content on Quora"))').hide();};
if(disable==1)
	var timer = setInterval(myFunction, 500);
else
	clearTimeout(timer);
