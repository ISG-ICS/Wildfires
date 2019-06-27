import {Component, EventEmitter, Input, OnInit} from '@angular/core';
import 'leaflet/dist/leaflet.css';
declare let L;
import * as $ from 'jquery';
import HeatmapOverlay from 'leaflet-heatmap/leaflet-heatmap.js';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';

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
  private map;
  @Input() timeRangeChange;

  constructor(private mapService: MapService) {
  }

  ngOnInit() {
    const mbAttr = 'Credit to yc';
    const mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiY' +
      'SI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
    const satellite = L.tileLayer(mbUrl, {id: 'mapbox.satellite', attribution: mbAttr});
    const streets = L.tileLayer(mbUrl, {id: 'mapbox.streets', attribution: mbAttr});
    const dark = L.tileLayer(mbUrl, {id: 'mapbox.dark'});
    this.map = L.map('map', {
      center: [33.64, -117.84],
      zoom: 5,
      layers: [satellite, streets, dark]
    });
    const baseLayers = {
      '<span style =\'color:blue\'>Satellite</span>': satellite,
      '<span style =\'color:red\'>Streets</span>': streets,
      '<span style =\'color:black\'>Dark</span>': dark
    };

    this.mainControl = L.control.layers(baseLayers).addTo(this.map);

    // Coordinate
    this.map.addEventListener('mousemove', (ev) => {
      const lat = ev.latlng.lat;
      const lng = ev.latlng.lng;
      $('#mousePosition').html('Lat: ' + Math.round(lat * 100) / 100 + ' Lng: ' + Math.round(lng * 100) / 100);
    });

    this.mapService.getHeatmapData();
    // Cache heat data in the frontend
    this.mapService.heatmapDataLoaded.subscribe( this.heatmapDataHandler);

    this.mapService.getTweetsData();
    this.mapService.tweetDataLoaded.subscribe( this.tweetDataHandler);

    $('#liveTweetSwitch').on('click', this.liveTweetSwitchHandler);
    $(window).on('timeRangeChange', this.timeRangeChangeHandler);
  }

  tweetDataHandler = (data) => {

    // Tweets related layers
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

    // Mockup sampling data for fire events
    const fireEventList = [];

    for (let i = 0; i < data.tweetData.length; i++) {
      if (i % 1000 === 0) {
        const point = [data.tweetData[i][0], data.tweetData[i][1]];
        const size = Math.floor(Math.random() * 80);
        const fireIcon = L.icon({
          iconUrl: 'assets/image/pixelfire.gif',
          iconSize: [ size, size],
        });
        const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire');
        fireEventList.push(marker);
      }
    }

    const fireEvents = L.layerGroup(fireEventList);
    this.mainControl.addOverlay(fireEvents, 'Fire event');

    // Mockup Data for liveTweetLayer
    const birdIcon = L.icon({
      iconUrl: 'assets/image/perfectBird.gif',
      iconSize: [20, 20]
    });

    for (let i = 0; i < data.tweetData.length; i++) {
      if (i % 2000 === 0) {
        const point = [data.tweetData[i][0], data.tweetData[i][1]];
        const marker = L.marker(point, {icon: birdIcon}).bindPopup('I am a live tweet');
        this.liveTweetBird.push(marker);
      }
    }

    this.liveTweetLayer = L.layerGroup(this.liveTweetBird);
    // Show the live tweet switch when the layer is ready
    $('.switch').css('display', 'inline-block');

  }

  heatmapDataHandler = (data) => {
    const heatmapConfig = {
      // radius should be small ONLY if scaleRadius is true (or small radius is intended)
      // if scaleRadius is false it will be the constant radius used in pixels
      radius: 1,
      maxOpacity: 0.5,
      // scales the radius based on map zoom
      scaleRadius: true,
      // if set to false the heatmap uses the global maximum for colorization
      // if activated: uses the data maximum within the current map boundaries
      //   (there will always be a red spot with useLocalExtremas true)
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

    this.liveTweetMarkers = L.TileLayer.maskCanvas({
      radius: 10,
      useAbsoluteRadius: true,
      color: '#000',
      opacity: 1,
      noMask: true,
      lineColor: '#e25822'
    });

    this.liveTweetLayer.addTo(this.map);
    const birdCoordinates = [];
    this.liveTweetBird.forEach(x => {
      birdCoordinates.push([x._latlng.lat, x._latlng.lng]);
    });

    this.liveTweetMarkers.setData(birdCoordinates);
    const birds = $('.leaflet-marker-icon');
    window.setTimeout(() => {
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

  timeRangeChangeHandler = (event,data) => {
    const tempData = [];
    this.tweetData.forEach(entry => {
      if (entry[2] > data.timebarStart && entry[2] < data.timebarEnd) {
        tempData.push([entry[0], entry[1]]);
      }
    });
    this.tweetLayer.setData(tempData);
  }



}
