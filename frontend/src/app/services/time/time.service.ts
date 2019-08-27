import {Injectable} from '@angular/core';
// import {Observable, Subject, BehaviorSubject} from 'rxjs';
// import {HttpClient, HttpParams} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})

/**
 * Summary: TimeService as one separate service that allows other components to get time.
 *
 * Description: Initial current time range from previous 6 months to present.
 *
 * Author: (Hugo) Qiaonan Huang
 *
 * @param currentDateInYMD    Current date in yyyy-mm-dd, used in click event in time series.
 * @param rangeStartDateInMS  Range start time in millisecond, used in selection event in time series.
 * @param rangeEndDateInMS    Range end time in millisecond, used in selection event in time series.
 *
 */
export class TimeService {
    private currentDateInYMD = undefined;
    private rangeStartDateInMS = new Date().getTime() - 6 * 30 * 24 * 3600 * 1000;
    private rangeEndDateInMS = new Date().getTime();

    constructor() {
    }

    setCurrentDate(dateInYMD: string): void {
        this.currentDateInYMD = dateInYMD;
    }

    setRangeDate(startInMs: number, endInMs: number): void {
        this.rangeStartDateInMS = startInMs;
        this.rangeEndDateInMS = endInMs;
    }

    getCurrentDate(): string {
        return this.currentDateInYMD !== undefined ? this.currentDateInYMD : new Date().toISOString().substring(0, 10);
    }

    getRangeDate(): [number, number] {
        return [this.rangeStartDateInMS, this.rangeEndDateInMS];
    }
}

