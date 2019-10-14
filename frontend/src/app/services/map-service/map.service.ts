import {EventEmitter, Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient, HttpParams} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {Tweet} from '../../models/tweet.model';
import {Wind} from '../../models/wind.model';
import {HeatMap} from '../../models/heatMap.model';
import {Boundary} from '../../models/boundary.model';
import {SearchSuggestion} from '../../models/search.suggestion.model';
import {environment} from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class MapService {

    // Declare data events for components to action
    temperatureChangeEvent = new EventEmitter();
    searchMarkerLoaded = new EventEmitter();
    hoverMarkerLoaded = new EventEmitter();
    markerRemove = new EventEmitter();
    searchNameLoaded = new EventEmitter();
    sendFireToFront = new EventEmitter();

    constructor(private http: HttpClient) {
    }


    getFireTweetData(): Observable<Tweet[]> {
        return this.http.get<Tweet[]>(`http://${environment.host}:${environment.port}/tweet/fire-tweet`);
    }

     getDateCountData(): Observable<Tweet[]> {
        return this.http.get<Tweet[]>(`http://${environment.host}:${environment.port}/tweet/tweet-count`);
    }


    getWildfirePredictionData(northEastBoundaries, southWestBoundaries, start, end): Observable<any> {
        return this.http.post(`http://${environment.host}:${environment.port}/wildfire-prediction`, JSON.stringify({
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
            startDate: start,
            endDate: end,
        }));
    }

    getFirePolygonData(northEastBoundaries, southWestBoundaries, setSize, start, end): Observable<any> {

        return this.http.post(`http://${environment.host}:${environment.port}/data/fire-polygon`, JSON.stringify({
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
            size: setSize,
            startDate: start,
            endDate: end,
        })).pipe(map(data => {

            return {type: 'FeatureCollection', features: data};
        }));
    }


    getWindData(): Observable<Wind[]> {
        return this.http.get<Wind[]>(`http://${environment.host}:${environment.port}/data/wind`);
    }

    getBoundaryData(stateLevel, countyLevel, cityLevel, northEastBoundaries, southWestBoundaries): Observable<Boundary> {

        return this.http.post<object>(`http://${environment.host}:${environment.port}/search/boundaries`, JSON.stringify({
            states: stateLevel,
            cities: cityLevel,
            counties: countyLevel,
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
        })).pipe(map(data => {

            return {type: 'FeatureCollection', features: data};
        }));
    }

    getDropBox(userInput): Observable<SearchSuggestion[]> {
        // gets auto-completion suggestions
        return this.http.get<SearchSuggestion[]>(`http://${environment.host}:${environment.port}/dropdownMenu`,
            {params: new HttpParams().set('userInput', userInput)});
    }


    getRecentTweetData(): Observable<any> {

        return this.http.get(`http://${environment.host}:${environment.port}/tweet/recent-tweet`);
    }

    getTemperatureData(): Observable<HeatMap[]> {
        return this.http.get<HeatMap[]>(`http://${environment.host}:${environment.port}/data/recent-temp`);
    }

    getClickData(lat, lng, radius, timestamp, range): Observable<any> {

        return this.http.post(`http://${environment.host}:${environment.port}/data/aggregation`, JSON.stringify({
            lat, lng, radius, timestamp, range
        }));
    }

    getIntentTweetData(id): Observable<any> {
        return this.http.get(`http://${environment.host}:${environment.port}/tweet/tweet-from-id`,
            {params: new HttpParams().set('tweet_id', id)});
    }
}
