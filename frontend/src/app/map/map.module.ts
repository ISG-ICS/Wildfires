import {Input, NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {HeatmapComponent} from './heatmap/heatmap.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { TimeSeriesComponent } from './time-series/time-series.component';
import {SearchComponent} from './search/search.component';

@NgModule({
  declarations: [HeatmapComponent, SidebarComponent, TimeSeriesComponent, SearchComponent],
  exports: [
    HeatmapComponent,
    SidebarComponent,
    TimeSeriesComponent,
    SearchComponent
  ],
  imports: [
    CommonModule,
    LeafletModule
  ]
})
export class MapModule {}
