var heatmapConfig = {
  // radius should be small ONLY if scaleRadius is true (or small radius is intended)
  // if scaleRadius is false it will be the constant radius used in pixels
  "radius": 1,
  "maxOpacity": 0.5, 
  // scales the radius based on map zoom
  "scaleRadius": true, 
  // if set to false the heatmap uses the global maximum for colorization
  // if activated: uses the data maximum within the current map boundaries 
  //   (there will always be a red spot with useLocalExtremas true)
  "useLocalExtrema": true,
  // which field name in your data represents the latitude - default "lat"
  latField: 'lat',
  // which field name in your data represents the longitude - default "lng"
  lngField: 'lng',
  // which field name in your data represents the data value - default "value"
  valueField: 'temperature'
};

var heatmapLayer = new HeatmapOverlay(heatmapConfig);
var heatData = {};

$(document).ready(function() {
  $.ajax({
      type: "GET",
      url: "http://127.0.0.1:5000/temp",
      dataType: "text",
      success: function(data) {
        var tempData = processCSVData(data,60000);
        var tempDataArray = [];
        var coorSet = new Set();
        var dailyCount = {};
        for(var i=0; i<tempData.length; i++){
          var entry = tempData[i];
          var createAt = entry[6];

          if(dailyCount.hasOwnProperty(createAt)){
            dailyCount[createAt] = entry[8];
          }
          else{
            dailyCount[createAt] = entry[8];
          }
          if(!coorSet.has(entry[3]+entry[4])){
            tempDataArray.push({lat:entry[3],lng:entry[4],temperature:entry[8]});
          }
          var station = entry[3]+entry[4];
          coorSet.add(station);
          if(heatData.hasOwnProperty(station)){
            heatData[station].push([new Date(createAt).getTime(),parseFloat(entry[8])]);
          }
          else{
            heatData[station] = [[new Date(createAt).getTime(),parseFloat(entry[8])]];
          }
          
        }

        var testData = {
          max:8,
          data:tempDataArray
        };

        $(window).trigger("heatDataLoaded",[]);
        heatmapLayer.setData(testData);
        mainControl.addOverlay(heatmapLayer,"Temperature");
      }
   });
});