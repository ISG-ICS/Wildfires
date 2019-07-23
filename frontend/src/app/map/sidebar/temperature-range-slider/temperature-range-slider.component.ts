import {Component, OnInit} from '@angular/core';
import {MapService} from '../../../services/map-service/map.service';
import 'nouislider/distribute/nouislider.css';


@Component({
    selector: 'app-temperature-range-slider',
    templateUrl: './temperature-range-slider.component.html',
    styleUrls: ['./temperature-range-slider.component.css']
})
export class TemperatureRangeSliderComponent implements OnInit {
    units = {
        Celcius: '°C',
        Fahrenheit: '°F'
    };

    config = {
        minTemp: -6,
        maxTemp: 35,
        unit: 'Celcius'
    };

    ngOnInit() {
        const slider = document.getElementById('slider');
    }

    constructor(private mapService: MapService) {

    }

    setTemperature = (newValue) => {
        //
        const temperature = document.getElementById('temperature');
        temperature.style.height = (newValue - this.config.minTemp) / (this.config.maxTemp - this.config.minTemp) * 100 + '%';
        temperature.dataset.value = newValue + this.units[this.config.unit];
    };

    highTemperatureSelectorUpdate = (event) => {
        const newValue = event.target.value;

        this.setTemperature(newValue);
        this.mapService.temperatureChangeEvent.emit({high: Number(newValue)});
    };

    lowTemperatureSelectorUpdate = (event) => {
        const newValue = event.target.value;
        this.setTemperature(newValue);
        this.mapService.temperatureChangeEvent.emit({low: Number(newValue)});
    }


}


