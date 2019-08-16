import {Injectable} from '@angular/core';
// import {Observable, Subject, BehaviorSubject} from 'rxjs';
// import {HttpClient, HttpParams} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class TimeService {
    // "2018-04-23T10:26:00.996Z" => "2018-04-23"
    private currentDateInYMD = null;
    private rangeStartDateInMS = new Date().getTime() - 6 * 30 * 24 * 3600 * 1000;
    private rangeEndDateInMS = new Date().getTime();

    constructor() {
    }

    setCurrentDate(dateInYMD) {
        this.currentDateInYMD = dateInYMD;
    }

    getCurrentDate() {
        return this.currentDateInYMD !== null ? this.currentDateInYMD : new Date().toISOString().substring(0, 10);
    }

    setRangeDate(startInMs, endInMs) {
        this.rangeStartDateInMS = startInMs;
        this.rangeEndDateInMS = endInMs;
    }

    getRangeDate() {
        return [this.rangeStartDateInMS, this.rangeEndDateInMS];
    }
}

