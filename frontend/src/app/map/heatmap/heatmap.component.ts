import * as $ from 'jquery';
import HeatmapOverlay from 'leaflet-heatmap/leaflet-heatmap.js';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import * as Highcharts from 'highcharts';

import {SearchService} from '../../services/search/search.service';
import {FireTweetLayer} from '../layers/fire.tweet.layer';
import {WindLayer} from '../layers/wind.layer';
import {FireEventLayer} from '../layers/fire.event.layer';
import {of, Subject} from 'rxjs';
import {FireRegionLayer} from '../layers/fire.region.layer';
import {LocationBoundaryLayer} from '../layers/location.boundary.layer';
import {LocationMarkerLayer} from '../layers/location.marker';
import {Component, OnInit} from '@angular/core';


declare let L;

@Component({
    selector: 'app-heatmap',
    templateUrl: './heatmap.component.html',
    styleUrls: ['./heatmap.component.css']
})
export class HeatmapComponent implements OnInit {

    private static STATE_LEVEL_ZOOM = 8;
    private static COUNTY_LEVEL_ZOOM = 9;
    private locationBoundaryLayer;
    private mainControl;
    private map;
    private theSearchMarker;
    private theHighlightMarker;
    private geojsonLayer;
    private fireTweetLayer;
    private windLayer;
    private fireEventLayer;
    private fireRegionLayer;
    private locationMarkerLayer;

    constructor(private mapService: MapService, private searchService: SearchService) {
    }


    private pinRadius = 40000;
    // For what to present when click event happens
    private marker = null;
    private group;
    private timer = null;


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


    constructor(private mapService: MapService, private searchService: SearchService) {
    }

