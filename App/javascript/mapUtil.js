  // for the temperature overlays 
  
  function processCSVData(allText,limit,delim=",") {
    var allTextLines = allText.split(/\r\n|\n/);
    var matrix = []
    for(var i=1; i<allTextLines.length && i<=limit;i++){
      var s = allTextLines[i];
      var tempEntry = s.split(delim);
      var entry = [];
      for(var j=0;j<tempEntry.length;j++){
        if(tempEntry[j] !== ""){
          entry.push(tempEntry[j]);
        }
      }
      matrix.push(entry);  
    }
    return matrix;
  }