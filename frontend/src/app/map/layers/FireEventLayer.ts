import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';

declare let L;

export class FireEventLayer {

    constructor(private mainControl, private mapService: MapService) {
        this.mapService.getWildfirePredictionData().subscribe(this.fireEventHandler);
    }


    fireEventHandler = (fireEvents) => {
        // OPTIMIZE: move this to backend
        fireEvents.filter(entry => entry.nlp === true);
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

        this.mainControl.addOverlay(L.layerGroup(fireEventList), 'Fire event');
    }
}
