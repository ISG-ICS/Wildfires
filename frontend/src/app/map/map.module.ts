import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {HeatmapComponent} from './heatmap/heatmap.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {TimeSeriesComponent} from './time-series/time-series.component';
import {TemperatureRangeSliderComponent} from './sidebar/temperature-range-slider/temperature-range-slider.component';

@NgModule({
    declarations: [HeatmapComponent, SidebarComponent, TimeSeriesComponent, TemperatureRangeSliderComponent],
    exports: [
        HeatmapComponent,
        SidebarComponent,
        TimeSeriesComponent,
        TemperatureRangeSliderComponent
    ],
    imports: [
        CommonModule,
        LeafletModule
    ]
})
export class MapModule {
}
