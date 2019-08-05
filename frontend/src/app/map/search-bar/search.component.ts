import {Component, OnInit} from '@angular/core';
import {MapService} from "../../services/map-service/map.service";

import 'leaflet/dist/leaflet.css';

import 'leaflet-maskcanvas';
import {FormControl} from "@angular/forms";
import "@angular/cdk";
import {SearchService} from "../../services/search/search.service";


@Component({
    selector: 'search-bar',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.css']
})


export class SearchComponent implements OnInit {

    public dataToDropDownMenu;
    myControl = new FormControl();

    constructor(private mapService: MapService, private searchService: SearchService) {
    }

    ngOnInit() {
        this.searchService.searchDataLoaded.subscribe(this.userInputCheckHandler);

    }

    dropDownHandler = (event) => {
        // clears any possible existing value from search box

        if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp' && event.key !== 'Enter') {
            if (event.target.value !== "") {
                this.mapService.getDropBox(event.target.value).subscribe(this.getSearchInputDataHandler);
                // gets auto-completion suggestion from the database
            }
        } else if (event.key === 'Enter') {
            this.selected(null, event.target.value);
            console.log('here in enter directly')
        }

    };

    getSearchInputDataHandler = (data) => {
        // process the data, make the display look more aesthetic
        let i;
        let cityString, countyString, stateString, city, county, state;
        cityString = countyString = stateString = city = county = state = "";
        let arr = {};
        this.dataToDropDownMenu = [];

        for (i = 0; i < data.length; i++) {
            // if the level data exists, add to the dictionary arr, then add arr to list dataToDropDownMen
            if (data[i][0]) {
                cityString = data[i][0] + " (city) ";
                city = data[i][0]
            }
            if (data[i][1]) {
                countyString = data[i][1] + " (county) ";
                county = data[i][1];
            }
            if (data[i][2]) {
                stateString = data[i][2] + " (state)";
                state = data[i][2];
            }
            arr['display'] = cityString + countyString + stateString;
            // 'display' is for showing on the drop down menu
            if (city) {
                arr['value'] = city;
            } else if (county) {
                arr['value'] = county;
            } else {
                arr['value'] = state;
            }
            // 'value' is for showing on the search box

            arr['id'] = data[i][3];
            // 'id' is for accurately locating the location
            this.dataToDropDownMenu.push(arr);
            arr = {};
        }
    };

    userInputCheckHandler = ([[data], value]) => {
        console.log(data);
        // given the boundary data after the keyword search, fits the map according to the boundary and shows the name label
        if (data) {
            console.log('data', data);
        } else {
            console.log('here, no data');
            (<HTMLInputElement>document.getElementById("search-input-id")).value = "";

        }
    };


    selected = (id, value) => {
        // FIXME: county id are all set to 6 due to the lack of county id data
        // passes the id and location name to search component
        if (id) {
            console.log('here in selected with id')
            this.searchService.getSearch(id).subscribe((data) => {
                this.searchService.searchDataLoaded.emit([data, value])
            })
        } else {
            console.log('here in selected with value');
            console.log('id', id);
            console.log('value', value);

            this.searchService.getSearch(value).subscribe((data) => {
                this.searchService.searchDataLoaded.emit([data, value])
            })
        }

    }

}