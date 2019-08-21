import {Component, OnInit} from '@angular/core';
import {MapService} from '../../services/map-service/map.service';

import 'leaflet/dist/leaflet.css';

import 'leaflet-maskcanvas';
import {FormControl} from '@angular/forms';
import '@angular/cdk';
import {SearchService} from '../../services/search/search.service';
import {SearchSuggestion} from "../../models/search.suggestion.model";


@Component({
    selector: 'app-search-bar',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.css']
})


export class SearchComponent implements OnInit {

    private dataToDropDownMenu;
    private formControl = new FormControl();

    constructor(private mapService: MapService, private searchService: SearchService) {
    }

    ngOnInit() {
        this.searchService.searchDataLoaded.subscribe(this.userInputCheckHandler);

    }

    dropDownHandler = (event) => {

        // clears any possible existing value from search box
        if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp' && event.key !== 'Enter') {
            if (event.target.value !== '') {
                this.mapService.getDropBox(event.target.value).subscribe(this.getSearchInputDataHandler);
                // gets auto-completion suggestion from the database
            }
        }
        if (event.key === 'Enter') {
            this.selected(null, event.target.value);
        }
    };

    getSearchInputDataHandler = (data: SearchSuggestion[]) => {
        // process the data, make the display look more aesthetic
        let i;
        let cityString = '';
        let countyString = '';
        let stateString = '';

        this.dataToDropDownMenu = [];

        for (i = 0; i < data.length; i++) {
            // if the level data exists, add to the dictionary arr, then add arr to list dataToDropDownMen
            if (data[i][0]) {
                cityString = data[i][0] + ', ';
            }
            if (data[i][1]) {
                countyString = data[i][1] + ', ';
            }
            if (data[i][2]) {
                stateString = data[i][2];
            }

            // 'value' is for showing on the search box
            const value = cityString + countyString + stateString;
            const id = data[i][3];
            // 'id' is for accurately locating the location
            this.dataToDropDownMenu.push({display: value, value, id});
        }
    };

    userInputCheckHandler = ([[data], value]) => {
        // given the boundary data after the keyword search, fits the map according to the boundary and shows the name label
        if (data) {

        } else {

            (document.getElementById('search-input-id') as HTMLInputElement).value = '';

            (document.getElementById('placeholder') as HTMLInputElement).innerHTML = 'Please enter again';

        }
    };


    selected = (id, value) => {
        // FIXME: county id are all set to 6 due to the lack of county id data
        // passes the id and location name to search component
        if (id) {

            this.searchService.getSearch(id).subscribe((data) => {
                this.searchService.searchDataLoaded.emit([data, value]);
            });
        } else {

            this.searchService.getSearch(value).subscribe((data) => {
                this.searchService.searchDataLoaded.emit([data, value]);
            });
        }

    };

}
