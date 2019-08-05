import {Component, OnInit} from '@angular/core';
import {MapService} from "../../services/map-service/map.service";

import 'leaflet/dist/leaflet.css';

import 'leaflet-maskcanvas';
import {FormControl} from "@angular/forms";
import "@angular/cdk";


@Component({
    selector: 'app-dropdownMenu',
    templateUrl: './dropdownMenu.component.html',
    styleUrls: ['./dropdownMenu.component.css']
})


export class DropdownMenuComponent implements OnInit {

    public dataToDropDownMenu;
    myControl = new FormControl();
    private map;

    constructor(private mapService: MapService) {
    }

    ngOnInit() {
        this.mapService.mapLoaded.subscribe((map) => {
            this.map = map;
        });
    }

    dropDownHandler = (event) => {
        // takes in the user input from the search box
        if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp' && event.key !== 'Enter') {
            if (event.target.value !== "") {
                this.mapService.getDropBox(event.target.value);
                // provides real time user input to get auto-completion suggestion

                this.mapService.dropDownMenuDataLoaded.subscribe(this.getSearchInputDataHandler);
                // gets auto-completion suggestion from the database
            }
        }
    };

    getSearchInputDataHandler = (data) => {
        // gets data from database, process data
        this.processData(data);
    };

    processData = (data) => {
        // process the data, make the display look more aesthetic
        let i;
        let cityString, countyString, stateString, city, county, state;
        cityString = countyString = stateString = city = county = state = "";
        let arr = {};
        this.dataToDropDownMenu = [];

        for (i = 0; i < data.length; i++) {
            // if the level data exists, add to the dictionary arr, then add arr to list dataToDropDownMen
            if (data[i][0]) {
                cityString = data[i][0] + " (city)  ";
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


    selected = (id, value) => {
        // passes the id and location name to search component
        this.mapService.dropBoxToSearch(id, value);

    }

}