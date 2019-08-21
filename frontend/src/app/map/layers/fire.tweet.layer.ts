import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import 'leaflet-maskcanvas';
import 'leaflet-velocity-ts';
import {of} from 'rxjs';
import {Tweet} from '../../models/tweet.model';

declare let L;

export class FireTweetLayer {

    private tweetLayer;
    private tweetData: Tweet[] = [];
    private currentBounds = null;
    private currentMarker = null;
    private scaleX = 0;
    private scaleY = 0;
    private mouseOverPointI = 0;
    private tempDataWithID = [];
    private timer = null;

    constructor(private mainControl, private mapService: MapService, private map) {

        this.mapService.getFireTweetData().subscribe(this.tweetDataHandler);
        this.map.on('mousemove', e => this.onMapMouseMove(e));
    }

    // TODO: REWRITE IT!!!!!!
    static translateTweetDataToShow(tweetJSON) {
        // still need username, userPhotoUrl, image url from database
        let tweetid = '';
        try {
            tweetid = tweetJSON.id;
        } catch (e) {
            // tweet id missing in this Tweet.
        }

        let userName = '';
        try {
            userName = tweetJSON.user;
        } catch (e) {
            // userName missing in this Tweet.
        }

        let userPhotoUrl = '';
        try {
            // 'http://p1.qhimg.com/t015b79f2dd6a285745.jpg'
            userPhotoUrl = tweetJSON.profilePic;
        } catch (e) {
            // user.profile_image_url missing in this Tweet.
        }

        let tweetText = '';
        try {
            tweetText = tweetJSON.text;
        } catch (e) {
            // Text missing in this Tweet.
        }

        let tweetTime = '';
        try {
            const createdAt = new Date(tweetJSON.create_at);
            tweetTime = createdAt.toISOString();
        } catch (e) {
            // Time missing in this Tweet.
        }

        let tweetLink = '';
        try {
            tweetLink = 'https://twitter.com/' + userName + '/status/' + tweetid;
        } catch (e) {
            // tweetLink missing in this Tweet.
        }

        let imageUrl = '';
        try {
            imageUrl = tweetJSON.image; // 'https://pbs.twimg.com/media/DE6orpqVYAAeCYz.jpg'
        } catch (e) {
            // imageLink missing in this Tweet.
        }

        let tweetTemplate;

        // handles exceptions:
        if (tweetText === '' || null || undefined) {
            tweetTemplate = '\n'
                + '<div>'
                + 'Fail to get Tweets data.'
                + '</div>\n';
        } else {
            // presents all the information.
            tweetTemplate = '\n'
                + '<div class="tweet">\n '
                + '  <div class="tweet-body">'
                + '    <div class="user-info"> '
                + '      <img src="'
                + userPhotoUrl
                + '" onerror=" this.src=\'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJIsOFUYD9y2r12OzjDoEe5I1uhhF-gfVj5WGIqg8MzNBVzSogRw\'" style="width: 32px; display: inline; ">\n'
                + '      <span class="name" style=\'color: #0e90d2; font-weight: bold\'> '
                + userName
                + '      </span> '
                + '    </div>\n	'
                + '    <span class="tweet-time" style=\'color: darkgray\'>'
                + tweetTime
                + '    <br></span>\n	 '
                + '    <span class="tweet-text" style=\'color: #0f0f0f\'>'
                + tweetText
                + '    </span><br>\n	 '
                + '\n <a href="'
                + tweetLink
                + '"> '
                + tweetLink
                + '</a>'
                + '  </div>\n	'
                + '      <img src="'
                + imageUrl
                + '" onerror=" this.src=\'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1oYihdIC_G2vCN1dr3B6t5Y1EVKRLmD5qCrrtV_1eE3aJXpYv\'" style="height: 100px; ">\n'
                + '</div>\n';
        }

        return tweetTemplate;
    }


