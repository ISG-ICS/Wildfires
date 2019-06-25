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
    const currentLayer = 'wildfire tweet';
    const timebarStart = 0;
    const timebarEnd = 0;
    const map = L.map('map', {
      center: [33.64, -117.84],
      zoom: 5,
      layers: [satellite, streets, dark]
    });

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
      // $('#mousePosition').html('Lat: ' + Math.round(lat * 100) / 100 + ' Lng: ' + Math.round(lng * 100) / 100);
    });

    // Overlay event listener
    const addOverlayHandler = (event) => {
      if (event.name === 'fire tweet') {
      }
    };

    map.on('overlayadd', addOverlayHandler);


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
      mainControl.addOverlay(heatmapLayer, 'temperature');
    });

    const tweetLayer = L.TileLayer.maskCanvas({
        radius: 10,
        useAbsoluteRadius: true,
        color: '#000',
        opacity: 1,
        noMask: true,
        lineColor: '#e25822'
    });

    // Request tweets data from server
    this.mapService.getTweetsData();

    $(window).on('tweetsLoaded', (event, data) => {
        tweetLayer.setData(data.tweetData);
        mainControl.addOverlay(tweetLayer, 'Fire tweet');
    });


  }


}
