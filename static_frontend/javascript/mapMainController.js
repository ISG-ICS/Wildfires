  // for the base map layers

	var mbAttr = 'Credit to yc',
		mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

  var satellite = L.tileLayer(mbUrl, {id: 'mapbox.satellite', attribution: mbAttr});
  var streets = L.tileLayer(mbUrl, {id: 'mapbox.streets', attribution: mbAttr});
  var dark = L.tileLayer(mbUrl, {id: 'mapbox.dark'});
  var currentLayer = "wildfire tweet";
  var timebarStart = 0;
  var timebarEnd = 0;
	var map = L.map('map', {
		center: [33.64, -117.84],
		zoom: 5,
		layers: [satellite,streets,dark]
	});

	var baseLayers = {
		"<span style ='color:blue'>Satellite</span>": satellite,
		"<span style ='color:red'>Streets</span>": streets,
    "<span style ='color:black'>Dark</span>":dark
	};

            
     
  var mainControl = L.control.layers(baseLayers).addTo(map);
  
  //Coordinate
  
  map.addEventListener('mousemove', function(ev) {
       lat = ev.latlng.lat;
       lng = ev.latlng.lng;
       $("#mousePosition").html("Lat: "+Math.round(lat*100)/100+" Lng: "+Math.round(lng*100)/100);
  });
   
  var liveTweetLayer = L.TileLayer.maskCanvas({
   radius: 10,  
   useAbsoluteRadius: true,  
   color: '#000',  
   opacity: 1,  
   noMask: true,  
   lineColor: '#e25822'
  });

  //Overlay event listener
  var addOverlayHandler = function(event){
  };

  map.on('overlayadd',addOverlayHandler);