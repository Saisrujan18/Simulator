var {PythonShell} = require('python-shell')
var path = require("path");
const { brotliCompress } = require('zlib');
const { measureMemory } = require('vm');
const { memoryUsage } = require('process');

function RUN()
{
	var x = document.getElementById("MIPS").value;
	var regValue = []
	for(let i = 0;i<30;i++){
		regValue.push("0");
	}	
	var options = {
		scriptPath : path.join(__dirname, '/'),
		args : [x]
	}
	PythonShell.run('Start.py',options,function(err,message) {
		if  (err)  throw err;
    	
		console.log(message);
		if(message){
			for(let i=0;i<30;i++){
				regValue[i] = message[i]  
			}
			var memory = document.getElementById("MEMORY")
			while(memory.lastElementChild) {
				memory.removeChild(memory.lastElementChild)	
			}
			var memoryHeader = document.createElement("h4")
			memoryHeader.innerHTML = "MEMORY"
			memory.appendChild(memoryHeader)
			for(let i = 30;i<message.length;i++){
				var memAddress = message[i].split(':')[0]
				var memValue = message[i].split(':')[1]
				var memoryLocationWrapper = document.createElement("div")
				memoryLocationWrapper.classList.add('memwrapper')
				var memoryLocationAddress = document.createElement("div")
				memoryLocationAddress.classList.add("memadd")
				memoryLocationAddress.innerHTML = memAddress
				var memoryLocationValue = document.createElement("div")
				memoryLocationValue.classList.add("memvalue")
				memoryLocationValue.innerHTML = memValue
				memoryLocationWrapper.appendChild(memoryLocationAddress) 
				memoryLocationWrapper.appendChild(memoryLocationValue)
				memory.appendChild(memoryLocationWrapper)
			}
		}

		for(let i=0;i<30;i++){
			var register = document.getElementById(`${i}v`);
			register.innerHTML = ` ${regValue[i]} `; // format
		}
		
		if(!message){document.getElementById("console").innerHTML="Terminated due to errors";}
		else {document.getElementById("console").innerHTML="Success !!!";}
		
		// // document.getElementById("Register")="<p>hell</p><p>hell></p>";
		// var tag = document.createElement("p");
   		// var text = document.createTextNode("Tutorix");
   		// tag.appendChild(text);
		// var tag1 = document.createElement("p");
   		// var t1ext = document.createTextNode("orix");
   		// tag1.appendChild(t1ext);
   		// var element = document.getElementById("REGISTERS");
   		// element.appendChild(tag);
   		// element.appendChild(tag1);
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