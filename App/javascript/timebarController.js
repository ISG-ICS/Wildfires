$(window).on("tweetsLoaded",function(ev){
  chart = Highcharts.chart('timebar-container', {
    chart:{
      type:"line",
      zoomType: 'x',
      height:200,
      backgroundColor: null,
      events:{
        selection:function(event){
          if(event.hasOwnProperty("xAxis")){
            timebarStart = event["xAxis"][0]["min"];
            timebarEnd = event["xAxis"][0]["max"];
          }
          else{
            timebarStart = event["target"]["axes"][0]["dataMin"];
            timebarEnd = event["target"]["axes"][0]["dataMax"];    
          }
          $(window).trigger("timeRangeChange",[]);
          
        }
      }
    },
    title: {
        text: currentLayer
    },
    xAxis: {
        type:"datetime",
    },
    series: [{
        data: chartData,
        color:"#e25822",
        label:"wildfire tweets"
    }]

  });  
});
                          
