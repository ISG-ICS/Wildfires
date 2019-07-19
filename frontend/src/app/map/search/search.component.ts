import {Component, OnInit} from '@angular/core';
import {MapService} from "../../services/map-service/map.service";

import {stateBoundaries} from "./StateBoundaries.js";
import 'leaflet/dist/leaflet.css';

import 'leaflet-maskcanvas';

declare let L;
let geojson;


@Component({
    selector: 'app-search',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.css']
})

export class SearchComponent implements OnInit {

    private map;

    constructor(private mapService: MapService) {
    }

    ngOnInit() {
        this.mapService.mapLoaded.subscribe((map) => {
            this.map = map;

            this.statesStaticDisplay();
            // initializing the geojson boundary for the boundary highlighting interface
            // TODO: hook the stateBoundaries with server
            geojson = L.geoJson(stateBoundaries, {
                style: this.style,
                onEachFeature: this.onEachFeature
            }).addTo(this.map);

        });
    }

    statesStaticDisplay = () => {
        // displays the states boundaries when the map is first inited
        // TODO: hook the stateBoundaries with server
        L.geoJson(stateBoundaries).addTo(this.map);
    };

    boundaryDataHandler = (data) => {
        let listWithFixedLL = []; // list will be converted because of the lat and lon are misplaced
        // TODO: get rid of this when data on the server is changed to correct lat lon
        if (data['data'] !== null) {
            for (let item of data['data']['coordinates'][0]) {
                // rid of the list --> into the array list instead of an array of array
                let tlat = parseFloat(item[1]);
                let tlon = parseFloat(item[0]);
                console.log('lonlat', [tlat, tlon]);
                listWithFixedLL.push([tlat, tlon]);
            }

            console.log('list refined', listWithFixedLL);
            this.map.fitBounds(listWithFixedLL); // fits map according to the given boundary list

        } else {
            // display "invalid input" on the search box if the user input data is not found in data list
            (<HTMLInputElement>document.getElementById("searchBox")).value = "";
            (<HTMLInputElement>document.getElementById("searchBox")).placeholder = "Invalid input, please try again";
        }


    };

    searchEventHandler = (event) => {
        // takes user input and requests data from server
        if (event.key === 'Enter') {
            let userInput = event.target.value;
            this.mapService.getBoundaryData(userInput);
            this.mapService.searchDataLoaded.subscribe(this.boundaryDataHandler);
        }

    };

    getColor = (d) => {
        // color for the boundary layers
        return d > 1000 ? '#800026' :
            d > 500 ? '#BD0026' :
                d > 200 ? '#E31A1C' :
                    d > 100 ? '#FC4E2A' :
                        d > 50 ? '#FD8D3C' :
                            d > 20 ? '#FEB24C' :
                                d > 10 ? '#FED976' :
                                    '#FFEDA0';
    };

    style = (feature) => {
        // style for the boundary layers
        return {
            fillColor: this.getColor(feature.properties.density),
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
        };
    };


    highlightFeature = (e) => {
        // highlights the region when the mouse moves over the region
        let layer = e.target;

        layer.setStyle({
            weight: 5,
            color: '#e3d926',
            dashArray: '',
            fillOpacity: 0.7
        });
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    };

    resetHighlight = (e) => {
        // gets rid of the highlight when the mouse moves out of the region
        geojson.resetStyle(e.target);
    };

    zoomToFeature = (e) => {
        // zooms to a region when the region is clicked
        console.log('target', e.target);
        this.map.fitBounds(e.target.getBounds());
        console.log('map portion', this.map.getBounds());
        console.log('map zoom', this.map.getZoom());
    };

    onEachFeature = (feature, layer) => {
        // controls the interaction between the mouse and the map
        layer.on({
            mouseover: this.highlightFeature,
            mouseout: this.resetHighlight,
            click: this.zoomToFeature
        });
    };

};


