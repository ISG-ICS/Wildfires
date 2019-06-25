import {Component, OnInit} from '@angular/core';
import 'leaflet/dist/leaflet.css';
import {latLng, tileLayer} from 'leaflet';
// import {$} from 'protractor';

declare let L;

@Component({
  selector: 'app-heatmap',
  templateUrl: './heatmap.component.html',
  styleUrls: ['./heatmap.component.css']
})
export class HeatmapComponent implements OnInit {

  constructor() {
  }


  // options = {
  //   layers: [
  //     // tslint:disable-next-line:max-line-length
  //     tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  //       attribution: '&copy; OpenStreetMap contributors'
  //     })
  //   ],
  //   zoom: 7,
  //   center: latLng([ 46.879966, -121.726909 ])
  // };

  ngOnInit() {
    // const map = L.map('map').setView([51.505, -0.09], 13);
    //
    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //   attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    // }).addTo(map);

    // for the base map layers


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
  }


}
