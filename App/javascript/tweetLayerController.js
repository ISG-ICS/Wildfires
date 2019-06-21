  //tweets in points
  var chartData = [];
  var tweetsPoint = [];
  var dailyCount = {};
  var tweetLayer = L.TileLayer.maskCanvas({
   radius: 10,  
   useAbsoluteRadius: true,  
   color: '#000',  
   opacity: 1,  
   noMask: true,  
   lineColor: '#e25822'
  });
  $(document).ready(function() {
    
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/tweets",
        dataType: "text",
        success: function(data) {
          
          var tempData = JSON.parse(data);
          var tweetData = [];
          tempData.forEach(function(entry){
            
            var createAt = entry["create_at"].split("T")[0];
            
            if(dailyCount.hasOwnProperty(createAt)){
              dailyCount[createAt]++;
            }
            else{
              dailyCount[createAt] = 1;
            }
            
            let leftTop = entry["place"]["bounding_box"][0];
            let bottomRight  = entry["place"]["bounding_box"][1];
            let center = [leftTop[0]+bottomRight[0]/2,leftTop[1]+bottomRight[1]/2];
            tweetData.push([leftTop[1],leftTop[0]]);
            tweetsPoint.push([new Date(createAt).getTime(),leftTop[1],leftTop[0]]);
            
          })
          

          
          //time bar

          Object.keys(dailyCount).sort().forEach(function(key){
            chartData.push([new Date(key).getTime(),dailyCount[key]]);

          });

                    
          tweetLayer.setData(tweetData);
          mainControl.addOverlay(tweetLayer,"fire tweet");
          $(window).trigger("tweetsLoaded",[]); 
        }
    });
    
    function timebarChangeHandler(){
      var tweetData = [];
      tweetsPoint.forEach(function(entry){
        if(entry[0]>timebarStart && entry[0]<timebarEnd){
          tweetData.push([entry[1],entry[2]]);
        }
      });
      tweetLayer.setData(tweetData);
    }
    
    $(window).on("timeRangeChange",timebarChangeHandler);
    
  });

//Live Tweet



$(window).on("tweetsLoaded",function(){
  
  var markerList = [];
  
  for(var i=0;i<tweetsPoint.length;i++){
   if(i%1000==0){
     var point = [tweetsPoint[i][1],tweetsPoint[i][2]];
     var size= Math.floor(Math.random()*80)
     var fireIcon = L.icon({
      iconUrl: 'image/pixelfire.gif',
      iconSize:     [ size, size],
    });
     var marker = L.marker(point,{icon:fireIcon}).bindPopup("I am a fire");
     markerList.push(marker);
     
   } 
  }
  
  var fireEvents = L.layerGroup(markerList);
  mainControl.addOverlay(fireEvents,"Fire event");
  
})




