import {Component, EventEmitter, Input, OnInit} from '@angular/core';
import 'leaflet/dist/leaflet.css';
declare let L;
import * as $ from 'jquery';
import HeatmapOverlay from 'leaflet-heatmap/leaflet-heatmap.js';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-rain';

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
    this.mapService.getHeatmapData();
    this.mapService.heatmapDataLoaded.subscribe( this.heatmapDataHandler);

    // Get tweets data from service
    this.mapService.getTweetsData();
    this.mapService.tweetDataLoaded.subscribe(this.tweetDataHandler);

    // Get rainfall data from service
    this.mapService.getWildfirePredictionData();
    this.mapService.fireEventDataLoaded.subscribe( this.fireEventHandler);

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
      lngField: 'lng',
      valueField: 'temperature'
    };

    // Create heatmap overaly for temperature data with heatmap configuration
    const heatmapLayer = new HeatmapOverlay(heatmapConfig);
    heatmapLayer.setData(data.heatmapData);
    this.mainControl.addOverlay(heatmapLayer, 'Temperature');

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

    console.log(data);

    const birdCoordinates = [];

    data.data.forEach( (x) => {
      if (!this.liveTweetIdSet.has(x.id)) {
        const point = [x.lat, x.long];
        birdCoordinates.push([x.lat, x.long]);
        const marker = L.marker(point, {icon: birdIcon}).bindPopup('I am a live tweet');
        this.liveTweetBird.push(marker);
        this.liveTweetIdSet.add(x.id);
      }
    })

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
    for ( bird of birds) {
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

    for (let i = 0; i < data.fireEvents.length; i++) {
      const point = [data.fireEvents[i].lat, data.fireEvents[i].long];
      const size = 40;
      const fireIcon = L.icon({
        iconUrl: 'assets/image/pixelfire.gif',
        iconSize: [ size, size],
      });
      const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire(image>40%)');
      fireEventList.push(marker);

    }
    const fireEvents = L.layerGroup(fireEventList);
    this.mainControl.addOverlay(fireEvents, 'Fire event');
  }



}
