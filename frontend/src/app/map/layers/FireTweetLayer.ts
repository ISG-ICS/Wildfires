import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import {Tweet} from '../../models/tweet.model';

declare let L;

export class FireTweetLayer {
    private tweetLayer;
    private tweetData;

    constructor(private mainControl, private mapService: MapService) {
        this.mapService.getFireTweetData().subscribe(this.tweetDataHandler);
    }


    tweetDataHandler = (tweets: Tweet[]) => {
        this.tweetLayer = L.TileLayer.maskCanvas({
            radius: 10,
            useAbsoluteRadius: true,
            color: '#000',
            opacity: 1,
            noMask: true,
            lineColor: '#e25822'
        });
        const tempData = [];
        this.tweetData = tweets;
        tweets.forEach(tweet => {
            tempData.push([tweet.lat, tweet.long]);
        });

        this.tweetLayer.setData(tempData);
        this.mainControl.addOverlay(this.tweetLayer, 'Fire tweet');

    }
}
