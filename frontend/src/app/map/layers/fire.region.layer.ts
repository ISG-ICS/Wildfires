import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import * as $ from 'jquery';
import {FireService} from '../../services/fire-service/fire.service';


declare let L;

export class FireRegionLayer {
    private firePolygon;
    private dateStartInISO;
    private dateEndInISO;
    private fireLabelLayer;
    private fireObjectInfo;
    private fireZoomOutPopup;


    constructor(private mainControl, private mapService: MapService, private map, private fireService: FireService) {
        this.mapService.sendFireToFront.subscribe(this.sendFireToFrontHandler);
        this.map.on('zoomend, moveend', this.getFirePolygonOnceMoved);
    }

    timeRangeChangeFirePolygonHandler = (event, data) => {
        // processes given time data from time-series
        this.dateStartInISO = new Date(data.timebarStart);
        this.dateEndInISO = new Date(data.timebarEnd);
        this.getFirePolygon(this.dateStartInISO, this.dateEndInISO);

    };
    getFirePolygon = (start, end) => {
        // sends request to the map service based on the start/end time and the current screen map boundaries
        const zoom = this.map.getZoom();
        let size;
        if (zoom < 8) {
            size = 4;
        } else if (zoom < 9) {
            size = 3;
        } else {
            size = 2;
        }
        // TODO: replace polygon with fire icon in some conditions
        const bound = this.map.getBounds();
        const boundNE = {lat: bound._northEast.lat, lon: bound._northEast.lng};
        const boundSW = {lat: bound._southWest.lat, lon: bound._southWest.lng};
        this.mapService.getFirePolygonData(boundNE, boundSW, size, start, end).subscribe(this.firePolygonDataHandler);
    };


    firePolygonDataHandler = (data) => {
        // adds the fire polygon to the map, the accuracy is based on the zoom level
        if (this.firePolygon) {
            this.map.removeLayer(this.firePolygon);
            this.mainControl.removeLayer(this.firePolygon);
        }
        if (this.fireLabelLayer) {
            this.map.removeLayer(this.fireLabelLayer);
            this.mainControl.removeLayer(this.fireLabelLayer);

        }
        if (this.map.getZoom() < 8) {
            const fireLabelList = [];
            for (const fireObject of data.features) {
                const latlng = [fireObject.geometry.coordinates[1], fireObject.geometry.coordinates[0]];
                const size = this.map.getZoom() * this.map.getZoom();
                const fireIcon = L.icon({
                    iconUrl: 'assets/image/pixelfire.gif',
                    iconSize: [size, size],
                });
                const marker = L.marker(latlng, {icon: fireIcon}).bindPopup(this.popUpContentZoomIn(fireObject));
                fireLabelList.push(marker);
            }
            this.fireLabelLayer = L.layerGroup(fireLabelList);
            this.mainControl.addOverlay(this.fireLabelLayer, 'Fire polygon');
            this.map.addLayer(this.fireLabelLayer);
        } else {
            this.firePolygon = L.geoJson(data, {
                style: this.style,
                onEachFeature: this.onEachFeature
            });
            this.mainControl.addOverlay(this.firePolygon, 'Fire polygon');
            this.map.addLayer(this.firePolygon);
            this.firePolygon.bringToFront();
        }

    };

    popUpContentZoomIn = (fireObject) => {
        // creates css style for the pop up content
        const fireInfoTemplate = $('<div />');
        // tslint:disable-next-line:max-line-length
        fireInfoTemplate.html('<button href="#" class="button-action" style="color: #ff8420; font-family: "Dosis", Arial, Helvetica, sans-serif">Zoom In</button><br>').on('click',
            '.button-action', () => {
                // when the fire pop up is triggered, go into firePolygonZoomInDataHandler which handels the zoom in
                this.fireObjectInfo = fireObject;
                this.fireService.searchFirePolygon(fireObject.id, 2).subscribe(this.firePolygonZoomInDataHandler);
            });
        const content = '\n <div class="fire">\n '
            + '      <span class="name" style=\'color: #ff8420;\'> '
            + 'Fire Name: ' + fireObject.properties.name
            + '      </span><br> '
            + '      <span class="fire-starttime" style=\'color: #ff8420;\'>'
            + 'Fire Start Time: ' + fireObject.properties.starttime
            + '      </span><br>\n	 '
            + '      <span class="fire-endtime" style=\'color: #ff8420;\'>'
            + 'Fire End Time: ' + fireObject.properties.endtime
            + '      </span><br>\n	 '
            + '      <span class="fire-area" style=\'color: #ff8420;\'>'
            + 'Fire Area: ' + fireObject.properties.area + ' acres'
            + '      </span><br>\n	 '
            + '<span class="fire-agency" style=\'color: #ff8420;\'>'
            + 'Fire Agency: ' + fireObject.agency
            + '      </span><br>\n	 '
            + '</div>\n';
        fireInfoTemplate.append(content);
        return fireInfoTemplate[0];
    };

