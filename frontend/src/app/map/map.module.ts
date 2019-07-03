import {Input, NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {HeatmapComponent} from './heatmap/heatmap.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { TimeSeriesComponent } from './time-series/time-series.component';

@NgModule({
  declarations: [HeatmapComponent, SidebarComponent, TimeSeriesComponent],
  exports: [
    HeatmapComponent,
    SidebarComponent,
    TimeSeriesComponent,
  ],
  imports: [
    CommonModule,
    LeafletModule
  ]
})
export class MapModule {}
