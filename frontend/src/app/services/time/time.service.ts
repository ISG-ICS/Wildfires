import {Injectable} from '@angular/core';
// import {Observable, Subject, BehaviorSubject} from 'rxjs';
// import {HttpClient, HttpParams} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class TimeService {
    // "2018-04-23T10:26:00.996Z" => "2018-04-23"
    private currentDateInYMD = null;
    private startDate;
    private rangeStartDate;
    private rangeEndDate;

    constructor() {
    }

    setCurrentDate(dateInYMD) {
        this.currentDateInYMD = dateInYMD;
    }

    getCurrentDate() {
        return this.currentDateInYMD !== null ? this.currentDateInYMD : new Date().toISOString().substring(0, 10);
    }

    setRangeDate(startInMs, endInMs) {
        this.rangeStartDate = new Date(startInMs).toISOString().substring(0, 10);
        this.rangeEndDate = new Date(endInMs).toISOString().substring(0, 10);
    }

    getRangeDate() {
        return [this.rangeStartDate, this.rangeEndDate];
    }
}

