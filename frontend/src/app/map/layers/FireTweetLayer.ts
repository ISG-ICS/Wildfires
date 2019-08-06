import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';

declare let L;

export class FireTweetLayer {
    private tweetLayer;
    private tweetData;

    constructor(private mainControl, private mapService: MapService) {
        this.mapService.getFireTweetData().subscribe(this.tweetDataHandler);
    }


    tweetDataHandler = (data) => {
        this.tweetLayer = L.TileLayer.maskCanvas({
            radius: 10,
            useAbsoluteRadius: true,
            color: '#000',
            opacity: 1,
            noMask: true,
            lineColor: '#e25822'
        });
        const tempData = [];
        this.tweetData = data.tweetData;
        data.tweetData.forEach(x => {
            tempData.push([x[0], x[1]]);
        });

        this.tweetLayer.setData(tempData);
        this.mainControl.addOverlay(this.tweetLayer, 'Fire tweet');

    }
}