    tweetDataHandler = (tweets: Tweet[]) => {
        this.tweetData = tweets;
        this.tweetLayer = L.TileLayer.maskCanvas({
            radius: 10,
            useAbsoluteRadius: true,
            color: '#000',
            opacity: 1,
            noMask: true,
            lineColor: '#e25822'
        });
        const tempData = [];

        this.tweetData.forEach(tweet => {
                tempData.push([tweet.lat, tweet.long]);
            }
        );

        this.tweetLayer.setData(tempData);
        this.mainControl.addOverlay(this.tweetLayer, 'Fire tweet');

    }

    timeRangeChangeHandler = (event, data) => {
        const tempData = [];
        this.tempDataWithID = [];

        this.tweetData.forEach(tweet => {
            const time = new Date(tweet.create_at).getTime();
            if (time > data.timebarStart && time < data.timebarEnd) {
                tempData.push([tweet.lat, tweet.long]);
                this.tempDataWithID.push([tweet.lat, tweet.long, tweet.id]);
            }
        });
        this.tweetLayer.setData(tempData);
    }

    idOverPoint(x, y) {
        for (let i = 0; i < this.tempDataWithID.length; i += 1) {
            const distX = Math.abs((this.tempDataWithID[i][0] - x) / this.scaleX);
            const distY = Math.abs((this.tempDataWithID[i][1] - y) / this.scaleY);
            if (distX <= 0.001 && distY <= 0.001) {
                return [i, this.tempDataWithID[i][2]];
            }
        }
        return [-1, null];
    }

    onMapMouseMove(event) {
        const duration = 250;
        if (this.timer !== null) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        this.timer = setTimeout(L.Util.bind(() => {
            of(event).subscribe((ev) => this.onMapMouseIntent(ev));
            this.timer = null;
        }, this), duration);
    }

    onMapMouseIntent(e) {

        // make sure the scale metrics are updated
        if (this.currentBounds === null || this.scaleX === 0 || this.scaleY === 0) {
            this.currentBounds = this.map.getBounds();
            this.scaleX = Math.abs(this.currentBounds.getEast()
                - this.currentBounds.getWest());
            this.scaleY = Math.abs(this.currentBounds.getNorth()
                - this.currentBounds.getSouth());
        }

        const iandID = this.idOverPoint(e.latlng.lat, e.latlng.lng);
        const i = iandID[0];

        // if mouse over a new point, show the Popup Tweet!
        if (i >= 0 && this.mouseOverPointI !== i) {
            this.mouseOverPointI = i;
            // (1) If previous Marker is not null, destroy it.
            if (this.currentMarker != null) {
                this.map.removeLayer(this.currentMarker);
            }
            // (2) Create a new Marker to highlight the point.
            this.currentMarker = L.circleMarker(e.latlng, {
                radius: 7,
                color: '#fa4c3c',
                weight: 3,
                fillColor: '#f7ada6',
                fillOpacity: 1.0
            }).addTo(this.map);
            this.mapService.getIntentTweetData(iandID[1]).subscribe(data => this.IntentTweetPopup(data));
        }
    }

    IntentTweetPopup(data) {
        this.currentMarker.bindPopup(FireTweetLayer.translateTweetDataToShow(data));
    }

    recentTweetLoadHandler(data) {
        const fireEventList = [];
        for (const ev of data.slice(0, 150)) {
            const point = [ev.lat, ev.long];
            const size = 12.5;
            const fireIcon = L.icon({
                iconUrl: 'assets/image/perfectBird.gif',
                iconSize: [size, size],
            });
            const tweetContent = FireTweetLayer.translateTweetDataToShow(ev);
            // const tweetContent = 'CONTENT: ' + ev[4] + '<br/>TIME: ' + ev[2] + '<br/>TWEETID#: ' + ev[3];
            const marker = L.marker(point, {icon: fireIcon}).bindPopup(tweetContent);
            fireEventList.push(marker);

        }
        const fireEvents = L.layerGroup(fireEventList);
        this.mainControl.addOverlay(fireEvents, 'Recent tweet (within 2 days)');

    }

}
