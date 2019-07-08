import {Component, OnInit} from '@angular/core';
import 'leaflet/dist/leaflet.css';

declare let L;
import * as $ from 'jquery';
import HeatmapOverlay from 'leaflet-heatmap/leaflet-heatmap.js';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import * as turf from '@turf/turf'

@Component({
  selector: 'app-heatmap',
  templateUrl: './heatmap.component.html',
  styleUrls: ['./heatmap.component.css']
})
export class HeatmapComponent implements OnInit {

  private mainControl;
  private tweetData;
  private tweetLayer;
  private liveTweetLayer;
  private liveTweetBird = [];
  private liveTweetMarkers;
  private liveTweetIdSet = new Set();
  private map;
  private switchStatus = 0;

  constructor(private mapService: MapService) {
  }

  ngOnInit() {
    // A hacky way to declare that
    const that = this;
    // Initialize map and 3 base layers
    const mapBoxUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiY' +
      'SI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
    const satellite = L.tileLayer(mapBoxUrl, {id: 'mapbox.satellite'});
    const streets = L.tileLayer(mapBoxUrl, {id: 'mapbox.streets'});
    const dark = L.tileLayer(mapBoxUrl, {id: 'mapbox.dark'});
    this.map = L.map('map', {
      center: [33.64, -117.84],
      zoom: 5,
      maxzoom: 22,
      layers: [satellite, streets, dark]
    });

    // Initialize base layer group
    const baseLayers = {
      '<span style =\'color:blue\'>Satellite</span>': satellite,
      '<span style =\'color:red\'>Streets</span>': streets,
      '<span style =\'color:black\'>Dark</span>': dark
    };

    this.mainControl = L.control.layers(baseLayers).addTo(this.map);

    this.mapService.mapLoaded.emit(this.map);
    // Generate coordinate in siderbar
    this.map.addEventListener('mousemove', (ev) => {
      const lat = ev.latlng.lat;
      const lng = ev.latlng.lng;
      $('#mousePosition').html('Lat: ' + Math.round(lat * 100) / 100 + ' Lng: ' + Math.round(lng * 100) / 100);
    });

    // Get heatmap data from service
    //this.mapService.getHeatmapData();
    //this.mapService.heatmapDataLoaded.subscribe(this.heatmapDataHandler);

    // Get my heatmap data from service
    this.mapService.getmyTempData();
    this.mapService.contourDataLoaded.subscribe( this.contourDataHandler);
    this.mapService.contourDataLoaded.subscribe( this.polygonDataHandler);
    this.mapService.contourDataLoaded.subscribe( this.heatmapDataHandler);
    //this.contourDataHandler()

    // Get tweets data from service
    this.mapService.getTweetsData();
    this.mapService.tweetDataLoaded.subscribe(this.tweetDataHandler);

    // Get rainfall data from service
    this.mapService.getWildfirePredictionData();
    this.mapService.fireEventDataLoaded.subscribe(this.fireEventHandler);

    // Get wind data from service
    this.mapService.getWindData();
    this.mapService.windDataLoaded.subscribe(this.windDataHandler);

    // Add event Listener to live tweet switch
    $('#liveTweetSwitch').on('click', this.liveTweetSwitchHandler);

    // Add event Listener when user specify a time range on time series
    $(window).on('timeRangeChange', this.timeRangeChangeHandler);
  }

  tweetDataHandler = (data) => {
    this.tweetLayer = L.TileLayer.maskCanvas({
      radius: 10,
      useAbsoluteRadius: true,
      color: '#000',
      opacity: 1,
      noMask: true,
      lineColor: '#e25822'
    });
    const tempData = [];
    this.tweetData = data.tweetData;
    data.tweetData.forEach(x => {
      tempData.push([x[0], x[1]]);
    });

    this.tweetLayer.setData(tempData);
    this.mainControl.addOverlay(this.tweetLayer, 'Fire tweet');

  }

