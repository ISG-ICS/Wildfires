import {EventEmitter, Injectable} from '@angular/core';
import {interval, Observable} from 'rxjs';
import {HttpClient, HttpParams} from '@angular/common/http';
import {map, switchMap} from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class MapService {

    // Declare data events for components to action
    mapLoaded = new EventEmitter();
    temperatureChangeEvent = new EventEmitter();
    liveTweetCycle: any;


    constructor(private http: HttpClient) {


    }

    getFireTweetData(): Observable<any> {
        interface Tweet {
            create_at: string;
            lat: number;
            long: number;
        }

        return this.http.get('http://127.0.0.1:5000/tweet/fire-tweet').pipe(map((data: Tweet[]) => {
            const chartData = [];
            const dailyCount = {};
            const dataArray = [];
            for (const entry of data) {
                const createAt = entry.create_at.split('T')[0];

                if (dailyCount.hasOwnProperty(createAt)) {
                    dailyCount[createAt]++;
                } else {
                    dailyCount[createAt] = 1;
                }

                const leftTop = [entry.lat, entry.long];
                dataArray.push([leftTop[0], leftTop[1], new Date(createAt).getTime()]);
            }

            // time bar
            Object.keys(dailyCount).sort().forEach(key => {
                chartData.push([new Date(key).getTime(), dailyCount[key]]);
            });
            return {tweetData: dataArray, chartData};
        }));
    }

    getWildfirePredictionData(): Observable<any> {
        return this.http.get('http://127.0.0.1:5000/wildfire-prediction');
    }

    getLiveTweetData(): Observable<any> {

        return interval(20000).pipe(
            switchMap(() => {
                console.log('requesting');
                return this.http.get('http://127.0.0.1:5000/tweet/live-tweet');
            }));
    }

    getWindData(): Observable<any> {
        return this.http.get<any>('http://127.0.0.1:5000/data/wind');
    }

    getSearch(userInput): Observable<any> {
        return this.http.get('http://127.0.0.1:5000/search',
            {params: new HttpParams().set('keyword', userInput)}).pipe(map(data => data[0]));
    }

    // get administrative boundaries within screen
    getBoundaryData(stateLevel, countyLevel, cityLevel, northEastBoundaries, southWestBoundaries): Observable<any> {

        return this.http.post('http://127.0.0.1:5000/search/boundaries', JSON.stringify({
            states: stateLevel,
            cities: cityLevel,
            counties: countyLevel,
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
        })).pipe(map(data => {
            return {type: 'FeatureCollection', features: data};
        }));
    }

    getDropBox(userInput): Observable<any> {
        // gets auto-completion suggestions

        return this.http.get('http://127.0.0.1:5000/dropdownMenu', {params: new HttpParams().set('userInput', userInput)})
    }


    stopLiveTweet(): void {
        window.clearInterval(this.liveTweetCycle);
    }

    getTemperatureData(): Observable<any> {
        return this.http.get('http://127.0.0.1:5000/data/recent-temp');
    }
}
