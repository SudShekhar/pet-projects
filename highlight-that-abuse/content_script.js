chrome.storage.sync.get("highlight_abuse", function(data){
	if(data["highlight_abuse"] == "stop"){
	}
	else {
		walk(document.body, data["highlight_abuse"]);
	}
});
function walk(node, action)
{
	// I stole this function from here:
	// http://is.gd/mwZp7E
	
	var child, next;

	switch ( node.nodeType )
	{
		case 1:  // Element
		case 9:  // Document
		case 11: // Document fragment
			child = node.firstChild;
			while ( child )
			{
				next = child.nextSibling;
				walk(child, action);
				child = next;
			}
			break;

		case 3: // Text node
			handleText(node, action);
			break;
	}
}
RegExp.quote = function(str) {
     return str.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
};
String.prototype.repeat = function( num )
{
	    return new Array( num + 1 ).join( this );
};
function handleText(textNode, action)
{
	var v = textNode.nodeValue;
	if(action == "capitalize"){
		for(var key in data){
			var re = new RegExp("\\b"+key+"\\b","g");
			v = v.replace(re, key.toUpperCase());
		}
	}
	else if(action == "hide"){
		for(var key in data){
			var re = new RegExp("\\b"+key+"\\b", "g");
			v = v.replace(re, "*".repeat(key.length));
		}
	}
	else if(action == "alternate"){
		var charset = "^$#!@*";
		for(var key in data){
			var re = new RegExp("\\b"+key+"\\b","g");
			var replace = new Array();
			for(var i=0;i<key.length;i++){
				if(i&1)
					replace.push(charset[Math.floor(Math.random()*charset.length)]);
				else
					replace.push(key[i]);
			}
			v = v.replace(re, replace.join(""));
		}
	}
	else if(action == "meaning"){
		for(var key in data){
			var re = new RegExp("\\b"+key+"\\b","g");
			if(data[key]=="")
				data[key] = "No idea";
			v =v.replace(re,key+"("+data[key]+")");
		}
	}
	// Fix some misspellings
		// The Generation of €700
	textNode.nodeValue = v;
}
chrome.storage.sync.get("highlight_abuse", function(data){
		console.log("Status is "+data["highlight_abuse"]);
});
