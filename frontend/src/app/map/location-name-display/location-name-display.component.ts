import {Component, OnInit} from '@angular/core';
import 'leaflet/dist/leaflet.css';
import 'leaflet-maskcanvas';
import {MapService} from '../../services/map-service/map.service';
import {SearchService} from '../../services/search/search.service';

@Component({
    selector: 'app-location-name-display',
    templateUrl: './location-name-display.component.html',
    styleUrls: ['./location-name-display.component.css']
})
export class LocationNameDisplayComponent implements OnInit {

    constructor(private mapService: MapService, private searchService: SearchService) {
    }

    ngOnInit() {
        this.searchService.searchDataLoaded.subscribe(this.locationInputEventHandler);
        this.mapService.searchNameLoaded.subscribe(this.locationMouseHoverEventHandler);

    }

    // OPTIMIZE: combine these two handlers
    locationInputEventHandler = ([[data], value]) => {
        document.getElementById('info').innerHTML = 'location name: ' + value;

    };

    locationMouseHoverEventHandler = (value) => {
        document.getElementById('info').innerHTML = 'location name: ' + value;

    };
}
