import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import * as $ from 'jquery';
import {FireService} from '../../services/fire-service/fire.service';
import {TimeService} from '../../services/time/time.service';


declare let L;

export class FireRegionLayer {
    private POINT_LABEL_ZOOM = 8;
    private ACCURATE_POLYGON_ZOOM = 9;
    private POINT_FIRE = 4;
    private LESS_DETAILED_FIRE_POLYGON = 3;
    private DETAILED_FIRE_POLYGON = 2;
    private MORE_DETAILED_FIRE_POLYGON = 1;
    private MOST_DETAILED_FIRE_POLYGON = 0;
    private isMarker;

    private firePolygon;
    private dateStartInISO;
    private dateEndInISO;
    private fireObjectInfo;
    private fireZoomOutPopup;
    private subscription;
    private needsRestart = false;

    constructor(private mainControl, private mapService: MapService, private map,
                private fireService: FireService, private timeService: TimeService, private isFirstTime) {
        this.mapService.sendFireToFront.subscribe(this.sendFireToFrontHandler);
        this.map.on('zoomend, moveend', this.getFirePolygonOnceMoved);
        // this.map.removeLayer(this.firePolygon);
        console.log('isFirstTime', this.isFirstTime);
        this.timeRangeChangeFirePolygonHandler();
        $(window).on('timeRangeChange', this.timeRangeChangeFirePolygonHandler);

    }

    /**
     * Creates the css style and adds object for the pop up content
     * @param fireObject  value in the features array of geojson data.
     * @return            Properly formatted pop up style and content.
     */
    private static formatPopUpContent(fireObject) {
        return '\n <div class="fire">\n '
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
    }

    /**
     * Gets start and end time from the time service, call function "getFirePolygon()" and provides it with the start and end time
     */
    timeRangeChangeFirePolygonHandler = () => {
        // processes given time data from time-series
        const [dateStartInMs, dateEndInMs] = this.timeService.getRangeDate();
        this.dateStartInISO = new Date(dateStartInMs).toISOString();
        this.dateEndInISO = new Date(dateEndInMs).toISOString();
        // start and end time are both in ISO datetime format
        this.getFirePolygon(this.dateStartInISO, this.dateEndInISO);
    };

    /**
     * Takes in the start and end time of a selected time range, defines the size (accuracy) of the fire polygon based on the
     * zoom in level, records the northEast and southWest bounds on the current screen display.
     * Then calls the function "getFirePolygonData" and provides NE bounds, SW bounds, size, start and end time
     * @param start  start time in ISO format.
     * @param end  end time in ISO format.
     */
    getFirePolygon = (start, end) => {
        // sends request to the map service based on the start/end time and the current screen map boundaries
        const zoom = this.map.getZoom();
        let size;
        if (zoom < this.POINT_LABEL_ZOOM) {
            size = this.POINT_FIRE;
        } else if (zoom < this.ACCURATE_POLYGON_ZOOM) {
            size = this.LESS_DETAILED_FIRE_POLYGON;
        } else {
            size = this.DETAILED_FIRE_POLYGON;
        }
        // decides how detailed the fire polygon should be based on the zoom level
        const bound = this.map.getBounds();
        const boundNE = {lat: bound._northEast.lat, lon: bound._northEast.lng};
        const boundSW = {lat: bound._southWest.lat, lon: bound._southWest.lng};
        // gets the NE and SW bounds on the current display
        this.subscription = this.mapService.getFirePolygonData(boundNE, boundSW, size, start, end).subscribe(this.firePolygonDataHandler);
    };

