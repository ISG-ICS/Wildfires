import 'leaflet/dist/leaflet.css';
import {MapService} from '../../services/map-service/map.service';
import * as $ from 'jquery';

declare let L;

export class ClickboxLayer {

    private pinRadius = 40000;

    private clickIcon = L.icon({
        iconUrl: 'assets/image/pin6.gif',
        iconSize: [26, 30],
    });
    private marker;
    private circle;
    private boundary;
    private group;

    constructor(private mainControl, private mapService: MapService, private map, private latlng) {
        this.generateClickbox();
    }

    mouseMoveChangeRadius(event) {
        const newRadius = this.distance(event.latlng);
        this.boundary.setRadius(newRadius);
        this.circle.setRadius(newRadius);
    }

    distance(pt) {
        // convert unit : degree of latlng to meter. eg: 1degree = 111km = 111000m
        return 111000 * Math.sqrt(Math.pow(this.latlng.lat - pt.lat, 2) + Math.pow(this.latlng.lng - pt.lng, 2));
    }

    generateClickbox() {

        this.marker = L.marker(this.latlng, {
            draggable: false,
            icon: this.clickIcon,
            isSticky: false,
        });
        this.circle = L.circle(this.latlng, {
            radius: this.pinRadius,
            stroke: false,
            fillColor: 'white',
            fillOpacity: 0.35,
        });
        this.boundary = L.circle(this.latlng, {
            radius: this.pinRadius,
            color: 'white',
            weight: 5,
            fill: false,
            bubblingMouseEvents: false,
        }).addTo(this.map)
        // change bound color when mouse on to tell user your mouse is on
            .on('mouseover', () => {
                this.boundary.setStyle({color: '#919191'});
            })
            .on('mouseout', () => {
                this.boundary.setStyle({color: 'white'});
            })
            .on('mousedown', () => {
                // deal with drag event when mouseon circle bound
                this.map.removeEventListener('click');
                this.map.dragging.disable();
                this.map.on('mousemove', this.mouseMoveChangeRadius, this);
                // send changed radius to backend with mousedown/mouseup
            })
            .on('mouseup', () => {
                this.map.dragging.enable();
                this.map.removeEventListener('mousemove', this.mouseMoveChangeRadius, this);
                setTimeout(() => {
                    this.map.on('click', event => {
                        this.marker = new ClickboxLayer(this.mainControl, this.mapService, this.map, event.latlng);
                    });
                }, 500);
            });
        this.group = L.layerGroup([this.marker, this.circle, this.boundary]).addTo(this.map);


        // this.map.on('mouseup', () => {
        //     // this.mapService.getClickData(event.latlng.lat, event.latlng.lng, this.pinRadius / 111000, '2019-07-30T15:37:27Z', 7)
        //     //     .subscribe(this.clickPointHandler);
        //     this.map.dragging.enable();
        //     this.map.removeEventListener('mousemove', mouseMoveChangeRadius);
        //     setTimeout(() => {
        //         this.map.on('click', this.onMapClick);
        //     }, 500);
        // });

        // Create Button To Set Sticky In Popup
        const container = $('<div />');
        container.html('<button href="#" class="leaflet-popup-sticky-button">S</button><br>')
            .on('click', '.leaflet-popup-sticky-button', () => {
                // Justify current sticky status
                this.marker.isSticky = !this.marker.isSticky;
                if (!this.marker.isSticky) {
                    this.marker.getPopup().on('remove', () => {
                        this.group.remove();
                    });
                } else {
                    this.marker.getPopup().removeEventListener('remove');
                }
            });
        container.append('You clicked the map at ' + this.latlng.toString());
        this.marker.bindPopup(container[0], {
            closeOnClick: false,
            autoClose: true,
        }).openPopup();

        // Remove popup fire remove all (default is not sticky)
        this.marker.getPopup().on('remove', () => {
            this.group.remove();
        });
        // TODO: change marker from global var since it only specify one.
        // this.mapService.getClickData(event.latlng.lat, event.latlng.lng, this.pinRadius / 111000, '2019-07-30T15:37:27Z', 7)
        //     .subscribe(this.clickPointHandler);
    }


}

