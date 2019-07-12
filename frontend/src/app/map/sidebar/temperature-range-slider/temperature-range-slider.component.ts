import {Component, EventEmitter, Input, OnInit} from '@angular/core';
import {MapService} from '../../../services/map-service/map.service';
import noUiSlider from 'nouislider';
import 'nouislider/distribute/nouislider.css';


@Component({
    selector: 'app-temperature-range-slider',
    templateUrl: './temperature-range-slider.component.html',
    styleUrls: ['./temperature-range-slider.component.css']
})
export class TemperatureRangeSliderComponent implements OnInit {
          const units = {
          Celcius: '°C',
          Fahrenheit: '°F' };

          const config = {
          minTemp: -6,
          maxTemp: 35,
          unit: 'Celcius' };

    ngOnInit() {
        const slider = document.getElementById('slider');
        noUiSlider.create(slider, {
            start: [4000],
            range: {
            min: [1],
            max: [10000]
        }
        });

    }

    constructor(private mapService: MapService) {

    }

   setTemperature = (newValue) => {
          const range = document.querySelector('input[type=\'range\']');
          const temperature = document.getElementById('temperature');
          temperature.style.height = (newValue - this.config.minTemp) / (this.config.maxTemp - this.config.minTemp) * 100 + '%';
          temperature.dataset.value = newValue + this.units[this.config.unit];
    }

    temperatureRangeChange = (event) => {
        const newValue = event.target.value;
        const range = document.querySelector('input[type=\'range\']');
        this.setTemperature(newValue);
        this.mapService.temperatureChangeEvent.emit({newTemperature: Number(newValue)});
    }

    temperatureRangeChange2 = (event) => {
        const newValue = event.target.value;
        const range = document.querySelector('input[type=\'range\']');
        this.setTemperature(newValue);
        this.mapService.temperatureChangeEvent.emit({newTemperature2: Number(newValue)});
    }


}