    static drawChart(name, xValue, y1Name, y1Value, y1Unit, y2Name, y2Value, y2Unit, y2Color) {
        Highcharts.chart(name, {
            title: {
                text: '',
            },
            chart: {
                zoomType: 'x',
                style: {
                    fontSize: '10px',
                },
            },
            xAxis: {
                categories: xValue,
                crosshair: true,
            },
            plotOptions: {
                series: {
                    allowPointSelect: true,
                }
            },
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}' + y1Unit,
                    style: {
                        color: '#3b2f31',
                        fontSize: '8px',
                    }
                },
                title: {
                    text: '',
                }
            }, { // Secondary yAxis
                title: {
                    text: '',
                },
                labels: {
                    format: '{value} ' + y2Unit,
                    style: {
                        color: y2Color,
                        fontSize: '8px',
                    }
                },
                opposite: true
            }],
            tooltip: {
                shared: true,
            },
            series: [{
                name: y2Name,
                type: 'spline',
                color: y2Color,
                yAxis: 1,
                data: y2Value,
                tooltip: {
                    valueSuffix: ' ' + y2Unit,
                },
                showInLegend: false

            }, {
                name: y1Name,
                type: 'spline',
                color: '#3b2f31',
                data: y1Value,
                yAxis: 0,
                tooltip: {
                    valueSuffix: y1Unit,
                },
                showInLegend: false
            }]
        });
    }

    ngOnInit() {
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

        // Generate coordinate in sidebar
        this.map.addEventListener('mousemove', (ev) => {
            const lat = ev.latlng.lat;
            const lng = ev.latlng.lng;
            $('#mousePosition').html('Lat: ' + Math.round(lat * 100) / 100 + ' Lng: ' + Math.round(lng * 100) / 100);
        });

        // get boundary on init
        // this.getBoundary();

        // Get temperature data from service
        const tempSubject = new Subject();
        tempSubject.subscribe(this.dotMapDataHandler);
        tempSubject.subscribe(this.heatmapDataHandler);
        this.mapService.getTemperatureData().subscribe(tempSubject);

        // Get tweets data from service
        this.fireTweetLayer = new FireTweetLayer(this.mainControl, this.mapService, this.map);

        // Get fire events data from service
        this.fireEventLayer = new FireEventLayer(this.mainControl, this.mapService, this.map);

        this.fireRegionLayer = new FireRegionLayer(this.mainControl, this.mapService, this.map);

        this.locationBoundaryLayer = new LocationBoundaryLayer(this.mainControl, this.mapService, this.map);

        this.locationMarkerLayer = new LocationMarkerLayer(this.mainControl, this.mapService, this.map);
        // Get wind events data from service
        this.windLayer = new WindLayer(this.mainControl, this.mapService);

        // Get boundary data from service to draw it on map
        this.searchService.searchDataLoaded.subscribe(this.boundaryDataHandler);


        // Add event Listener when user specify a time range on time series
        $(window).on('timeRangeChange', this.fireTweetLayer.timeRangeChangeHandler);
        $(window).on('timeRangeChange', this.fireRegionLayer.timeRangeChangeFirePolygonHandler);
        $(window).on('timeRangeChange', this.fireEventLayer.timeRangeChangeFireEventHandler);

        // Send temp range selected from service
        this.mapService.temperatureChangeEvent.subscribe(this.rangeSelectHandler);

        this.map.on('mousedown', e => this.onMapHold(e));
        this.mapService.getRecentTweetData().subscribe(data => this.fireTweetLayer.recentTweetLoadHandler(data));

    }


    // fireEventHandler = (data) => {
    //
    //     const fireEventList = [];
    //
    //     for (const ev of data.fireEvents) {
    //         const point = [ev.lat, ev.long];
    //         const size = 40;
    //         const fireIcon = L.icon({
    //             iconUrl: 'assets/image/pixelfire.gif',
    //             iconSize: [size, size],
    //         });
    //         const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire(image>40%). My evidence is:<br/>' + ev.text);
    //         fireEventList.push(marker);
    //
    //     }
    //     const fireEvents = L.layerGroup(fireEventList);
    //     this.mainControl.addOverlay(fireEvents, 'Fire event');
    // };

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

    onMapClick(e) {
        // const oldMarker = this.marker;
        // const oldGroup = this.group;
        // if (oldMarker !== null) {
        //     if (oldMarker.isSticky) {
        //         oldGroup.addTo(this.map);
        //     }
        // }

        function mouseMoveChangeRadius(event) {
            const newRadius = distance(circle._latlng, event.latlng);
            localBound.setRadius(newRadius);
            circle.setRadius(newRadius);
        }


        function distance(center, pt) {
            // convert unit : degree of latlng to meter. eg: 1degree = 111km = 111000m
            return 111000 * Math.sqrt(Math.pow(center.lat - pt.lat, 2) + Math.pow(center.lng - pt.lng, 2));
        }

        const clickIcon = L.icon({
            iconUrl: 'assets/image/pin6.gif',
            iconSize: [26, 30],
        });
        const marker = L.marker(e.latlng, {draggable: false, icon: clickIcon});
        marker.isSticky = false;
        const circle = L.circle(e.latlng, {
            stroke: false,
            fillColor: 'white',
            fillOpacity: 0.35,
            radius: 40000,
        });
        const localBound = L.circle(e.latlng, {
            radius: 40000,
            color: 'white',
            weight: 5,
            fill: false,
            bubblingMouseEvents: false,
        })
            .on('mouseover', () => {
                localBound.setStyle({color: '#919191'});
            })
            .on('mouseout', () => {
                localBound.setStyle({color: 'white'});
            })
            .on('mousedown', () => {
                this.map.removeEventListener('click');
                this.map.dragging.disable();
                this.map.on('mousemove', mouseMoveChangeRadius);

                this.map.on('mouseup', (event) => {
                    const newRadius = distance(circle._latlng, event.latlng);
                    this.mapService.getClickData(e.latlng.lat, e.latlng.lng, newRadius / 111000, '2019-08-12T15:37:27Z', 7)  // convert unit :  meter to degree of latlng. eg: 1degree = 111km = 111000m
                        .subscribe(this.clickPointHandler);
                    this.map.dragging.enable();
                    this.map.removeEventListener('mousemove', mouseMoveChangeRadius);
                    setTimeout(() => {
                        this.map.on('mousedown', this.onMapHold, this);
                        this.map.removeEventListener('mouseup');
                    }, 500);
                }, this);
            });
        const group = L.layerGroup([marker, circle, localBound]).addTo(this.map);

        marker.bindPopup('You clicked the map at ' + e.latlng.toString(), {
            closeOnClick: false,
            autoClose: true,
        }).openPopup();

        this.map.on('mousedown', (e) => this.judgeDistance(e, group));

        this.marker = marker;
        this.group = L.layerGroup([marker, circle, localBound]);


        marker.getPopup().on('remove', () => {
            group.remove();
        }); // Remove popup fire remove all (default is not sticky)

        // TODO: change marker from global var since it only specify one.
        this.mapService.getClickData(e.latlng.lat, e.latlng.lng, this.pinRadius / 111000, '2019-08-19T15:37:27Z', 7)
            .subscribe(this.clickPointHandler);
    }

    judgeDistance(event, group) {
        this.map.on('mouseup', (e) => {
            if (event.latlng.lat === e.latlng.lat && event.latlng.lng === e.latlng.lng) {
                //if (!that.marker.isSticky) {
                group.remove();
                //}
            }
        });
    }


    clickPointHandler = (data) => {
        console.log(data);

        const cntTime = [];
        const cntValue = [];
        for (const tweetcnt of data.cnt_tweet) {
            cntTime.push(tweetcnt[0]);
            if (tweetcnt[1] === null) {
                cntValue.push(0);
            } else {
                cntValue.push(tweetcnt[1]);
            }
        }
        const tmpTime = [];
        const tmpValue = [];
        for (const avgtmp of data.tmp) {
            tmpTime.push(avgtmp[0]);
            if (avgtmp[1] === null) {
                tmpValue.push(0);
            } else {
                tmpValue.push(avgtmp[1] - 273.15);  // transfer the unit to celsius eg. 273 Kelvin --> 0 Celsius
            }
        }

        const soilwTime = [];
        const soilwValue = [];
        for (const avgsoilw of data.soilw) {
            soilwTime.push(avgsoilw[0]);
            if (avgsoilw[1] === null) {
                soilwValue.push(0);
            } else {
                soilwValue.push(avgsoilw[1] * 100); // transfer the unit to percent eg. 0.23 --> 23 %
            }
        }

        const pptTime = [];
        const pptValue = [];
        for (const avgppt of data.ppt) {
            pptTime.push(avgppt[0]);
            if (avgppt[1] === null) {
                pptValue.push(0);
            } else {
                pptValue.push(avgppt[1]);
            }
        }

        this.marker.bindPopup(this.clickboxContentsToShow).openPopup();
        HeatmapComponent.drawChart('container', soilwTime, 'Tweet counts', cntValue, 'tweets',
            'Moisture', soilwValue, '%', '#d9db9c');
        HeatmapComponent.drawChart('container2', tmpTime, 'Tweet counts', cntValue, 'tweets',
            'Temperature', tmpValue, 'Celsius', '#c4968b');
        HeatmapComponent.drawChart('container3', pptTime, 'Tweet counts', cntValue, 'tweets',
            'Precipitation', pptValue, 'mm', '#9fc7c3');

        this.marker.getPopup().on('remove', () => {
            this.group.remove();
        });

        // if (this.marker.isSticky) {
        //     this.group.addTo(this.map);
        // }
    };

    // stickyBotton = () => {
    //     const clickboxContents = $('<div />');
    //     clickboxContents.html('<button href="#" class="leaflet-popup-sticky-button1">S</button><br>')
    //         .on('click', '.leaflet-popup-sticky-button1', () => {
    //             this.marker.isSticky = !this.marker.isSticky;
    //             if (this.marker.isSticky) {
    //                 this.group.addTo(this.map);
    //             }
    //         });
    //     clickboxContents.append(this.clickboxContentsToShow);
    //     return clickboxContents[0];
    // };

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
            for (let i = 0; i < this.tempBreaks.length - 1; i++) {
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
    };


    boundaryDataHandler = ([[data], value]) => {
        // given the boundary data after the keyword search, fits the map according to the boundary and shows the name label
        // not plotting anything, only zooming in
        console.log(data);
        const listWithFixedLL = [];
        if (data) {
            // list will be converted because of the lat and lon are misplaced
            console.log(data.coordinates[0]);
            for (const item of data.coordinates[0]) {
                listWithFixedLL.push([parseFloat(item[1]), parseFloat(item[0])]);
            }
            this.map.fitBounds(listWithFixedLL); // fits map according to the given fixed boundary list
            const centerLatLng = this.getPolygonCenter(listWithFixedLL);
            this.mapService.searchMarkerLoaded.emit([centerLatLng, value]);
            // sends the center of the polygon to the location.boundary layer

        }
    };

    getPolygonCenter = (coordinateArr) => {
        // gets the center point when given a coordinate array
        // OPTIMIZE: the get polygon center function
        const x = coordinateArr.map(a => a[0]);
        const y = coordinateArr.map(a => a[1]);
        const minX = Math.min.apply(null, x);
        const maxX = Math.max.apply(null, x);
        const minY = Math.min.apply(null, y);
        const maxY = Math.max.apply(null, y);
        return [(minX + maxX) / 2, (minY + maxY) / 2];
    };


    clickboxContentsToShow() {
        const chartContents = '    <div id="containers" style="width: 280px; height: 360px;">\n' +
            '    <div id="container" style="width: 280px; height: 120px; margin: 0px; float: left;"></div>\n' +
            '    <div id="container2" style="width: 280px; height: 120px; margin: 0px; float: left;"></div>\n' +
            '    <div id="container3" style="width: 280px; height: 120px; margin: 0px; float: left;"></div>\n';


        const tweetContents = '    <div id="hh" style="width: 400px; height: 200px;">\n' +
            '    <div id="hh1" style="width: 200px; height: 100px; margin: 0px; float: left;"></div>\n' +
            '    <div id="hh2" style="width: 200px; height: 100px; margin: 0px; float: right;"></div>\n' +
            '    <div id="hh3" style="width: 200px; height: 100px; margin: 0px; float: left;"></div>\n' +
            '    <div id="hh4" style="width: 200px; height: 100px; margin: 0px;float: right;;"></div>\n';

        const clickboxContents = '<style>' +
            `.leaflet-popup-content {
                width: 400px;
            }
            .tabs {
                position: relative;
                min-height: 400px;
                min-width: 320px;
                clear: both;
                margin: 0px 0;
            }
            .tab {
                float: left;
                display: none;
            }
            .tab:first-of-type {
                display: inline-block;
            }
            .tabs-link {
                position: relative;
                top: -14px;
                height: 20px;
                left: -40px;
            }
            .tab-link {
                background: #eee;
                display: inline-block;
                padding: 10px;
                border: 1px solid #ccc;
                margin-left: -1px;
                position: relative;
                list-style-type: none;
                left: 1px;
                top: 1px;
                cursor: pointer;
            }
            .tab-link {
                background: #f8f8f8;
            }
            .content {
                background: white;
                position: absolute;
                top: 28px;
                left: 0;
                right: 0;
                bottom: 0;
                padding: 20px;
                border: 1px solid #ccc;
            }
            .tab:target {
                display: block;
            }` +
            '</style>' +
            '<div class="tabs" >' +
            '<div class="tab" id="tab-1" >' +
            '<div class="content">' +
            '<b>' +
            chartContents +
            '</b>' +
            '</div>' +
            '</div>' +

            '<div class="tab" id="tab-2" >' +
            '<div class="content">' +
            '<b>Put tweets contents here later</b>' +
            '</div>' +
            '</div>' +

            '<div class="tab" id="tab-3" >' +
            '<div class="content">' +
            '<b>whatever else</b>' +
            '</div>' +
            '</div>' +

            '<ul class="tabs-link">' +
            '<li class="tab-link"> <a href="#tab-1"><span>Charts</span></a></li>' +
            '<li class="tab-link"> <a href="#tab-2"><span>Tweets</span></a></li>' +
            '<li class="tab-link"> <a href="#tab-3"><span>Else</span></a></li>' +
            '</ul>' +
            '</div>';
        return clickboxContents;
    }
}
