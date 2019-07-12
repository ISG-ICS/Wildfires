import {Component, EventEmitter, Input, OnInit} from '@angular/core';
import {MapService} from '../../../services/map-service/map.service';


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
        this.mapService.temperatureChangeEvent.emit({newTemperature: newValue});
    }

}


