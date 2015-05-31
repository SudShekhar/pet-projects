document.addEventListener('DOMContentLoaded', function(){
	var input = document.getElementById('story-block');
	chrome.storage.sync.get('block_stories', function(data){
		if (data["block_stories"]){
			input.checked=true;
		}else{
			input.checked = false;
		}
	});
	input.addEventListener("change",function(){
		chrome.storage.sync.set({block_stories:input.checked});
	});
});