    firePolygonZoomInDataHandler = (data) => {
        // zooms in to the fire polygon and adds a pop up
        const bbox = data[0].bbox.coordinates[0];
        const firePolygonLL = [];
        for (const item of bbox) {
            // changes the lat and lng because the geojson format is different to the leaflet latlng format
            firePolygonLL.push([parseFloat(item[1]), parseFloat(item[0])]);
        }
        this.map.fitBounds(firePolygonLL);
        this.fireZoomOutPopup = L.popup({autoClose: false, closeOnClick: false})
            .setLatLng(this.map.getCenter())
            .setContent(this.popUpContentZoomOut(this.fireObjectInfo))
            .openOn(this.map);
    };

    popUpContentZoomOut = (fireObject) => {
        // creates css style for the pop up content
        const fireInfoTemplate = $('<div />');
        const fireReplaceTemplate = $('<div />');
        // tslint:disable-next-line:max-line-length
        fireInfoTemplate.html('<button href="#" class="button-action" style="color: #ff8420; font-family: "Dosis", Arial, Helvetica, sans-serif">Zoom Out</button><br>').on('click',
            '.button-action', () => {
                this.map.setView([33.64, -117.84], 5);
            });
        // tslint:disable-next-line:max-line-length
        fireReplaceTemplate.html('<button href="#" class="button-replace" style="color: #ff8420; font-family: "Dosis", Arial, Helvetica, sans-serif">Show Fire for Each Day</button><br>').on('click',
            '.button-replace', () => {
                this.fireService.searchSeparatedFirePolygon(fireObject.id, 2).subscribe(this.firePolygonDataHandler);
            });
        const content = '\n <div class="fire">\n '
            + '      <span class="name" style=\'color: #ff8420;\'> '
            + 'Fire Name: ' + fireObject.properties.name
            + '      </span><br> '
            + '      <span class="fire-starttime" style=\'color: #ff8420;\'>'
            + 'Fire Start Time: ' + fireObject.properties.starttime
            + '      </span><br>\n	 '
            + '      <span class="fire-endtime" style=\'color: #ff8420;\'>'
            + 'Fire End Time: ' + fireObject.properties.endtime
            + '      </span><br>\n	 '
            + '      <span class="fire-area" style=\'color: #ff8420;\'>'
            + 'Fire Area: ' + fireObject.properties.area + ' acres'
            + '      </span><br>\n	 '
            + '<span class="fire-agency" style=\'color: #ff8420;\'>'
            + 'Fire Agency: ' + fireObject.properties.agency
            + '      </span><br>\n	 '
            + '</div>\n';
        fireInfoTemplate.append(fireReplaceTemplate);
        fireInfoTemplate.append(content);
        return fireInfoTemplate[0];
    };


    getFirePolygonOnceMoved = () => {
        // calls this everytime the map is moved
        if (this.dateStartInISO && this.dateEndInISO) {
            this.getFirePolygon(this.dateStartInISO, this.dateEndInISO);
        }
        // removes the popout sticked to the fire polygon when zoomed out to a certain level
        if (this.fireZoomOutPopup && this.map.getZoom() < 8) {
            this.map.closePopup(this.fireZoomOutPopup);
        }
    };

    sendFireToFrontHandler = () => {
        // sends fire to the front layer
        if (this.firePolygon) {
            this.firePolygon.bringToFront();
        }
    };

    style = (feature) => {
        // style for the boundary layers
        return {
            fillColor: this.getColor(feature.properties.density),
            weight: 2,
            opacity: 0.8,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.5
        };
    };

    getColor = (density) => {
        // color for the fire polygon layers
        // switch (true) {
        //     case (density > 1000):
        //         return '#802403';
        //     case (density > 500):
        //         return '#BD0026';
        //     case (density > 200):
        //         return '#E31A1C';
        //     case (density > 100):
        //         return '#FC4E2A';
        //     case (density > 50):
        //         return '#FD8D3C';
        //     case (density > 20):
        //         return '#FEB24C';
        //     case (density > 10):
        //         return '#FED976';
        //     default:
        //         return '#FFEDA0';
        // }
        return '#fff10d';

    };

    onEachFeature = (feature, layer) => {
        // controls the interaction between the mouse and the map
        layer.on({
            mouseover: this.highlightFeature,
            mouseout: this.resetHighlight,
            click: this.zoomToFeature
        });
    };

    highlightFeature = (event) => {
        // highlights the region when the mouse moves over the region
        const layer = event.target;
        layer.setStyle({
            weight: 5,
            color: '#e37927',
            dashArray: '',
            fillOpacity: 0.7
        });

    };
    resetHighlight = (event) => {
        // gets rid of the highlight when the mouse moves out of the region

        this.firePolygon.resetStyle(event.target);
    };

    zoomToFeature = (event) => {
        // zooms to a region when the region is clicked
        this.map.fitBounds(event.target.getBounds());
    };


}
