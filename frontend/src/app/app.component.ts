import {Component} from '@angular/core';

import '../../node_modules/leaflet-routing-machine/dist/leaflet-routing-machine.js';

declare let L;

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'wildfires-frontend';

    constructor() {

    }

    // ngOnInit() {
    //     const map = L.map('map').setView([51.505, -0.09], 13);
    //     // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //         //         attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    //         //     }).addTo(map);
    //         //
    //         //     L.Routing.control({
    //         //         waypoints: [
    //         //              L.latLng(57.74, 11.94),
    //         //             L.latLng(57.6792, 11.949)
    //         //         ]
    //         //     }).addTo(map);
    //     }

}
