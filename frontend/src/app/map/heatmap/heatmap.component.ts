import {Component, OnInit} from '@angular/core';
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

  constructor(private mapService: MapService) {
  }



  ngOnInit() {
    const mbAttr = 'Credit to yc';
    const mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiY' +
      'SI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

    const satellite = L.tileLayer(mbUrl, {id: 'mapbox.satellite', attribution: mbAttr});
    const streets = L.tileLayer(mbUrl, {id: 'mapbox.streets', attribution: mbAttr});
    const dark = L.tileLayer(mbUrl, {id: 'mapbox.dark'});
    const map = L.map('map', {
      center: [33.64, -117.84],
      zoom: 5,
      layers: [satellite, streets, dark]
    });
    let tweetData = [];
    const baseLayers = {
      '<span style =\'color:blue\'>Satellite</span>': satellite,
      '<span style =\'color:red\'>Streets</span>': streets,
      '<span style =\'color:black\'>Dark</span>': dark
    };

    const mainControl = L.control.layers(baseLayers).addTo(map);

    // Coordinate

    map.addEventListener('mousemove', (ev) => {
      const lat = ev.latlng.lat;
      const lng = ev.latlng.lng;
      $('#mousePosition').html('Lat: ' + Math.round(lat * 100) / 100 + ' Lng: ' + Math.round(lng * 100) / 100);
    });

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
    // Request heatmap data from server
    this.mapService.getHeatmapData();
    // Cache heat data in the frontend
    $(window).on('heatDataLoaded', (event, data) => {
      heatmapLayer.setData(data);
      mainControl.addOverlay(heatmapLayer, 'Temperature');
    });
    // Tweets related layers
    const tweetLayer = L.TileLayer.maskCanvas({
        radius: 10,
        useAbsoluteRadius: true,
        color: '#000',
        opacity: 1,
        noMask: true,
        lineColor: '#e25822'
    });

    this.mapService.getTweetsData();

    let liveTweet = L.layerGroup();
    const liveTweetList = [];
    const htmlSelectElements = $(window).on('tweetsLoaded', (event, data) => {

      const tempData = [];
      tweetData = data.tweetData;
      data.tweetData.forEach(x => {
        tempData.push([x[0], x[1]]);
      });

      tweetLayer.setData(tempData);
      mainControl.addOverlay(tweetLayer, 'Fire tweet');

      const fireEventList = [];
      for (let i = 0; i < data.tweetData.length; i++) {
          if (i % 1000 === 0) {
            const point = [data.tweetData[i][0], data.tweetData[i][1]];
            const size = Math.floor(Math.random() * 80);
            const fireIcon = L.icon({
                iconUrl: 'assets/image/pixelfire.gif',
                iconSize:     [ size, size],
            });
            const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire');
            fireEventList.push(marker);
          }
      }

      const fireEvents = L.layerGroup(fireEventList);
      mainControl.addOverlay(fireEvents, 'Fire event');

      for (let i = 0; i < data.tweetData.length; i++) {
        if (i % 2000 === 0) {
          const point = [data.tweetData[i][0], data.tweetData[i][1]];
          const icon = L.icon({
              iconUrl: 'assets/image/perfectBird.gif',
              iconSize: [20, 20]
          });
          const marker = L.marker(point, {icon}).bindPopup('I am a live tweet');
          liveTweetList.push(marker);
        }
      }

      liveTweet = L.layerGroup(liveTweetList);
      $('.switch').css('display', 'inline-block');
    });

    const liveTweetLayer = L.TileLayer.maskCanvas({
      radius: 10,
      useAbsoluteRadius: true,
      color: '#000',
      opacity: 1,
      noMask: true,
      lineColor: '#e25822'
    });

    function liveTweetHandler(ev) {
      liveTweet.addTo(map);
      const temp = [];
      liveTweetList.forEach(x => {
          temp.push([x._latlng.lat, x._latlng.lng]);
      });

      liveTweetLayer.setData(temp);
      const birds = $('.leaflet-marker-icon');
      window.setTimeout(() => {
          liveTweet.clearLayers();
          liveTweet.addLayer(liveTweetLayer);
      }, 3200);
      let bird: any = 0;
      for ( bird of birds) {
        if (bird.src.indexOf('perfectBird') !== -1) {
          $(bird).css('animation', 'fly 3s linear');
        }
      }
    }

    $('#liveTweetSwitch').on('click', liveTweetHandler);


    const timeRangeHandler = (ev, data) => {
      const tempData = [];
      tweetData.forEach(entry => {
        if (entry[2] > data.timebarStart && entry[2] < data.timebarEnd) {
          tempData.push([entry[0], entry[1]]);
        }
      });
      tweetLayer.setData(tempData);
    };



    $(window).on('timeRangeChange', timeRangeHandler);
  }


}
