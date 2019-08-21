import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';

declare let L;

export class LocationMarkerLayer {
    private theSearchMarker;
    private theHighlightMarker;

    constructor(private mainControl, private mapService: MapService, private map) {
        this.mapService.searchMarkerLoaded.subscribe(this.markerInputEventHandler);
        this.mapService.hoverMarkerLoaded.subscribe(this.markerMouseHoverEventHandler);
        this.mapService.markerRemove.subscribe(this.markerMouseHoverRemoveHandler);
    }

    markerInputEventHandler = (value) => {
        // creates the marker on the location being searched after zoomed in
        const centerLatlng = value[0];
        const userInput = value[1];
        const zoom = this.map.getZoom();

        if (this.theSearchMarker) {
            // removes previous marker
            this.map.removeControl(this.theSearchMarker);
        }

        // creates the name label
        const divIcon = L.divIcon({
            html: '<span style=\'color:#ffffff;font-size:18px;\' id=\'userInput\'>' + userInput + '</span>',
            iconSize: [this.map.getZoom(), this.map.getZoom()],
        });
        this.theSearchMarker = L.marker(new L.LatLng(centerLatlng[0], centerLatlng[1]), {icon: divIcon}).addTo(this.map);
        this.setLabelStyle(this.theSearchMarker); // sets the label style
    };

    markerMouseHoverEventHandler = (event) => {
        // shows the name label when the area is highlighted
        const layer = event.target;
        const divIcon = L.divIcon({
            html: '<span style=\'color:#ffffff;font-size: 18px;\'>' + layer.feature.properties.name + '</span>',
            iconSize: [this.map.getZoom(), this.map.getZoom()],
        });
        const centerLatLng = layer.getCenter();

        if (this.theSearchMarker) {
            this.map.removeControl(this.theSearchMarker);
        }

        if (this.theHighlightMarker) {
            this.map.removeControl(this.theHighlightMarker);
        }
        this.theHighlightMarker = L.marker(new L.LatLng(centerLatLng.lat, centerLatLng.lng), {icon: divIcon}).addTo(this.map);
        this.setLabelStyle(this.theHighlightMarker);

    };

    markerMouseHoverRemoveHandler = () => {
        if (this.theHighlightMarker) {
            this.map.removeControl(this.theHighlightMarker);
        }
    };


    setLabelStyle = (marker) => {
        // sets the name label style
        marker.getElement().style.backgroundColor = 'transparent';
        marker.getElement().style.border = 'transparent';
        marker.getElement().style.fontFamily = 'arial';
        marker.getElement().style.webkitTextStroke = '#ff8420';
        marker.getElement().style.webkitTextStrokeWidth = '0.5px';

    };


}
