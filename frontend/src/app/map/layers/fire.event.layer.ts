import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';

declare let L;

export class FireEventLayer {
    private fireEvent;

    constructor(private mainControl, private mapService: MapService, private map) {
    }

    timeRangeChangeFireEventHandler = (event, data) => {
        console.log('series, event', data);
        console.log('series, data', data);
        const dateStartInISO = new Date(data.timebarStart);

        const dateEndInISO = new Date(data.timebarEnd);

        console.log('series, data1', dateStartInISO);
        console.log('series, data2', dateEndInISO);

        this.getFireEvent(dateStartInISO, dateEndInISO);
    };
    getFireEvent = (start, end) => {
        console.log('here in get fire event');
        const bound = this.map.getBounds();
        const boundNE = {lat: bound._northEast.lat, lon: bound._northEast.lng};
        const boundSW = {lat: bound._southWest.lat, lon: bound._southWest.lng};
        console.log('latlng', boundSW);
        this.mapService.getWildfirePredictionData(boundNE, boundSW, start, end).subscribe(this.fireEventHandler);
    };

    fireEventHandler = (fireEvents) => {
        // OPTIMIZE: move this to backend
        fireEvents.filter(entry => entry.nlp === true);


        if (!this.map.hasLayer(this.fireEvent) && this.fireEvent) {
            return;
        }

        if (this.fireEvent) {
            this.map.removeLayer(this.fireEvent);
            this.mainControl.removeLayer(this.fireEvent);
        }
        const fireEventList = [];

        for (const ev of fireEvents) {
            const point = [ev.lat, ev.long];
            const size = 40;
            const fireIcon = L.icon({
                iconUrl: 'assets/image/pixelfire.gif',
                iconSize: [size, size],
            });
            const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire');

            fireEventList.push(marker);

        }
        this.fireEvent = L.layerGroup(fireEventList)
        this.mainControl.addOverlay(this.fireEvent, 'Fire event');
        this.map.addLayer(this.fireEvent);
    }
}
