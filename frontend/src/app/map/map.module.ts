import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {HeatmapComponent} from './heatmap/heatmap.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {TimeSeriesComponent} from './time-series/time-series.component';
import {TabGroupComponent} from './tab/tab.component';
import {TemperatureRangeSliderComponent} from './sidebar/temperature-range-slider/temperature-range-slider.component';
import {SearchComponent} from './search-bar/search.component';
import {MatAutocompleteModule, MatFormFieldModule, MatInputModule, MatTabsModule} from '@angular/material';
import {MatSelectModule} from '@angular/material/select';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {LocationNameDisplayComponent} from './location-name-display/location-name-display.component';

@NgModule({
    declarations: [HeatmapComponent, SidebarComponent, TimeSeriesComponent,
        TemperatureRangeSliderComponent, SearchComponent, SearchComponent,
        LocationNameDisplayComponent, TabGroupComponent],
    exports: [
        HeatmapComponent,
        SidebarComponent,
        TimeSeriesComponent,
        TemperatureRangeSliderComponent,
        SearchComponent,
        TabGroupComponent,
        LocationNameDisplayComponent
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
        MatTabsModule,

    ],
})
export class MapModule {
    constructor() {
    }
}
