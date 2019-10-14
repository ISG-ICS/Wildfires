/**
 * @Summary: TimeService as one separate service that allows other components to get time.
 *
 * @Description: Initial current time range from previous 6 months to present.
 *
 * @Author: (Hugo) Qiaonan Huang
 *
 * Last modified  : 2019-08-27 15:31:40
 */

import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
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
    private currentDateInYMD = undefined;
    private rangeStartDateInMS = new Date().getTime() - 6 * 30 * 24 * 3600 * 1000;
    private rangeEndDateInMS = new Date().getTime();

    constructor(private http: HttpClient) {

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

    getTweetByDate(startDate, endDate): Observable<Tweet[]> {
        return this.http.get<Tweet[]>(`http://${environment.host}:${environment.port}/tweet/tweet-by-date`,
            {params: new HttpParams().set('start-date', startDate).set('end-date', endDate)});
    }
}