  heatmapDataHandler = (data) => {
    const heatmapConfig = {
      radius: 1,
      maxOpacity: 0.5,
      scaleRadius: true,
      useLocalExtrema: true,
      latField: 'lat',
      lngField: 'long',
      valueField: 'temp'
    };
    console.log(data);
    // Create heatmap overaly for temperature data with heatmap configuration
    const heatmapLayer = new HeatmapOverlay(heatmapConfig);
    heatmapLayer.setData({max: null,data:data.contourData});
    this.mainControl.addOverlay(heatmapLayer, 'Temp heatmap');

  }

  liveTweetSwitchHandler = (event) => {
    if (this.switchStatus === 1) {
      this.liveTweetLayer.clearLayers();
      this.mapService.stopliveTweet();
      this.switchStatus = 0;
      return;
    }
    this.mapService.getLiveTweetData();
    this.mapService.liveTweetLoaded.subscribe(this.liveTweetDataHandler);
    this.switchStatus = 1;
  }

  liveTweetDataHandler = (data) => {
    this.liveTweetMarkers = L.TileLayer.maskCanvas({
      radius: 10,
      useAbsoluteRadius: true,
      color: '#000',
      opacity: 1,
      noMask: true,
      lineColor: '#e25822'
    });

    // Mockup Data for liveTweetLayer
    const birdIcon = L.icon({
      iconUrl: 'assets/image/perfectBird.gif',
      iconSize: [20, 20]
    });

    const birdCoordinates = [];

    data.data.forEach((tweet) => {
      if (!this.liveTweetIdSet.has(tweet.id)) {
        const point = [tweet.lat, tweet.long];
        birdCoordinates.push([tweet.lat, tweet.long]);
        const marker = L.marker(point, {icon: birdIcon}).bindPopup('I am a live tweet');
        this.liveTweetBird.push(marker);
        this.liveTweetIdSet.add(tweet.id);
      }
    });

    this.liveTweetLayer = L.layerGroup(this.liveTweetBird);
    this.liveTweetLayer.addTo(this.map);


    this.liveTweetMarkers.setData(birdCoordinates);
    const birds = $('.leaflet-marker-icon');
    window.setTimeout(() => {
      this.liveTweetBird = [];
      this.liveTweetLayer.clearLayers();
      this.liveTweetLayer.addLayer(this.liveTweetMarkers);
    }, 3200);
    let bird: any = 0;
    for (bird of birds) {
      if (bird.src.indexOf('perfectBird') !== -1) {
        $(bird).css('animation', 'fly 3s linear');
      }
    }
  }

  timeRangeChangeHandler = (event, data) => {
    const tempData = [];
    this.tweetData.forEach(entry => {
      if (entry[2] > data.timebarStart && entry[2] < data.timebarEnd) {
        tempData.push([entry[0], entry[1]]);
      }
    });
    this.tweetLayer.setData(tempData);
  }

  fireEventHandler = (data) => {

    const fireEventList = [];

    for (const ev of  data.fireEvents) {
      const point = [ev.lat, ev.long];
      const size = 40;
      const fireIcon = L.icon({
        iconUrl: 'assets/image/pixelfire.gif',
        iconSize: [size, size],
      });
      const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire(image>40%)');
      fireEventList.push(marker);

    }
    const fireEvents = L.layerGroup(fireEventList);
    this.mainControl.addOverlay(fireEvents, 'Fire event');
  }

  contourDataHandler = (data) => {
      let tempPointsList = [];
      for (let points of data.contourData){
        const tempPoint = turf.point([points.long, points.lat], {'temperature':points.temp});
        tempPointsList.push(tempPoint);
      }
      //console.log(tempPointsList);
      //const pointGrid = turf.featureCollection(tempPointsList)
      const tempFeatures = turf.featureCollection(tempPointsList);
      const pointGrid = turf.explode(tempFeatures);
      const breaks = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31];
      //const breaks = [0.08, 0.09, 0.10, 0.11, 0.12];
      let lines = turf.isolines(pointGrid, breaks, { zProperty: 'temperature' });
      //console.log(lines)

