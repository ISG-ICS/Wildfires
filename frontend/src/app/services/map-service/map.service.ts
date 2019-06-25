import { Injectable } from '@angular/core';
import * as $ from 'jquery';

@Injectable({
  providedIn: 'root'
})
export class MapService {

  constructor() { }

  processCSVData(allText, limit, delim= ',') {
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
          const tempData = that.processCSVData(data, 60000);
          const tempDataArray = [];
          const coorSet = new Set();
          const dailyCount = {};
          for (const entry of tempData) {
              const createAt = entry[6];

              if (dailyCount.hasOwnProperty(createAt)) {
                  dailyCount[createAt] = entry[8];
              } else {
                  dailyCount[createAt] = entry[8];
              }
              if (!coorSet.has(entry[3] + entry[4])) {
                  tempDataArray.push({lat: entry[3], lng: entry[4], temperature: entry[8]});
              }
              const station = entry[3] + entry[4];
              coorSet.add(station);
              if (heatData.hasOwnProperty(station)) {
                  heatData[station].push([new Date(createAt).getTime(), parseFloat(entry[8])]);
              } else {
                  heatData[station] = [[new Date(createAt).getTime(), parseFloat(entry[8])]];
              }

          }

          const testData = {
              max: 8,
              data: tempDataArray
          };

          $(window).trigger('heatDataLoaded', testData);
      });
  }

  getTweetsData(): void {

      const chartData = [];
      const tweetsPoint = [];
      const dailyCount = {};

      $.ajax({
          type: 'GET',
          url: 'http://127.0.0.1:5000/tweets',
          dataType: 'text',
      }).done(data => {

          const tempData = JSON.parse(data);
          const tweetData = [];
          tempData.forEach(entry => {

              const createAt = entry.create_at.split('T')[0];

              if (dailyCount.hasOwnProperty(createAt)) {
                  dailyCount[createAt]++;
              } else {
                  dailyCount[createAt] = 1;
              }

              const leftTop = [entry.lat, entry.long];
              tweetData.push(leftTop);
              tweetsPoint.push([new Date(createAt).getTime(), leftTop[0], leftTop[1]]);

          });



          // timebar
          Object.keys(dailyCount).sort().forEach(key => {
              chartData.push([new Date(key).getTime(), dailyCount[key]]);

          });

          $(window).trigger('tweetsLoaded', {tweetData});
      });
  }

}
