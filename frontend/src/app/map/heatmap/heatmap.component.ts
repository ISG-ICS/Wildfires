import {Component, OnInit} from '@angular/core';
import 'leaflet/dist/leaflet.css';

declare let L;
import * as $ from 'jquery';
import HeatmapOverlay from 'leaflet-heatmap/leaflet-heatmap.js';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import * as turf from '@turf/turf'
import {statesData} from '../../../../../data/boundaries/us-states.js';
import {citiesData} from '../../../../../data/boundaries/us-cities.js';



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

    // Set up for a range and each smaller interval of temp to give specific color layers
    private tempLayers = [];
    private tempLayer1;
    private tempBreaks = [-6, -3, 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36];

    // For temp range selector store current max/min selected by user
    private tempRegionsMax = [];
    private tempMax = [0];
    private tempMin = [0];
    private geojson;

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

        // Get temperature data from service
        this.mapService.getTemperatureData();
        this.mapService.contourDataLoaded.subscribe(this.contourDataHandler);
        this.mapService.contourDataLoaded.subscribe(this.polygonDataHandler);
        this.mapService.contourDataLoaded.subscribe(this.heatmapDataHandler);
        //this.mapService.contourDataLoaded.subscribe(this.ChoroplethDataHandler);

        // Send temp range selected from service
        this.mapService.temperatureChangeEvent.subscribe(this.rangeSelectHandler);

        // Get tweets data from service
        this.mapService.getTweetsData();
        this.mapService.tweetDataLoaded.subscribe(this.tweetDataHandler);

        // Get fire events data from service
        this.mapService.getWildfirePredictionData();
        this.mapService.fireEventDataLoaded.subscribe(this.fireEventHandler);

        // Get wind data from service
        this.mapService.getWindData();
        this.mapService.windDataLoaded.subscribe(this.windDataHandler);

        //this.ChoroplethDataHandler();
        //this.CityDataHandler();
        this.geojson = L.geoJson(citiesData, {
               style: this.style,
               onEachFeature: this.onEachFeature
           }).addTo(this.map);



        // Add event Listener to live tweet switch
        $('#liveTweetSwitch').on('click', this.liveTweetSwitchHandler);

        // Add event Listener when user specify a time range on time series
        $(window).on('timeRangeChange', this.timeRangeChangeHandler);
  // Add event Listener when user specify a temperature range on temp series
        $(window).on('tempRangeChange', this.tempRangeChangeHandler);
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


    heatmapDataHandler = (data) => {
        // use heatmapOverlay from leaflet-heatmap
        // Documentation for details in change of custom parameter
        // https://www.patrick-wied.at/static/heatmapjs/docs.html#heatmap-setData
        const heatmapConfig = {
            radius: 1,
            maxOpacity: 0.63,
            minOpacity: 0.2,
            scaleRadius: true,
            useLocalExtrema: false,
            blur: 1,
            latField: 'lat',
            lngField: 'long',
            valueField: 'temp',
            // gradient is customized to match the color scales of temp plotting layers exactly the same
            gradient: {
                '.1': '#393fb8',
                '.2': '#45afd6',
                '.3': '#49ebd8',
                '.4': '#49eb8f',
                '.5': '#a6e34b',
                '.55': '#f2de5a',
                '.6': '#edbf18',
                '.65': '#e89c20',
                '.7': '#f27f02',
                '.75': '#f25a02',
                '.8': '#f23a02',
                '.85': '#f0077f',
                '.9': '#f205c3',
                '.99': '#9306ba',
            }
        };
        const heatmapLayer = new HeatmapOverlay(heatmapConfig);
        heatmapLayer.setData({max: 680, data: data.contourData});
        this.mainControl.addOverlay(heatmapLayer, 'Temp heatmap');
    }


    contourDataHandler = (data) => {
        // used turf built in features to add contour lines,
        // but contour lines can only built on ractangled data size boundary
        let tempPointsList = [];
        for (let points of data.contourData) {
            const tempPoint = turf.point([points.long, points.lat], {'temperature': points.temp});
            tempPointsList.push(tempPoint);
        }
        // Establish features and break points for contour lines
        const tempFeatures = turf.featureCollection(tempPointsList);
        const pointGrid = turf.explode(tempFeatures);
        const lines = turf.isolines(pointGrid, this.tempBreaks, {zProperty: 'temperature'});
        // Make contour lines smooth
        const _lFeatures = lines.features;
        for (let i = 0; i < _lFeatures.length; i++) {
            const _coords = _lFeatures[i].geometry.coordinates;
            const _lCoords = [];
            for (let j = 0; j < _coords.length; j++) {
                const _coord = _coords[j];
                const line = turf.lineString(_coord);
                const curved = turf.bezierSpline(line);
                _lCoords.push(curved.geometry.coordinates);
            }
            _lFeatures[i].geometry.coordinates = _lCoords;
        }
        // Give colors from light to dark for different temperature
        const tempEvents = [];
        for (let index = 0; index < lines.features.length; index++) {
            const colorCode = Math.floor(200 * (index + 1) / this.tempBreaks.length + 55);
            tempEvents.push(L.geoJSON(lines.features[index], {
                style: {
                    color: 'rgb(0, ' + colorCode + ', ' + colorCode + ')',
                    weight: 1,
                    opacity: 0.4
                }
            }));
        }
        // Add the contour layer to the map
        const region = L.layerGroup(tempEvents);
        this.mainControl.addOverlay(region, 'temp-contour');

    }

    polygonDataHandler = (data) => {
        let my = data.contourData;
        let all_latlng = []
        // Classify points for different temp into different list
        for (let t = 0; t < this.tempBreaks.length - 1; t++) {
            let latlng_list = [];
            for (let i = 0; i < my.length; i++) {
                if (my[i].temp >= this.tempBreaks[t] && my[i].temp <= this.tempBreaks[t + 1]) {
                    latlng_list.push([Number(my[i].lat), Number(my[i].long)]);
                }
            }
            all_latlng.push(latlng_list)

        }
        console.log(all_latlng);
        // Assign a different color and a layer for each small temperature interval
        const colorlist = ['#393fb8', '#45afd6', '#49ebd8', '#49eb8f',
            '#a6e34b', '#f2de5a', '#edbf18', '#e89c20',
            '#f27f02', '#f25a02', '#f23a02', '#f0077f',
            '#f205c3', '#9306ba'
        ];
        const boxlist = ['blue- -6C', 'lightblue- -3C', 'greenblue- 0C', 'green- 3C', 'lightgreen- 6C',
            'yellow- 9C', 'darkyellow- 12C', 'lightorange- 15C', 'orange-18C', 'richorange- 21C', 'red- 24C',
            'purplered- 27C', 'lightpurple- 30C', 'purple- 33C'
        ]
        for (let i = 0; i < colorlist.length; i++) {
            this.tempLayer1 = L.TileLayer.maskCanvas({
                radius: 5,
                useAbsoluteRadius: true,
                color: '#000',
                opacity: 0.85,
                noMask: true,
                lineColor: colorlist[i]
            });
            this.tempLayer1.setData(all_latlng[i]);
            this.mainControl.addOverlay(this.tempLayer1, boxlist[i]);
            this.tempLayers.push(this.tempLayer1);
        }
        console.log(this.tempLayers);
    }

    rangeSelectHandler = (event) => {
        // Respond to the input range of temperature from the range selector in side bar

        // var int: always keep the lastest input Max/Min temperature
        if (event.newTemperature !== undefined) {
            this.tempMax = [];
            this.tempMax.push(event.newTemperature);
        }
        if (event.newTemperature2 !== undefined) {
            this.tempMin = [];
            this.tempMin.push(event.newTemperature2);
        }

        // for each valid input range, given list of layers of temp plotting satisfy the range and add to map
        if (this.tempMin[0] <= this.tempMax[0]) {
            for (let i = 0; i < this.tempBreaks.length; i++) {

                if (this.tempMax[0] >= this.tempBreaks[i] && this.tempMax[0] < this.tempBreaks[i + 1]) {
                    this.tempRegionsMax = [];
                    for (let k = 0; k <= i; k++) {
                        const region = this.tempLayers[k];
                        this.tempRegionsMax.push(region);
                    }
                }
            }
            for (let i = 0; i < this.tempBreaks.length; i++) {
                if (this.tempMin[0] >= this.tempBreaks[i] && this.tempMin[0] < this.tempBreaks[i + 1]) {
                    this.tempRegionsMax.splice(0, i);
                }
            }

            for (const layer of this.tempLayers) {
                this.map.removeLayer(layer);
            }
            for (const region of this.tempRegionsMax) {
                region.addTo(this.map);
            }
        }
    }

    ChoroplethDataHandler = () => {
        const colorlist = ['#bbd5f0','#87b9ed','#2f8ded','#1371d1',
            '#175799','#063b73','#032242','#031629'];
        function getColor(d) {
            return d > 800 ? colorlist[7] :
                d > 500 ? colorlist[6] :
                    d > 200 ? colorlist[5] :
                        d > 100 ? colorlist[4] :
                            d > 50 ? colorlist[3] :
                                d > 20 ? colorlist[2] :
                                    d > 10 ? colorlist[1] :
                                        colorlist[0];
        }

        function style(feature) {
            return {
                fillColor: getColor(feature.properties.density),
                weight: 0.5,
                opacity: 0.5,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7
            };
        }

        const ChoroplethLayer = L.geoJson(statesData, {style: style}) //.addTo(this.map);
        this.mainControl.addOverlay(ChoroplethLayer, 'Choropleth Map');

        function highlightFeature(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                layer.bringToFront();
            }
        }

        function resetHighlight(e) {
            geojson.resetStyle(e.target);
        }

        var geojson;
        geojson = L.geoJson();


    }

    CityDataHandler = () => {

        function style() {
            return {
                weight: 0.5,
                opacity: 0.5,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7
            };
        }

        const CityLayer = L.geoJson(citiesData, {style: style}) //.addTo(this.map);
        this.mainControl.addOverlay(CityLayer, 'City Map');
    }



    getColor = (d) => {
       return d > 1000 ? '#800026' :
           d > 500 ? '#BD0026' :
               d > 200 ? '#E31A1C' :
                   d > 100 ? '#FC4E2A' :
                       d > 50 ? '#FD8D3C' :
                           d > 20 ? '#FEB24C' :
                               d > 10 ? '#FED976' :
                                   '#FFEDA0';
   }
   style = (feature) => {
       return {
           //fillColor: this.getColor(feature.properties.density),
           weight: 2,
           opacity: 1,
           color: 'white',
           dashArray: '3',
           fillOpacity: 0.7
       };
   }

   highlightFeature = (e) => {
       // highlights the region when the mouse moves over the region
       let layer = e.target;
       layer.setStyle({
           weight: 5,
           color: '#666',
           dashArray: '',
           fillOpacity: 0.7
       });
       if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
           layer.bringToFront();
       }
   }
   resetHighlight = (e) => {
       // gets rid of the highlight when the mouse moves out of the region
       this.geojson.resetStyle(e.target);
   }
   zoomToFeature = (e) => {
       // zooms to a region when the region is clicked
       console.log('target', e.target);
       this.map.fitBounds(e.target.getBounds());
       console.log('map portion', this.map.getBounds());
       console.log('map zoom', this.map.getZoom());
   }
   onEachFeature = (feature, layer) => {
       // controls the interaction between the mouse and the map
       layer.on({
           mouseover: this.highlightFeature,
           mouseout: this.resetHighlight,
           click: this.zoomToFeature
       });
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