    /**
     * Adds fire label or fire polygon to the map based on the zoom in level
     * Adds pop ups once the user clicks on the fire label/fire polygon
     * @param data  geojson provided by the backend server
     */
    firePolygonDataHandler = (data) => {
        this.subscription.unsubscribe();
        if (this.map.hasLayer(this.firePolygon)) {
            this.isFirstTime = false;
            // if the layer is opened, then the first time condition is set to false, and each move/zoom in & out will add layer to the map
        }
        if (!this.map.hasLayer(this.firePolygon) && this.firePolygon) {
            return;
            // returns if the check box on main control is not checked but the fire polygon layer exists
        }
        if (this.firePolygon) {
            this.map.removeLayer(this.firePolygon);
            this.mainControl.removeLayer(this.firePolygon);
            // removes previous layer before adding the new layer
        }
        if (this.map.getZoom() < this.POINT_LABEL_ZOOM) {
            // the added firePolygon layer will have fire labels instead of polygons shown
            const fireLabelList = [];
            for (const fireObject of data.features) {
                if (fireObject.geometry.coordinates[0].length) {
                    // error handler: error exists when the user zoom in to fire polygon level --> move time series --> zoom out quickly
                    // into fire label level since the fireObject.geometry.coordinates[0] will be an array instead of a geolocation value
                    // if the returned value is correct (no error), its length is underfined thus will not come into this if statement
                    this.needsRestart = true;
                    break;
                    // this.needsRestart is set to true and breaks out of the current "if" condition
                }
                const latlng = [fireObject.geometry.coordinates[1], fireObject.geometry.coordinates[0]];
                // latlng order in geojson is different from that in the leaflet system, thus need to reverse the order
                const size = this.map.getZoom() * this.map.getZoom();
                const fireIcon = L.icon({
                    iconUrl: 'assets/image/pixelfire.gif',
                    iconSize: [size, size],
                });
                const marker = L.marker(latlng, {icon: fireIcon}).bindPopup(this.popUpContentZoomIn(fireObject));
                fireLabelList.push(marker);
                // adds the fire marker binding with a pop up
            }
            this.firePolygon = L.layerGroup(fireLabelList);
            this.mainControl.addOverlay(this.firePolygon, 'Fire polygon');
            if (!this.isFirstTime) {
                // if the map is initialized for the first time, the fire polygon layer is added to the main control but not opened
                this.map.addLayer(this.firePolygon);
            }
            this.isMarker = true;
            // the bringToFront() function does not work for marker, it only works for layer
        } else {
            // when the zoom in level allows the fire polygon to be shown
            this.firePolygon = L.geoJson(data, {
                style: this.style,
                onEachFeature: this.onEachFeature
            });
            // adds the fire polygon (which is data in geojson format) onto the map, with its style set
            this.mainControl.addOverlay(this.firePolygon, 'Fire polygon');
            if (!this.isFirstTime) {
                // if the map is initialized for the first time, the fire polygon layer is added to the main control but not opened
                this.map.addLayer(this.firePolygon);
            }
            this.firePolygon.bringToFront();
            this.isMarker = false;
            // the bringToFront() function does not work for marker, it only works for layer
        }
        if (this.needsRestart) {
            this.needsRestart = false;
            this.timeRangeChangeFirePolygonHandler();
            // calls the timeRangeChangeFirePolygonHandler() again and force it to detect the NE and SW boundaries of the display again
            // until the data provided is correct
        }
    };

    /**
     * Constructs the pop up content shown with the fire labels (which has a "zoom in" button on it)
     * @param fireObject  value in the features array of geojson data.
     * @return fireInfoTemplate[0] Properly formatted pop up style and content.
     */
    popUpContentZoomIn = (fireObject) => {
        // creates css style for the pop up content
        const fireInfoTemplate = $('<div />');
        fireInfoTemplate.html('<button href="#" class="button-action" ' +
            'style="color: #ff8420; font-family: "Dosis", Arial, Helvetica, sans-serif">Zoom In</button><br>')
            .on('click',
                '.button-action', () => {
                    // when the "zoom in" button is clicked in the pop up, go into firePolygonZoomInDataHandler which handles the zoom in
                    this.fireObjectInfo = fireObject;
                    // tslint:disable-next-line:max-line-length
                    this.fireService.searchFirePolygon(fireObject.id, this.DETAILED_FIRE_POLYGON).subscribe(this.firePolygonZoomInDataHandler);
                });
        const content = FireRegionLayer.formatPopUpContent(fireObject);
        fireInfoTemplate.append(content);
        return fireInfoTemplate[0];
    };

