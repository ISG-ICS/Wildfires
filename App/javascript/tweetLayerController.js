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

          let leftTop = [entry["lat"],entry["long"]];
          tweetData.push(leftTop);
          tweetsPoint.push([new Date(createAt).getTime(),leftTop[0],leftTop[1]]);

        })



        //time bar

        Object.keys(dailyCount).sort().forEach(function(key){
          chartData.push([new Date(key).getTime(),dailyCount[key]]);

        });


        tweetLayer.setData(tweetData);
        mainControl.addOverlay(tweetLayer,"Fire tweet");
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



var liveTweet = {};
var liveTweetList = [];
$(window).on("tweetsLoaded",function(){
  
  var fireEventList = [];
  
  for(var i=0;i<tweetsPoint.length;i++){
   if(i%1000 === 0){
     var point = [tweetsPoint[i][1],tweetsPoint[i][2]];
     var size= Math.floor(Math.random()*80)
     var fireIcon = L.icon({
      iconUrl: 'image/pixelfire.gif',
      iconSize:     [ size, size],
    });
     var marker = L.marker(point,{icon:fireIcon}).bindPopup("I am a fire");
     fireEventList.push(marker);
     
   } 
  }
  
  var fireEvents = L.layerGroup(fireEventList);
  mainControl.addOverlay(fireEvents,"Fire event");
  
  for(var i=0;i<tweetsPoint.length;i++){
    if(i%2000 === 0){
      var point = [tweetsPoint[i][1],tweetsPoint[i][2]];
      var icon = L.icon({
        iconUrl:"image/perfectBird.gif",
        iconSize: [20,20]
      });
      var marker = L.marker(point,{icon:icon}).bindPopup("I am a live tweet");
      liveTweetList.push(marker);
    }
  }

  liveTweet = L.layerGroup(liveTweetList);
  $(".switch").css("display","inline-block");
})

function liveTweetHandler(ev){
  liveTweet.addTo(map);
  var temp = []
  liveTweetList.forEach(function(x){
    temp.push([x._latlng["lat"],x._latlng["lng"]])
  });

  liveTweetLayer.setData(temp);
  var birds = $(".leaflet-marker-icon");
  window.setTimeout(function(){
    liveTweet.clearLayers();
    liveTweet.addLayer(liveTweetLayer);
  },3200)
  for(var i=0;i<birds.length;i++){
    if(birds[i].src.indexOf("perfectBird") !== -1){
      $(birds[i]).css("animation","fly 3s linear");
    }
  }
}

$("#liveTweetSwitch").on("click",liveTweetHandler);



