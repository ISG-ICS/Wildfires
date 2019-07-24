import {EventEmitter, Injectable} from '@angular/core';
import * as $ from 'jquery';

@Injectable({
    providedIn: 'root'
})
export class MapService {

    // Declare data events for components to action
    tweetDataLoaded = new EventEmitter();
    heatmapDataLoaded = new EventEmitter();
    timeseriesDataLoaded = new EventEmitter();
    fireEventDataLoaded = new EventEmitter();
    liveTweetLoaded = new EventEmitter();
    mapLoaded = new EventEmitter();
    windDataLoaded = new EventEmitter();
    searchDataLoaded = new EventEmitter();
    boundaryDataLoaded = new EventEmitter();
    liveTweetCycle: any;

    constructor() {
    }

    processCSVData(allText, limit, delim = ',') {
        const allTextLines = allText.split(/\r\n|\n/);
        const matrix = [];
        for (let i = 1; i < allTextLines.length && i <= limit; i++) {
            const s = allTextLines[i];
            const tempEntry = s.split(delim);
            const entries = [];
            for (const entry of tempEntry) {
                if (entry !== '') {
                    entries.push(entry);
                }
            }
            matrix.push(entries);
        }
        return matrix;
    }

    getHeatmapData(): void {
        const heatData = [];
        const that = this;
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/temp',
            dataType: 'text',
        }).done(data => {
            const dataList = JSON.parse(data);
            console.log(dataList);
            const testData = {
                max: 8,
                data: dataList
            };
            this.heatmapDataLoaded.emit({heatmapData: testData});
        });

    }

    getTweetsData(): void {

        const chartData = [];
        const dailyCount = {};
        const that = this;
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/tweets',
            dataType: 'text',
        }).done(data => {

            const tempData = JSON.parse(data);
            const dataArray = [];
            tempData.forEach(entry => {
                const createAt = entry.create_at.split('T')[0];

                if (dailyCount.hasOwnProperty(createAt)) {
                    dailyCount[createAt]++;
                } else {
                    dailyCount[createAt] = 1;
                }

                const leftTop = [entry.lat, entry.long];
                dataArray.push([leftTop[0], leftTop[1], new Date(createAt).getTime()]);
            });

            // timebar
            Object.keys(dailyCount).sort().forEach(key => {
                chartData.push([new Date(key).getTime(), dailyCount[key]]);

            });

            this.tweetDataLoaded.emit({tweetData: dataArray});
            this.timeseriesDataLoaded.emit({chartData});
        });
    }

    getWildfirePredictionData(): void {
        const that = this;
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/wildfire_prediction',
            dataType: 'text'
        }).done((data) => {
            const wildfire = JSON.parse(data).filter(entry => entry.nlp === true);
            this.fireEventDataLoaded.emit({fireEvents: wildfire});
        });
    }

    getLiveTweetData(): void {
        const that = this;
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/live_tweet'
        }).done((data) => {
            that.liveTweetLoaded.emit({data});
        });
        this.liveTweetCycle = setInterval(() => {
            $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:5000/live_tweet'
            }).done((data) => {
                that.liveTweetLoaded.emit({data});
            });
        }, 20000);

    }

    getWindData(): void {
        const that = this;
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/wind'
        }).done((data) => {
            this.windDataLoaded.emit({data});

        });
    }

    getSearch(userInput): void {
        const that = this;
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/search',
            data: {keyword: userInput},
        }).done((data) => {
            console.log('data', data);
            this.searchDataLoaded.emit({data});
        });
    }

    getBoundaryData(stateLevel, countyLevel, cityLevel, northEastBoundaries, southWestBoundaries): void {
        const that = this;
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/search/boundaries',
            data: JSON.stringify({
                states: stateLevel,
                cities: cityLevel,
                counties: countyLevel,
                northEast: northEastBoundaries,
                southWest: southWestBoundaries,
            })
        }).done((data) => {

            let dict = {"type": "FeatureCollection", "features": data};
            this.boundaryDataLoaded.emit(dict);
        });
    }


    stopliveTweet(): void {
        window.clearInterval(this.liveTweetCycle);
    }

}
