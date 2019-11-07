/**
 * @Summary: TimeService as one separate service that allows other components to get time.
 *
 * @Description: Initial current time range from previous 6 months to present.
 *
 * @Author: (Hugo) Qiaonan Huang
 *
 * Last modified  : 2019-08-27 15:31:40
 */

import {Injectable, EventEmitter} from '@angular/core';
import {Observable, of} from 'rxjs';
import {environment} from '../../../environments/environment';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Tweet} from "../../models/tweet.model";

// import {Observable, Subject, BehaviorSubject} from 'rxjs';
// import {HttpClient, HttpParams} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})

/**
 * @param currentDateInYMD    Current date in yyyy-mm-dd, used in click event in time series.
 * @param rangeStartDateInMS  Range start time in millisecond, used in selection event in time series.
 * @param rangeEndDateInMS    Range end time in millisecond, used in selection event in time series.
 *
 */
export class TimeService {
    public timeRangeChange = new EventEmitter();
    private currentDateInYMD = undefined;
    private rangeStartDateInMS = new Date().getTime() - 6 * 30 * 24 * 3600 * 1000;
    private rangeEndDateInMS = new Date().getTime();
    private timer;

    constructor(private http: HttpClient) {
    }

    setCurrentDate(dateInYMD: string): void {
        this.currentDateInYMD = dateInYMD;
    }

    setRangeDate(startInMs: number, endInMs: number): void {
        this.rangeStartDateInMS = startInMs;
        this.rangeEndDateInMS = endInMs;
        const duration = 1000;
        if (this.timer !== null) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        this.timer = setTimeout(L.Util.bind(() => {
            of(event).subscribe(() => this.timeRangeChange.next({start: this.rangeStartDateInMS, end: this.rangeEndDateInMS}));
            this.timer = null;
        }, this), duration);
        //this.timeRangeChange.next({start: this.rangeStartDateInMS, end: this.rangeEndDateInMS});
    }

    getCurrentDate(): string {
        return this.currentDateInYMD !== undefined ? this.currentDateInYMD : new Date().toISOString().substring(0, 10);
    }

    getRangeDate(): [number, number] {
        return [this.rangeStartDateInMS, this.rangeEndDateInMS];
    }

}

