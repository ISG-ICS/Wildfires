import {Component, OnInit} from '@angular/core';
import {MapService} from "../../services/map-service/map.service";

import 'leaflet/dist/leaflet.css';

import 'leaflet-maskcanvas';

declare let L;
let geojson, userInput, globalData, theHighlightMarker, theSearchMarker, theSideMarker;

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
        this.mapService.boundaryDataLoaded.subscribe(this.getBoundaryScreenDataHandler);
        this.mapService.mapLoaded.subscribe((map) => {
            this.map = map;
            this.getBoundary();

            this.map.on("zoomend, moveend", () => {
                this.getBoundary();

            });
        });
    }

    searchEventHandler = (event) => {
        // takes user input and requests data from server
        if (event.key === 'Enter') {
            userInput = event.target.value;
            this.mapService.getSearch(userInput);
            this.mapService.searchDataLoaded.subscribe(this.boundaryDataHandler);

        }
        // TODO: auto-completion
    };

    boundaryDataHandler = (data) => {
        // given the boundary data after the keyword search, fits the map according to the boundary and shows the name label
        let listWithFixedLL = [];
        if (data['data'] !== null) {
            // list will be converted because of the lat and lon are misplaced
            for (let item of data['data'][0]['coordinates'][0]) {
                listWithFixedLL.push([parseFloat(item[1]), parseFloat(item[0])]);
            }
            this.map.fitBounds(listWithFixedLL); // fits map according to the given fixed boundary list

            if (theSearchMarker) {
                //removes previous marker
                this.map.removeControl(theSearchMarker);
            }

            if (userInput !== null) {
                // creates the name label
                let divIcon = L.divIcon({
                    html: "<span style='color:#ffffff;font-size: 18px;' id='userInput'>" + userInput + "</span>",
                    iconSize: [this.map.getZoom(), this.map.getZoom()],
                });
                let centerLatlng = this.getPolygonCenter(listWithFixedLL);
                theSearchMarker = L.marker(new L.LatLng(centerLatlng[0], centerLatlng[1]), {icon: divIcon}).addTo(this.map);
                this.setLabelStyle(theSearchMarker);// sets the label style
            }

        } else {
            // display "invalid input" on the search box if the user input data is not found in data list
            (<HTMLInputElement>document.getElementById("searchBox")).value = "";
            (<HTMLInputElement>document.getElementById("searchBox")).placeholder = "Invalid input, please try again";
        }

    };

    getBoundary = () => {
        // gets the screen bounds and zoom level to get the corresponding geo boundaries from database
        console.log('here in get bound');
        let zoom = this.map.getZoom();
        let bound = this.map.getBounds();
        console.log('zoom level', zoom);
        console.log('move level', bound);
        let boundNE = {'lat': bound['_northEast']['lat'], 'lon': bound['_northEast']['lng']};
        let boundSW = {'lat': bound['_southWest']['lat'], 'lon': bound['_southWest']['lng']};
        console.log('zoom', zoom);
        let showCityLevel, showStateLevel, showCountyLevel;

        // the boundary display with zoom levels is defined arbitrarily
        switch (true) {
            case (zoom < 8):
                showCityLevel = false;
                showCountyLevel = false;
                showStateLevel = true;
                break;
            case (zoom >= 8 && zoom < 9):
                showCityLevel = false;
                showCountyLevel = true;
                showStateLevel = true;
                break;
            case (zoom >= 9):
                showCityLevel = true;
                showCountyLevel = true;
                showStateLevel = true;
                break;
            default:
                showCityLevel = false;
                showCountyLevel = false;
                showStateLevel = false;
                break;
        }
        this.mapService.getBoundaryData(showStateLevel, showCountyLevel, showCityLevel, boundNE, boundSW);
    };

    getBoundaryScreenDataHandler = (data) => {
        // receives data from the database
        console.log('data in screen data handler', data);
        globalData = data;
        // L.geoJson(data).addTo(this.map);


        if (geojson) {
            console.log('layer in search key', this.map.removeLayer(geojson));
        }
        console.log('this data', data);
        geojson = L.geoJson(data, {
            style: this.style,
            onEachFeature: this.onEachFeature
        }).addTo(this.map);
    };


    setLabelStyle = (marker) => {
        // sets the name label style
        marker.getElement().style.backgroundColor = 'transparent';
        marker.getElement().style.border = 'transparent';
        marker.getElement().style.fontFamily = 'monospace';
        marker.getElement().style.webkitTextStroke = '#ffe710';
        marker.getElement().style.webkitTextStrokeWidth = '0.5px';
    };


    getPolygonCenter = (coorArr) => {
        // gets the center point when given a coordinate array
        let x = coorArr.map(function (a) {
            return a[0]
        });
        let y = coorArr.map(function (a) {
            return a[1]
        });
        let minX = Math.min.apply(null, x);
        let maxX = Math.max.apply(null, x);
        let minY = Math.min.apply(null, y);
        let maxY = Math.max.apply(null, y);
        return [(minX + maxX) / 2, (minY + maxY) / 2];
    };


    onEachFeature = (feature, layer) => {
        // controls the interaction between the mouse and the map
        console.log('feature layer', layer)
        layer.on({
            mouseover: this.highlightFeature,
            mouseout: this.resetHighlight,
            click: this.zoomToFeature
        });
    };


    getColor = (d) => {
        // color for the boundary layers
        switch (true) {
            case (d > 1000):
                return '#802403';
            case (d > 500):
                return '#BD0026';
            case (d > 200):
                return '#E31A1C';
            case (d > 100):
                return '#FC4E2A';
            case (d > 50):
                return '#FD8D3C';
            case (d > 20):
                return '#FEB24C';
            case (d > 10):
                return '#FED976';
            default:
                return '#FFEDA0';
        }

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
        console.log('e target', e.target)
        layer.setStyle({
            weight: 5,
            color: '#e3d926',
            dashArray: '',
            fillOpacity: 0.7
        });
        // shows the name label when the area is highlighted
        let divIcon = L.divIcon({
            html: "<span style='color:#ffffff;font-size: 18px;'>" + layer['feature']['properties']['name'] + "</span>",
            iconSize: [this.map.getZoom(), this.map.getZoom()],
        });
        let centerlatlng = e.target.getCenter();
        if (theSearchMarker) {
            this.map.removeControl(theSearchMarker);
        }
        if (theHighlightMarker) {
            this.map.removeControl(theHighlightMarker);
        }
        theHighlightMarker = L.marker(new L.LatLng(centerlatlng['lat'], centerlatlng['lng']), {icon: divIcon}).addTo(this.map);
        theSearchMarker = L.marker(new L.latLng([this.map.getBounds()['_northEast']['lat'] - 15, this.map.getBounds()['_northEast']['lng'] - 60]), {icon: divIcon}).addTo(this.map);
        this.setLabelStyle(theHighlightMarker);
        this.setLabelStyle(theSearchMarker);
    };

    resetHighlight = (e) => {
        // gets rid of the highlight when the mouse moves out of the region
        console.log('e target', e.target)
        if (theHighlightMarker) {
            this.map.removeControl(theHighlightMarker);
        }
        if (theSearchMarker) {
            this.map.removeControl(theSearchMarker);
        }
        geojson.resetStyle(e.target);
    };

    zoomToFeature = (e) => {
        // zooms to a region when the region is clicked
        console.log('target at zoom to ', e.target);
        this.map.fitBounds(e.target.getBounds());

    };

}


