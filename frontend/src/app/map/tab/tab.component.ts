/**
 * @author Yuan Fu <yuanf9@uci.edu>
 */
import {Component, OnInit} from '@angular/core';

@Component({
    selector: 'tab-group-basic',
    templateUrl: 'tab.component.html',
    styleUrls: ['tab.component.css']
})
export class TabGroupComponent implements OnInit {
    public link: string;

    constructor() {
    }

    ngOnInit() {
    }
}
