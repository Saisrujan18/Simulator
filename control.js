function loadFileAsText()
{
    var fileToLoad = document.getElementById("fileToLoad").files[0];
  
    var fileReader = new FileReader();
    fileReader.onload = function(fileLoadedEvent)
    {
        var textFromFileLoaded = fileLoadedEvent.target.result;
        console.log(textFromFileLoaded);
        document.getElementById("MIPS").value = textFromFileLoaded;
    };
    fileReader.readAsText(fileToLoad, "UTF-8");
}