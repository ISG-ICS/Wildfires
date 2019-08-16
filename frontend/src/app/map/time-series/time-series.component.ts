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
    private currentTick = null;

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
                    selection: event => {
                        this.timeService.setRangeDate(event.xAxis[0].min + this.halfUnit, event.xAxis[0].max);
                        if (event.xAxis) {
                            $('#report').html('Last selection ----- ' +
                                'min: ' + Highcharts.dateFormat('%Y-%m-%d', event.xAxis[0].min) +
                                ', max: ' + Highcharts.dateFormat('%Y-%m-%d', event.xAxis[0].max));
                        } else {
                            $('#report').html('Selection reset');
                        }
                        this.timeRangeChange.emit();
                        $(window).trigger('timeRangeChange');
                        return true;
                    },
                    click: event => {
                        // @ts-ignore
                        const clickValue = event.xAxis[0].value;
                        let dateInMs = clickValue - clickValue % this.halfUnit;
                        dateInMs += dateInMs % (this.halfUnit * 2);
                        const dateSelectedInYMD = new Date(dateInMs).toISOString().substring(0, 10);
                        // @ts-ignore
                        const tick = event.xAxis[0].axis.ticks[dateInMs];
                        if (this.currentTick === null) {
                            timeseries.xAxis[0].addPlotBand({
                                from: dateInMs - this.halfUnit,
                                to: dateInMs + this.halfUnit,
                                color: 'rgba(216,128,64,0.25)',
                                id: 'plotBand',
                            });
                            if (tick != null) {
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
                            if (this.currentTick != null && this.currentTick.hasOwnProperty('label')) {
                                this.currentTick.label.css({
                                    color: '#666666'
                                });
                            }
                            if (tick != null) {
                                tick.label.css({
                                    color: '#ffffff'
                                });
                            }
                            this.currentTick = tick;
                            this.timeService.setCurrentDate(dateSelectedInYMD);
                        } else {
                            timeseries.xAxis[0].removePlotBand('plotBand');
                            if (this.currentTick != null && this.currentTick.hasOwnProperty('label')) {
                                this.currentTick.label.css({
                                    color: '#666666'
                                });
                            }
                            this.currentTick = null;
                            this.timeService.setCurrentDate(null);
                        }

                    },
                }
            },
            navigator: {
                height: 40
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
            scrollbar: {
                barBackgroundColor: 'gray',
                barBorderRadius: 6,
                barBorderWidth: 0,
                buttonBackgroundColor: 'gray',
                buttonBorderWidth: 0,
                buttonArrowColor: 'silver',
                buttonBorderRadius: 6,
                rifleColor: 'silver',
                trackBackgroundColor: 'rgba(251,254,255,0.19)',
                trackBorderWidth: 1,
                trackBorderColor: 'silver',
                trackBorderRadius: 6
            },
        });
    }


}
