import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import {Boundary} from '../../models/boundary.model';

declare let L;

export class LocationBoundaryLayer {
    private boundaryLayer;

    constructor(private mainControl, private mapService: MapService, private map) {
        this.getBoundary();
        this.map.on('zoomend, moveend', this.getBoundary);

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
        if (zoom < 9) {
            showCityLevel = false;
            showCountyLevel = false;
            showStateLevel = true;
        } else if (zoom < 8) {
            showCityLevel = false;
            showCountyLevel = true;
            showStateLevel = true;
        } else {
            showCityLevel = true;
            showCountyLevel = true;
            showStateLevel = true;
        }

        this.mapService.getBoundaryData(showStateLevel, showCountyLevel, showCityLevel, boundNE, boundSW)
            .subscribe(this.getBoundaryScreenDataHandler);
    };

    getBoundaryScreenDataHandler = (data: Boundary) => {
        // adds boundary layer onto the map
        if (!this.map.hasLayer(this.boundaryLayer) && this.boundaryLayer) {
            return;
        }

        // remove previous overlay
        if (this.boundaryLayer) {
            this.map.removeLayer(this.boundaryLayer);
            this.mainControl.removeLayer(this.boundaryLayer);
        }
        this.boundaryLayer = L.geoJson(data, {
            style: this.style,
            onEachFeature: this.onEachFeature,
        });

        this.mainControl.addOverlay(this.boundaryLayer, 'Boundary');
        this.map.addLayer(this.boundaryLayer);
        this.mapService.sendFireToFront.emit();
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
        // color for the boundary layers
        // TODO: remove this func
        // switch (true) {
        //     case (density > 1000):
        //         return '#fd3208';
        //     case (density > 500):
        //         return '#f40031';
        //     case (density > 200):
        //         return '#f74d1a';
        //     case (density > 100):
        //         return '#fc5a0a';
        //     case (density > 50):
        //         return '#fd810b';
        //     case (density > 20):
        //         return '#fe046a';
        //     default:
        return 'rgba(255,255,255,0.25)';

        // }

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
        this.mapService.searchNameLoaded.emit(event.target.feature.properties.name);
        this.mapService.hoverMarkerLoaded.emit(event);

    };

    resetHighlight = (event) => {
        // gets rid of the highlight when the mouse moves out of the region

        this.boundaryLayer.resetStyle(event.target);
        this.mapService.searchNameLoaded.emit('');
        this.mapService.markerRemove.emit();

    };

    zoomToFeature = (event) => {
        // zooms to a region when the region is clicked
        this.map.fitBounds(event.target.getBounds());
    };

}