    /**
     * zooms in to the fire polygon and adds a pop up to the polygon
     * @param data  value in the features array of geojson data.
     * @return      Properly formatted pop up style and content.
     */
    firePolygonZoomInDataHandler = (data) => {
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
        // adds the pop up onto the fire polygon
    };

    /**
     * Constructs the pop up content shown with the fire labels (which has a "zoom out" button on it)
     * @param fireObject  value in the features array of geojson data.
     * @return            Properly formatted pop up style and content.
     */
    popUpContentZoomOut = (fireObject) => {
        // creates css style for the pop up content
        const fireInfoTemplate = $('<div />');
        const fireReplaceTemplate = $('<div />');
        // tslint:disable-next-line:max-line-length
        fireInfoTemplate.html('<button href="#" class="button-action" style="color: #ff8420; ' +
            'font-family: "Dosis", Arial, Helvetica, sans-serif">Zoom Out</button><br>')
            .on('click',
                '.button-action', () => {
                    // zooms out to the initial map view point and zoom level
                    this.map.setView([33.64, -117.84], 5);
                });
        // tslint:disable-next-line:max-line-length
        fireReplaceTemplate.html('<button href="#" class="button-replace" style="color: #ff8420; ' +
            'font-family: "Dosis", Arial, Helvetica, sans-serif">Show Fire for Each Day</button><br>')
            .on('click',
                '.button-replace', () => {
                    this.fireService.searchSeparatedFirePolygon(fireObject.id, 2)
                        .subscribe(this.firePolygonDataHandler);
                });
        const content = FireRegionLayer.formatPopUpContent(fireObject);
        fireInfoTemplate.append(fireReplaceTemplate);
        fireInfoTemplate.append(content);
        return fireInfoTemplate[0];
    };

    /**
     * Once the map is moved or zoomed in/out, adds the fire polygon layer again
     * Closes the pop up on the fire polygon once zoomed out to a certain level
     */
    getFirePolygonOnceMoved = () => {
        // calls this every time the map is moved
        if (this.dateStartInISO && this.dateEndInISO) {
            this.getFirePolygon(this.dateStartInISO, this.dateEndInISO);
        }
        // removes the popout sticked to the fire polygon when zoomed out to a certain level
        if (this.fireZoomOutPopup && this.map.getZoom() < 8) {
            this.map.closePopup(this.fireZoomOutPopup);
        }
    };

    /**
     * Sends the fire polygon layer to the front everytime the map is moved/zoom in&out
     */
    sendFireToFrontHandler = () => {
        // sends fire to the front layer
        if (this.firePolygon && !this.isMarker) {
            this.firePolygon.bringToFront();
        }
    };

    /**
     * Sets the style for the fire polygon layer
     */
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

    /**
     * Sets the color of the fire polygon layer
     */
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

    /**
     * Highlights/unhighlights the polygon that the mouse hovers over, zooms in to the region when the polygon is clicked.
     */
    onEachFeature = (feature, layer) => {
        // controls the interaction between the mouse and the map
        layer.on({
            mouseover: this.highlightFeature,
            mouseout: this.resetHighlight,
            click: this.zoomToFeature
        });
    };

    /**
     * Highlights the polygon that the mouse hovers over
     */
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

    /**
     * Unhighlights the polygon that the mouse hovers over
     */
    resetHighlight = (event) => {
        // gets rid of the highlight when the mouse moves out of the region

        this.firePolygon.resetStyle(event.target);
    };

    /**
     * Zooms in to the region when the polygon is clicked
     */
    zoomToFeature = (event) => {
        // zooms to a region when the region is clicked
        this.map.fitBounds(event.target.getBounds());
    };


}
