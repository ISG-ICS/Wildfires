import {Component} from '@angular/core';

import '../../node_modules/leaflet-routing-machine/dist/leaflet-routing-machine.js';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'Wildfire Map';
}
