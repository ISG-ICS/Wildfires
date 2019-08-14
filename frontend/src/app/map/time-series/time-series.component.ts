import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import * as $ from 'jquery';
import {MapService} from '../../services/map-service/map.service';
import {TimeService} from '../../services/time/time.service';
import {Tweet} from '../../models/tweet.model';

import * as Highcharts from 'highcharts/highstock';

@Component({
    selector: 'app-time-series',
    templateUrl: './time-series.component.html',
    styleUrls: ['./time-series.component.css']
})
export class TimeSeriesComponent implements OnInit {

    @Output() timeRangeChange = new EventEmitter();
    private hasPlotBand = false;

    constructor(private mapService: MapService, private timeService: TimeService) {
    }

    ngOnInit() {
        this.mapService.getFireTweetData().subscribe(data => this.drawTimeSeries(data));
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

        const timeseries = Highcharts.stockChart('timebar-container', {
            chart: {
                height: 200,
                backgroundColor: null,
                zoomType: 'x',
                events: {
                    click: (event) => {
                        // @ts-ignore
                        const clickValue = event.xAxis[0].value;
                        const halfUnit = 86400000 / 2;
                        let dateInMs = clickValue - clickValue % halfUnit;
                        dateInMs += dateInMs % (halfUnit * 2);
                        const dateSelectedInISO = new Date(dateInMs).toISOString();
                        if (!this.hasPlotBand) {
                            timeseries.xAxis[0].addPlotBand({
                                from: dateInMs - halfUnit,
                                to: dateInMs + halfUnit,
                                color: 'rgba(216,128,64,0.25)',
                                id: 'plotBand',
                            });
                            this.hasPlotBand = true;
                            this.timeService.setCurrentDate(dateSelectedInISO);
                        } else if (this.ISOToYMD(dateSelectedInISO) !== this.ISOToYMD(this.timeService.getCurrentDate())) {
                            timeseries.xAxis[0].removePlotBand('plotBand');
                            timeseries.xAxis[0].addPlotBand({
                                from: dateInMs - halfUnit,
                                to: dateInMs + halfUnit,
                                color: 'rgba(216,128,64,0.25)',
                                id: 'plotBand'
                            });
                            this.hasPlotBand = true;
                            this.timeService.setCurrentDate(dateSelectedInISO);
                        } else {
                            timeseries.xAxis[0].removePlotBand('plotBand');
                            this.hasPlotBand = false;
                            this.timeService.setCurrentDate(null);
                        }
                    },
                }
            },
            navigator: {
                height: 20
            },
            title: {
                text: '',
            },
            series: [{
                type: 'line',
                data: chartData,
                color: '#e25822',
                name: '<span style=\'color:#e25822\'>Wildfire Tweet</span>'
            }],
            rangeSelector: {
                enabled: false
            },
            xAxis: {
                type: 'datetime',
                crosshair: true,
                range: 6 * 30 * 24 * 3600 * 1000, // six months
            },

        });
    }

    ISOToYMD(fullISOString) {
        return fullISOString.substring(0, 10);
    }

    YMDToISO(YMD) {
        return new Date(YMD).toISOString();
    }

}
