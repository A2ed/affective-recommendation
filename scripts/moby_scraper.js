var moby = require('moby');

//console.log(moby.search('sad'))

var dict, states;

dict = {};

states = ['groovy',
		  'adventurous',
		  'pensive',
		  'lonesome', 
		  'funky',
		  'belligerent',
		  'happy',
		  'sad',
		  'dapper',
		  'regretful',
		  'fabulous'];

states.forEach(function(item) {
	// populate dict with state/synonym key/value pairs
	dict[item] = moby.search(item)
});

// convert object to string
var data = JSON.stringify(dict);
// save file
var fs = require('fs');
fs.writeFile("emotion_ds.json", data, function(err){
 if (err) throw err;
  console.log("success");
}); 