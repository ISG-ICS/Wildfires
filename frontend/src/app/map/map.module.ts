import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {HeatmapComponent} from './heatmap/heatmap.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {TimeSeriesComponent} from './time-series/time-series.component';
import {TemperatureRangeSliderComponent} from './sidebar/temperature-range-slider/temperature-range-slider.component';
import {SearchComponent} from "./search-bar/search.component";
import {MatAutocompleteModule, MatFormFieldModule, MatInputModule} from "@angular/material";
import {MatSelectModule} from '@angular/material/select';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";


@NgModule({
    declarations: [HeatmapComponent, SidebarComponent, TimeSeriesComponent, TemperatureRangeSliderComponent, SearchComponent, SearchComponent],
    exports: [
        HeatmapComponent,
        SidebarComponent,
        TimeSeriesComponent,
        TemperatureRangeSliderComponent,
        SearchComponent
    ],
    imports: [
        CommonModule,
        LeafletModule,
        MatFormFieldModule,
        ReactiveFormsModule,
        MatAutocompleteModule,
        MatInputModule,
        FormsModule,
        MatSelectModule,
    ]
})
export class MapModule {
}
