import {Component, OnInit, EventEmitter, Output} from '@angular/core';
import * as $ from 'jquery';
import {MapService} from '../../services/map-service/map.service';
declare var require: any;
const Highcharts = require('highcharts');

@Component({
  selector: 'app-time-series',
  templateUrl: './time-series.component.html',
  styleUrls: ['./time-series.component.css']
})
export class TimeSeriesComponent implements OnInit {

  @Output() timeRangeChange = new EventEmitter();

  constructor(private mapService: MapService) { }

  ngOnInit() {
    this.mapService.timeseriesDataLoaded.subscribe(this.drawTimeSeries);
  }

  // Draw time series
  drawTimeSeries = (data) => {
    const chartData = data.chartData;
    const that = this;
    const timeseries = Highcharts.chart('timebar-container', {
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
  }

}
