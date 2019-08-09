import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';

declare let L;

export class FireRegionLayer {
    private firepolygon;

    constructor(private mainControl, private mapService: MapService, private map) {
    }


    timeRangeChangeFirePolygonHandler = (event, data) => {
        console.log('series, event', data);
        console.log('series, data', data);
        const dateStartInISO = new Date(data.timebarStart);

        const dateEndInISO = new Date(data.timebarEnd);

        console.log('series, data1', dateStartInISO);
        console.log('series, data2', dateEndInISO);

        this.getFirePolygon(dateStartInISO, dateEndInISO);

    };
    getFirePolygon = (start, end) => {
        console.log('here in get fire poly');
        const size = 3;
        // TODO: replace polygon with fire icon in some conditions
        const bound = this.map.getBounds();
        const boundNE = {lat: bound._northEast.lat, lon: bound._northEast.lng};
        const boundSW = {lat: bound._southWest.lat, lon: bound._southWest.lng};
        console.log('latlng', boundSW);
        this.mapService.getFirePolygonData(boundNE, boundSW, size, start, end).subscribe(this.firePolygonDataHandler);
    };

    firePolygonDataHandler = (data) => {
        console.log('here in fire handler', data);
        if (!this.map.hasLayer(this.firepolygon) && this.firepolygon) {
            return;
        }

        if (this.firepolygon) {
            this.map.removeLayer(this.firepolygon);
            this.mainControl.removeLayer(this.firepolygon);
        }

        this.firepolygon = L.geoJson(data, {
            style: this.style,
            onEachFeature: this.onEachFeature
        });

        console.log('here creating fire');
        this.mainControl.addOverlay(this.firepolygon, 'Fire polygon');
        this.map.addLayer(this.firepolygon);
        this.firepolygon.setZIndex(300);

    };
    style = (feature) => {
        // style for the boundary layers
        return {
            fillColor: this.getColor(feature.properties.density),
            weight: 2,
            opacity: 0.8,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.3
        };
    };

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

    };

    onEachFeature = (feature, layer) => {
        // controls the interaction between the mouse and the map
        layer.on({
            mouseover: () => {
                console.log('mouseover');
            },
            mouseout: () => {
                console.log('mouseout');
            },
            click: () => {
                console.log('click');
            }
        });
    }


}


