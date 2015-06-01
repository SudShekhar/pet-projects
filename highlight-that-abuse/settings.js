document.addEventListener('DOMContentLoaded', function(){
	chrome.storage.sync.get('highlight_abuse', function(data){
		if(data["highlight_abuse"]==""){
			chrome.storage.sync.set({highlight_abuse:"capitalize"});
			data["highlight_abuse"] = "stop";
		}
		var radioBtn = document.getElementById(data["highlight_abuse"]);
		radioBtn.checked=true;
	});
	$("input[type=radio]").click(function(){
		chrome.storage.sync.set({highlight_abuse:this.value});
	});
});
