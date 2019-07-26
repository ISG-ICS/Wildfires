import {Component, OnInit} from '@angular/core';
import 'leaflet/dist/leaflet.css';
import * as $ from 'jquery';
import HeatmapOverlay from 'leaflet-heatmap/leaflet-heatmap.js';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';

declare let L;

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
    private tempLayer;
    private tempBreaks = [-6, -3, 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36];

    private colorList = ['#393fb8', '#45afd6', '#49ebd8', '#49eb8f',
        '#a6e34b', '#f2de5a', '#edbf18', '#e89c20',
        '#f27f02', '#f25a02', '#f23a02', '#f0077f',
        '#f205c3', '#9306ba'
    ];

    // For temp range selector store current max/min selected by user
    private tempRegionsMax = [];
    private tempMax = 36;
    private tempMin = 0;

    constructor(private mapService: MapService) {
    }

    ngOnInit() {
        // A hacky way to declare that
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
        // Generate coordinate in sidebar
        this.map.addEventListener('mousemove', (ev) => {
            const lat = ev.latlng.lat;
            const lng = ev.latlng.lng;
            $('#mousePosition').html('Lat: ' + Math.round(lat * 100) / 100 + ' Lng: ' + Math.round(lng * 100) / 100);
        });

        // Get temperature data from service
        this.mapService.getTemperatureData();
        this.mapService.temperatureDataLoaded.subscribe(this.dotMapDataHandler);
        this.mapService.temperatureDataLoaded.subscribe(this.heatmapDataHandler);

        // Send temp range selected from service
        this.mapService.temperatureChangeEvent.subscribe(this.rangeSelectHandler);

        // Get tweets data from service
        this.mapService.getFireTweetData();
        this.mapService.fireTweetDataLoaded.subscribe(this.tweetDataHandler);

        // Get fire events data from service
        this.mapService.getWildfirePredictionData();
        this.mapService.fireEventDataLoaded.subscribe(this.fireEventHandler);

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

    };


    liveTweetSwitchHandler = (_) => {
        if (this.switchStatus === 1) {
            this.liveTweetLayer.clearLayers();
            this.mapService.stopLiveTweet();
            this.switchStatus = 0;
            return;
        }
        this.mapService.getLiveTweetData();
        this.mapService.liveTweetLoaded.subscribe(this.liveTweetDataHandler);
        this.switchStatus = 1;
    };

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
    };

    timeRangeChangeHandler = (event, data) => {
        const tempData = [];
        this.tweetData.forEach(entry => {
            if (entry[2] > data.timebarStart && entry[2] < data.timebarEnd) {
                tempData.push([entry[0], entry[1]]);
            }
        });
        this.tweetLayer.setData(tempData);
    };

    fireEventHandler = (data) => {

        const fireEventList = [];

        for (const ev of data.fireEvents) {
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
    };

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
    };


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
        heatmapLayer.setData({max: 680, data});
        this.mainControl.addOverlay(heatmapLayer, 'Temp heatmap');
    };

    dotMapDataHandler = (data) => {
        const latLongBins = [];
        // Classify points for different temp into different list
        for (let t = 0; t < this.tempBreaks.length - 1; t++) {
            const points = [];
            for (const point of data) {
                if (point.temp >= this.tempBreaks[t] && point.temp <= this.tempBreaks[t + 1]) {
                    points.push([Number(point.lat), Number(point.long)]);
                }
            }
            latLongBins.push(points);
        }
        console.log(latLongBins);
        // Assign a different color and a layer for each small temperature interval
        for (let i = 0; i < this.colorList.length; i++) {
            this.tempLayer = L.TileLayer.maskCanvas({
                radius: 5,
                useAbsoluteRadius: true,
                color: '#000',
                opacity: 0.85,
                noMask: true,
                lineColor: this.colorList[i]
            });
            this.tempLayer.setData(latLongBins[i]);
            this.tempLayers.push(this.tempLayer);
        }
    };


    rangeSelectHandler = (event) => {
        const inRange = (min: number, max: number, target: number) => {
            return target < max && target >= min;
        };

        // Respond to the input range of temperature from the range selector in side bar
        // var int: always keep the latest input Max/Min temperature
        if (event.high !== undefined) {
            this.tempMax = event.high;
        }
        if (event.low !== undefined) {
            this.tempMin = event.low;
        }
        if (this.tempMin <= this.tempMax) {
            this.tempRegionsMax = [];
            let startSelecting = false;
            // Push layers in selected range into list tempRegionsMax
            for (let i = 0; i < this.tempBreaks.length; i++) {
                const rangeMin = this.tempBreaks[i];
                const rangeMax = this.tempBreaks[i + 1];
                if (inRange(rangeMin, rangeMax, this.tempMin)) {
                    startSelecting = true;
                }
                if (startSelecting) {
                    this.tempRegionsMax.push(this.tempLayers[i]);
                }
                if (inRange(rangeMin, rangeMax, this.tempMax)) {
                    startSelecting = false;
                    break;
                }
            }
            // Remove previous canvas layers
            for (const layer of this.tempLayers) {
                this.map.removeLayer(layer);
            }
            // Add new canvas layers in the updated list tempRegionsMax to Map
            for (const region of this.tempRegionsMax) {
                region.addTo(this.map);
            }
            console.log(this.tempRegionsMax);
        }
    }
}