      var _lFeatures = lines.features;
      for(var i=0;i<_lFeatures.length;i++){
          var _coords = _lFeatures[i].geometry.coordinates;
          var _lCoords = [];
          for(var j=0;j<_coords.length;j++){
                                  var _coord = _coords[j];
                                  var line = turf.lineString(_coord);
                                  var curved = turf.bezierSpline(line);
                                  _lCoords.push(curved.geometry.coordinates);
                              }
          _lFeatures[i].geometry.coordinates = _lCoords;
      }

      const region = L.geoJSON(lines, {style: {color: '#49ebd8', weight: 1.8 ,opacity: 0.5}}).addTo(this.map);
      this.map.fitBounds(region.getBounds());


  }

  polygonDataHandler  = (data) => {
    let my = data.contourData;
    let all_latlng = []
    for (let t = 17; t < 32; t++) {
      //console.log(my[i].lat);
      let latlng_list = [];
      for (let i = 0; i < my.length; i++) {
        if (my[i].temp >= t && my[i].temp <= t + 1) {
          latlng_list.push([Number(my[i].lat), Number(my[i].long)]);
        }
      }
      all_latlng.push(latlng_list)


    }
      console.log(all_latlng);
      let points17 = [];
      for (let i of all_latlng[0]) {
        const points1 = L.circle(i, {
          color: '#393fb8',
          fillColor: '#393fb8',
          fillOpacity: 1
        })
        points17.push(points1);
      }
      const temp_plot17 = L.layerGroup(points17);
      this.mainControl.addOverlay(temp_plot17, 'blue-17C');


      let points18 = [];
      for (let i of all_latlng[1]) {
        const points1 = L.circle(i, {
          color: '#45afd6',
          fillColor: '#45afd6',
          fillOpacity: 1
        })
        points18.push(points1);
      }
      const temp_plot18 = L.layerGroup(points18);
      this.mainControl.addOverlay(temp_plot18, 'lightblue-18C');

      let points19 = [];
      for (let i of all_latlng[2]) {
        const points1 = L.circle(i, {
          color: '#49ebd8',
          fillColor: '#49ebd8',
          fillOpacity: 1
        });
        points19.push(points1);
      }
      const temp_plot19 = L.layerGroup(points19);
      this.mainControl.addOverlay(temp_plot19, 'greenblue-19C');

      let points20 = [];
      for (let i of all_latlng[3]) {
        const points1 = L.circle(i, {
          color: '#49eb8f',
          fillColor: '#49eb8f',
          fillOpacity: 1
        });
        points20.push(points1);
      }
      const temp_plot20 = L.layerGroup(points20);
      this.mainControl.addOverlay(temp_plot20, 'green-20C');

      let points21 = [];
      for (let i of all_latlng[4]) {
        const points1 = L.circle(i, {
          color: '#a6e34b',
          fillColor: '#a6e34b',
          fillOpacity: 1
        });
        points21.push(points1);
      }
      const temp_plot21 = L.layerGroup(points21);
      this.mainControl.addOverlay(temp_plot21, 'lightgreen-21C');


      let points22 = []
      for (let i of all_latlng[5]) {
        const points1 = L.circle(i, {
          color: '#f2de5a',
          fillColor: '#f2de5a',
          fillOpacity: 1
        })//.addTo(this.map);
        points22.push(points1)
      }
      const temp_plot22 = L.layerGroup(points22);
      this.mainControl.addOverlay(temp_plot22, 'yellow-22C');

      let points23 = []
      for (let i of all_latlng[6]) {
        const points1 = L.circle(i, {
          color: '#edbf18',
          fillColor: '#edbf18',
          fillOpacity: 1
        })
        points23.push(points1)
      }
      const temp_plot23 = L.layerGroup(points23);
      this.mainControl.addOverlay(temp_plot23, 'darkyellow-23C');

      let points24 = []
      for (let i of all_latlng[7]) {
        const points1 = L.circle(i, {
          color: '#e89c20',
          fillColor: '#e89c20',
          fillOpacity: 1
        })
        points24.push(points1)
      }
      const temp_plot24 = L.layerGroup(points24);
      this.mainControl.addOverlay(temp_plot24, 'lightorange-24C');

      let points25 = []
      for (let i of all_latlng[8]) {
        const points1 = L.circle(i, {
          color: '#f27f02',
          fillColor: '#f27f02',
          fillOpacity: 1
        })
        points25.push(points1)
      }
      const temp_plot25 = L.layerGroup(points25);
      this.mainControl.addOverlay(temp_plot25, 'orange-25C');

      let points26 = []
      for (let i of all_latlng[9]) {
        const points1 = L.circle(i, {
          color: '#f25a02',
          fillColor: '#f25a02',
          fillOpacity: 1
        })
        points26.push(points1)
      }
      const temp_plot26 = L.layerGroup(points26);
      this.mainControl.addOverlay(temp_plot26, 'richorange-26C');

      let points27 = []
      for (let i of all_latlng[10]) {
        const points1 = L.circle(i, {
          color: '#f23a02',
          fillColor: '#f23a02',
          fillOpacity: 1
        })
        points27.push(points1)
      }
      const temp_plot27 = L.layerGroup(points27);
      this.mainControl.addOverlay(temp_plot27, 'red-27C');

      let points28 = []
      for (let i of all_latlng[11]) {
        const points1 = L.circle(i, {
          color: '#f0077f',
          fillColor: '#f0077f',
          fillOpacity: 1
        })
        points28.push(points1)
      }
      const temp_plot28 = L.layerGroup(points28);
      this.mainControl.addOverlay(temp_plot28, 'purplered-28C');

      let points29 = []
      for (let i of all_latlng[12]) {
        const points1 = L.circle(i, {
          color: '#f205c3',
          fillColor: '#f205c3',
          fillOpacity: 1
        })
        points29.push(points1)
      }
      const temp_plot29 = L.layerGroup(points29);
      this.mainControl.addOverlay(temp_plot29, 'lightpurple-29C');

      let points30 = []
      for (let i of all_latlng[13]) {
        const points1 = L.circle(i, {
          color: '#9306ba',
          fillColor: '#9306ba',
          fillOpacity: 1
        })
        points30.push(points1)
      }
      const temp_plot30 = L.layerGroup(points30);
      this.mainControl.addOverlay(temp_plot30, 'purple-30C');

      /*
      const polyline0 = L.polyline(all_latlng[0], {color: 'blue', smoothFactor: 1, opacity: 0.3 }).addTo(this.map);
      this.map.fitBounds(polyline0.getBounds());
      const polyline1 = L.polyline(all_latlng[1], {color: 'green', smoothFactor: 1, opacity: 0.3 }).addTo(this.map);
      this.map.fitBounds(polyline1.getBounds());
      const polyline2 = L.polyline(all_latlng[2], {color: 'yellow', smoothFactor: 1, opacity: 0.3 }).addTo(this.map);
      this.map.fitBounds(polyline2.getBounds());
      const polyline3 = L.polyline(all_latlng[3], {color: 'orange', smoothFactor: 1, opacity: 0.3 }).addTo(this.map);
      this.map.fitBounds(polyline3.getBounds());
      const polyline4 = L.polyline(all_latlng[4], {color: 'red', smoothFactor: 1, opacity: 0.3 }).addTo(this.map);
      this.map.fitBounds(polyline4.getBounds());
       */

  }




  windDataHandler = (wind) => {
    // there's not much document about leaflet-velocity.
    // all we got is an example usage from
    // github.com/0nza1101/leaflet-velocity-ts
    const velocityLayer = L.velocityLayer({
      displayValues: true,
      displayOptions: {
        position: 'bottomleft', // REQUIRED !
        emptyString: 'No velocity data', // REQUIRED !
        angleConvention: 'bearingCW', // REQUIRED !
        velocityType: 'Global Wind',
        displayPosition: 'bottomleft',
        displayEmptyString: 'No wind data',
        speedUnit: 'm/s'
      },
      data: wind.data,
      maxVelocity: 12 // affect color and animation speed of wind
    });
    this.mainControl.addOverlay(velocityLayer, 'Global wind');
  }

}
