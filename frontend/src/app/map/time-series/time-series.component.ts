import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import * as $ from 'jquery';
import {MapService} from '../../services/map-service/map.service';
import {Tweet} from '../../models/tweet.model';

declare var require: any;

@Component({
    selector: 'app-time-series',
    templateUrl: './time-series.component.html',
    styleUrls: ['./time-series.component.css']
})
export class TimeSeriesComponent implements OnInit {

    @Output() timeRangeChange = new EventEmitter();

    constructor(private mapService: MapService) {
    }

    ngOnInit() {
        this.mapService.getFireTweetData().subscribe(this.drawTimeSeries);
    }

    // Draw time series
    drawTimeSeries = (tweets: Tweet[]) => {
        const chartData = [];
        const dailyCount = {};

        for (const tweet of tweets) {
            const createAt = tweet.create_at.split('T')[0];
            if (dailyCount.hasOwnProperty(createAt)) {
                dailyCount[createAt]++;
            } else {
                dailyCount[createAt] = 1;
            }
        }


        // time bar
        Object.keys(dailyCount).sort().forEach(key => {
            chartData.push([new Date(key).getTime(), dailyCount[key]]);
        });

        require('highcharts').chart('timebar-container', {
            chart: {
                type: 'line',
                zoomType: 'x',
                height: 200,
                backgroundColor: null,
                events: {
                    selection(event) {
                        let timebarStart = 1;
                        let timebarEnd = 0;
                        if (event.hasOwnProperty('xAxis')) {
                            timebarStart = event.xAxis[0].min;
                            timebarEnd = event.xAxis[0].max;
                        } else {
                            timebarStart = event.target.axes[0].dataMin;
                            timebarEnd = event.target.axes[0].dataMax;
                        }
                        $(window).trigger('timeRangeChange', {timebarStart, timebarEnd});
                    }
                }
            },
            title: {
                text: 'Wildfire',
                style: {
                    color: '#e25822'
                }
            },
            xAxis: {
                type: 'datetime'
            },
            series: [{
                data: chartData,
                color: '#e25822',
                name: '<span style=\'color:#e25822\'>Wildfire Tweet</span>'
            }]

        });
    };

}
