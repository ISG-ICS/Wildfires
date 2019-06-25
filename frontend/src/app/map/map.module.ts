import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {HeatmapComponent} from './heatmap/heatmap.component';

@NgModule({
  declarations: [HeatmapComponent],
  exports: [
    HeatmapComponent
  ],
  imports: [
    CommonModule,
    LeafletModule
  ]
})
export class MapModule { }
