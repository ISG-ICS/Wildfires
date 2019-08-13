import {Injectable} from '@angular/core';
// import {Observable, Subject, BehaviorSubject} from 'rxjs';
// import {HttpClient, HttpParams} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class TimeService {
    // "2018-04-23T10:26:00.996Z" => "2018-04-23"
    private currentDateInISOString = null;

    constructor() {
    }

    setCurrentDate(dateInISOString) {
        this.currentDateInISOString = dateInISOString;
    }

    getCurrentDate() {
        return this.currentDateInISOString !== null ? this.currentDateInISOString : new Date().toISOString();
    }
}

