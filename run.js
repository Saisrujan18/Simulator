var {PythonShell} = require('python-shell')
var path = require("path");

function RUN()
{
	var x = document.getElementById("MIPS").value;
	var options = {
		scriptPath : path.join(__dirname, '/'),
		args : [x]
	}
	PythonShell.run('Start.py',options,function(err,message) {
		if  (err)  throw err;
    	console.log(message);
		if(message==null)
		{
			document.getElementById("console").innerHTML="Terminated due to errors";
		}
		else
		{
			document.getElementById("console").innerHTML="Success !!!";
		}
	});
}

function loadFileAsText()
{
    var fileToLoad = document.getElementById("fileToLoad").files[0];
    var fileReader = new FileReader();
    fileReader.onload = function(fileLoadedEvent)
    {
        var textFromFileLoaded = fileLoadedEvent.target.result;
        document.getElementById("MIPS").value = textFromFileLoaded;
    };
    fileReader.readAsText(fileToLoad, "UTF-8");
}