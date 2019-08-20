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
    private halfUnit = 86400000 / 2;
    private currentTick = undefined;

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
                height: 150,
                backgroundColor: undefined,
                zoomType: 'x',
                events: {
                    click: event => {
                        // @ts-ignore
                        const clickValue = event.xAxis[0].value;
                        let dateInMs = clickValue - clickValue % this.halfUnit;
                        dateInMs += dateInMs % (this.halfUnit * 2);
                        const dateSelectedInYMD = new Date(dateInMs).toISOString().substring(0, 10);
                        // @ts-ignore
                        const tick = event.xAxis[0].axis.ticks[dateInMs];
                        if (this.currentTick === undefined) {
                            timeseries.xAxis[0].addPlotBand({
                                from: dateInMs - this.halfUnit,
                                to: dateInMs + this.halfUnit,
                                color: 'rgba(216,128,64,0.25)',
                                id: 'plotBand',
                            });
                            if (tick !== undefined) {
                                tick.label.css({
                                    color: '#ffffff'
                                });
                            }
                            this.currentTick = tick;
                            this.timeService.setCurrentDate(dateSelectedInYMD);
                        } else if (dateSelectedInYMD !== this.timeService.getCurrentDate()) {
                            timeseries.xAxis[0].removePlotBand('plotBand');
                            timeseries.xAxis[0].addPlotBand({
                                from: dateInMs - this.halfUnit,
                                to: dateInMs + this.halfUnit,
                                color: 'rgba(216,128,64,0.25)',
                                id: 'plotBand'
                            });
                            if (this.currentTick !== undefined && this.currentTick.hasOwnProperty('label')) {
                                this.currentTick.label.css({
                                    color: '#666666'
                                });
                            }
                            if (tick !== undefined) {
                                tick.label.css({
                                    color: '#ffffff'
                                });
                            }
                            this.currentTick = tick;
                            this.timeService.setCurrentDate(dateSelectedInYMD);
                        } else {
                            timeseries.xAxis[0].removePlotBand('plotBand');
                            if (this.currentTick !== undefined && this.currentTick.hasOwnProperty('label')) {
                                this.currentTick.label.css({
                                    color: '#666666'
                                });
                            }
                            this.currentTick = undefined;
                            this.timeService.setCurrentDate(undefined);
                        }

                    },
                }
            },
            navigator: {
                margin: 2,
                height: 30,
            },
            title: {
                text: '',
            },
            series: [{
                type: 'line',
                data: chartData,
                color: '#e25822',
                name: '<span style=\'color:#e25822\'>Wildfire Tweet</span>',
            }],
            tooltip: {
                enabled: true,
                backgroundColor: 'rgba(255,255,255,0)',
                padding: 0,
                hideDelay: 0,
                style: {
                    color: '#ffffff',
                }
            },
            rangeSelector: {
                enabled: false
            },
            xAxis: {
                type: 'datetime',
                range: 6 * 30 * 24 * 3600 * 1000, // six months
                events: {
                    setExtremes: (event) => {
                        this.timeService.setRangeDate(event.min + this.halfUnit, event.max);
                        $('#report').html('Date Range => ' +
                            'Start: ' + Highcharts.dateFormat('%Y-%m-%d', event.min) +
                            ', End: ' + Highcharts.dateFormat('%Y-%m-%d', event.max));
                        $(window).trigger('timeRangeChange');
                    }
                }
            },
            scrollbar: {
                height: 0,
            },
        });
    }


}
