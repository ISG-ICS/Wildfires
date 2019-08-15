import {EventEmitter, Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient, HttpParams} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {Tweet} from '../../models/tweet.model';
import {Wind} from '../../models/wind.model';
import {HeatMap} from '../../models/heatMap.model';
import {Boundary} from '../../models/boundary.model';
import {SearchSuggestion} from '../../models/search.suggestion.model';


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
        return this.http.get<Tweet[]>('http://127.0.0.1:5000/tweet/fire-tweet');
    }

    getWildfirePredictionData(northEastBoundaries, southWestBoundaries, start, end): Observable<any> {
        return this.http.post('http://127.0.0.1:5000/wildfire-prediction', JSON.stringify({
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
            startDate: start,
            endDate: end,
        }));
    }

    getFirePolygonData(northEastBoundaries, southWestBoundaries, setSize, start, end): Observable<any> {
        console.log('here in service');
        return this.http.post('http://127.0.0.1:5000/data/fire-polygon', JSON.stringify({
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
            size: setSize,
            startDate: start,
            endDate: end,
        })).pipe(map(data => {
            console.log('fire-polygon DATA ', data);
            return {type: 'FeatureCollection', features: data};
        }));
    }


    getWindData(): Observable<Wind[]> {
        return this.http.get<Wind[]>('http://127.0.0.1:5000/data/wind');
    }

    getBoundaryData(stateLevel, countyLevel, cityLevel, northEastBoundaries, southWestBoundaries): Observable<Boundary> {

        return this.http.post<object>('http://127.0.0.1:5000/search/boundaries', JSON.stringify({
            states: stateLevel,
            cities: cityLevel,
            counties: countyLevel,
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
        })).pipe(map(data => {
            console.log('boundary DATA ', {type: 'FeatureCollection', features: data});
            return {type: 'FeatureCollection', features: data};
        }));
    }

    getDropBox(userInput): Observable<SearchSuggestion[]> {
        // gets auto-completion suggestions
        return this.http.get<SearchSuggestion[]>('http://127.0.0.1:5000/dropdownMenu',
            {params: new HttpParams().set('userInput', userInput)});
    }


    getRecentTweetData(): Observable<any> {

        return this.http.get('http://127.0.0.1:5000/tweet/recent-tweet');
    }

    getTemperatureData(): Observable<HeatMap[]> {
        return this.http.get<HeatMap[]>('http://127.0.0.1:5000/data/recent-temp');
    }

    getClickData(lat, lng, radius, timestamp, range): Observable<any> {

        return this.http.post('http://127.0.0.1:5000/data/aggregation', JSON.stringify({
            lat, lng, radius, timestamp, range
        }));
    }

    getIntentTweetData(id): Observable<any> {
        return this.http.get('http://127.0.0.1:5000/tweet/tweet-from-id',
            {params: new HttpParams().set('tweet_id', id)});
    }
}
