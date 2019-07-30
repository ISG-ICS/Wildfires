import {Component, OnInit} from '@angular/core';
import {MapService} from '../../services/map-service/map.service';

import 'leaflet/dist/leaflet.css';

import 'leaflet-maskcanvas';

declare let L;


@Component({
    selector: 'app-search',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.css']
})

export class SearchComponent implements OnInit {


    private static STATE_LEVEL_ZOOM = 8;
    private static COUNTY_LEVEL_ZOOM = 9;
    private map;
    private mainControl;
    private geojson;
    private userInput;
    private theHighlightMarker;
    private theSearchMarker;


    constructor(private mapService: MapService) {
    }

    ngOnInit() {
        this.mapService.boundaryDataLoaded.subscribe(this.getBoundaryScreenDataHandler);
        this.mapService.mapLoaded.subscribe(([map, mainControl]) => {
            this.map = map;
            this.mainControl = mainControl; // get map and mainControl when heatmap.component loaded
            this.getBoundary();

            this.map.on('zoomend, moveend', () => {
                this.getBoundary();

            });
        });
    }

    searchEventHandler = (event) => {
        // takes user input and requests data from server
        if (event.key === 'Enter') {
            this.userInput = event.target.value;
            this.mapService.getSearch(this.userInput);
            this.mapService.searchDataLoaded.subscribe(this.boundaryDataHandler);

        }
        // TODO: auto-completion
    }

    boundaryDataHandler = (data) => {
        // given the boundary data after the keyword search, fits the map according to the boundary and shows the name label
        const listWithFixedLL = [];
        if (data !== null) {
            // list will be converted because of the lat and lon are misplaced
            for (const item of data.coordinates[0]) {
                listWithFixedLL.push([parseFloat(item[1]), parseFloat(item[0])]);
            }
            this.map.fitBounds(listWithFixedLL); // fits map according to the given fixed boundary list

            if (this.theSearchMarker) {
                // removes previous marker
                this.map.removeControl(this.theSearchMarker);
            }

            // TODO: separate a component for name label
            if (this.userInput !== null) {
                // creates the name label
                const divIcon = L.divIcon({
                    html: '<span style=\'color:#ffffff;font-size:18px;\' id=\'userInput\'>' + this.userInput + '</span>',
                    iconSize: [this.map.getZoom(), this.map.getZoom()],
                });
                const centerLatlng = this.getPolygonCenter(listWithFixedLL);
                this.theSearchMarker = L.marker(new L.LatLng(centerLatlng[0], centerLatlng[1]), {icon: divIcon}).addTo(this.map);
                this.setLabelStyle(this.theSearchMarker); // sets the label style
            }

        } else {
            // display "invalid input" on the search box if the user input data is not found in data list
            (document.getElementById('searchBox') as HTMLInputElement).value = '';
            (document.getElementById('searchBox') as HTMLInputElement).placeholder = 'Invalid input, please try again';
        }

    }

    getBoundary = () => {
        // gets the screen bounds and zoom level to get the corresponding geo boundaries from database
        const zoom = this.map.getZoom();
        const bound = this.map.getBounds();
        const boundNE = {lat: bound._northEast.lat, lon: bound._northEast.lng};
        const boundSW = {lat: bound._southWest.lat, lon: bound._southWest.lng};
        // tslint:disable-next-line:one-variable-per-declaration
        let showCityLevel, showStateLevel, showCountyLevel;

        // the boundary display with zoom levels is defined arbitrarily
        if (zoom < SearchComponent.STATE_LEVEL_ZOOM) {
            showCityLevel = false;
            showCountyLevel = false;
            showStateLevel = true;
        } else if (zoom < SearchComponent.COUNTY_LEVEL_ZOOM) {
            showCityLevel = false;
            showCountyLevel = true;
            showStateLevel = true;
        } else {
            showCityLevel = true;
            showCountyLevel = true;
            showStateLevel = true;
        }


        this.mapService.getBoundaryData(showStateLevel, showCountyLevel, showCityLevel, boundNE, boundSW);
    }

    getBoundaryScreenDataHandler = (data) => {

        // do nothing if checkbox is not checked
        if (!this.map.hasLayer(this.geojson) && this.geojson) {
            return;
        }

        // remove previous overlay
        if (this.geojson) {
            this.map.removeLayer(this.geojson);
            this.mainControl.removeLayer(this.geojson);
        }
        this.geojson = L.geoJson(data, {
            style: this.style,
            onEachFeature: this.onEachFeature
        });

        this.mainControl.addOverlay(this.geojson, 'Boundary');
        this.map.addLayer(this.geojson);
    }


    setLabelStyle = (marker) => {
        // sets the name label style
        marker.getElement().style.backgroundColor = 'transparent';
        marker.getElement().style.border = 'transparent';
        marker.getElement().style.fontFamily = 'monospace';
        marker.getElement().style.webkitTextStroke = '#ffe710';
        marker.getElement().style.webkitTextStrokeWidth = '0.5px';
    }


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
    }


    onEachFeature = (feature, layer) => {
        // controls the interaction between the mouse and the map
        layer.on({
            mouseover: this.highlightFeature,
            mouseout: this.resetHighlight,
            click: this.zoomToFeature
        });
    }


    getColor = (density) => {
        // color for the boundary layers
        // TODO: remove this func
        switch (true) {
            case (density > 1000):
                return '#802403';
            case (density > 500):
                return '#BD0026';
            case (density > 200):
                return '#E31A1C';
            case (density > 100):
                return '#FC4E2A';
            case (density > 50):
                return '#FD8D3C';
            case (density > 20):
                return '#FEB24C';
            case (density > 10):
                return '#FED976';
            default:
                return '#FFEDA0';
        }

    }

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
    }


    highlightFeature = (event) => {
        // highlights the region when the mouse moves over the region
        const layer = event.target;
        layer.setStyle({
            weight: 5,
            color: '#e3d926',
            dashArray: '',
            fillOpacity: 0.7
        });
        // shows the name label when the area is highlighted
        const divIcon = L.divIcon({
            html: '<span style=\'color:#ffffff;font-size: 18px;\'>' + layer.feature.properties.name + '</span>',
            iconSize: [this.map.getZoom(), this.map.getZoom()],
        });
        const centerLatLng = event.target.getCenter();
        if (this.theSearchMarker) {
            this.map.removeControl(this.theSearchMarker);
        }
        if (this.theHighlightMarker) {
            this.map.removeControl(this.theHighlightMarker);
        }
        this.theHighlightMarker = L.marker(new L.LatLng(centerLatLng.lat, centerLatLng.lng), {icon: divIcon})
            .addTo(this.map);
        this.theSearchMarker = L.marker(new L.latLng([this.map.getBounds()
            ._northEast.lat - 15, this.map.getBounds()._northEast.lng - 60]), {icon: divIcon}).addTo(this.map);
        this.setLabelStyle(this.theHighlightMarker);
        this.setLabelStyle(this.theSearchMarker);
    }

    resetHighlight = (event) => {
        // gets rid of the highlight when the mouse moves out of the region
        if (this.theHighlightMarker) {
            this.map.removeControl(this.theHighlightMarker);
        }
        if (this.theSearchMarker) {
            this.map.removeControl(this.theSearchMarker);
        }
        this.geojson.resetStyle(event.target);
    }

    zoomToFeature = (event) => {
        // zooms to a region when the region is clicked
        this.map.fitBounds(event.target.getBounds());

    }

}


