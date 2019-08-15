import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';

declare let L;

export class FireRegionLayer {
    private firePolygon;
    private dateStartInISO;
    private dateEndInISO;
    private fireLabelLayer;

    constructor(private mainControl, private mapService: MapService, private map) {
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
        console.log('here in get fire poly');
        const zoom = this.map.getZoom();
        console.log('=========zoom', zoom);
        let size;
        if (zoom < 8) {
            size = 4;
        } else if (zoom < 9) {
            size = 3;
        } else {
            size = 2;
        }
        // TODO: replace polygon with fire icon in some conditions
        console.log('print size here in get fire polygon', size);
        const bound = this.map.getBounds();
        const boundNE = {lat: bound._northEast.lat, lon: bound._northEast.lng};
        const boundSW = {lat: bound._southWest.lat, lon: bound._southWest.lng};
        this.mapService.getFirePolygonData(boundNE, boundSW, size, start, end).subscribe(this.firePolygonDataHandler);
    };


    firePolygonDataHandler = (data) => {
        // if (!this.map.hasLayer(this.firePolygon) && this.firePolygon) {
        //     return;
        // }
        //
        // if (!this.map.hasLayer(this.fireLabelLayer) && this.fireLabelLayer) {
        //     return;
        // }
        if (this.firePolygon) {
            this.map.removeLayer(this.firePolygon);
            this.mainControl.removeLayer(this.firePolygon);
        }
        if (this.fireLabelLayer) {
            this.map.removeLayer(this.fireLabelLayer);
            this.mainControl.removeLayer(this.fireLabelLayer);

        }
        if (this.map.getZoom() < 8) {
            console.log('here in fire label ----------');
            const fireLabelList = [];
            for (const fireObject of data.features) {
                const point = [fireObject.geometry.coordinates[1], fireObject.geometry.coordinates[0]];
                const size = this.map.getZoom() * this.map.getZoom();
                const fireIcon = L.icon({
                    iconUrl: 'assets/image/pixelfire.gif',
                    iconSize: [size, size],
                });
                const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire');
                fireLabelList.push(marker);
            }
            this.fireLabelLayer = L.layerGroup(fireLabelList);
            this.mainControl.addOverlay(this.fireLabelLayer, 'Fire polygon');
            this.map.addLayer(this.fireLabelLayer);
        } else {
            console.log('here in fire polygon ----------');
            this.firePolygon = L.geoJson(data, {
                style: this.style,
                onEachFeature: this.onEachFeature
            });
            console.log('fire polygon layer', this.firePolygon);
            this.mainControl.addOverlay(this.firePolygon, 'Fire polygon');
            this.map.addLayer(this.firePolygon);
            this.firePolygon.bringToFront();
        }

    };

    getFirePolygonOnceMoved = () => {
        // calls this everytime the map is moved
        if (this.dateStartInISO && this.dateEndInISO) {
            console.log('here in fire polygon once moved');
            this.getFirePolygon(this.dateStartInISO, this.dateEndInISO);
        }
    };

    sendFireToFrontHandler = () => {
        if (this.firePolygon) {
            this.firePolygon.bringToFront();
            console.log('here send fire to front');
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
            fillOpacity: 0.7
        };
    };

    getColor = (density) => {
        // color for the boundary layers
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
