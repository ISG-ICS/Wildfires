import {Input, NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import {HeatmapComponent} from './heatmap/heatmap.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {TimeSeriesComponent} from './time-series/time-series.component';
import {DropdownMenuComponent} from './dropdown-menu/dropdown-menu.component';
import {DropdownMenu2Component} from './dropdown-menu2/dropdown-menu2.component';
import {DropdownMenu3Component} from './dropdown-menu3/dropdown-menu3.component';

@NgModule({
  declarations: [HeatmapComponent, SidebarComponent, TimeSeriesComponent, DropdownMenuComponent,
    DropdownMenu2Component, DropdownMenu3Component],
  exports: [
    HeatmapComponent,
    SidebarComponent,
    TimeSeriesComponent,
    DropdownMenuComponent,
    DropdownMenu2Component,
    DropdownMenu3Component,
  ],
  imports: [
    CommonModule,
    LeafletModule
  ]
})
export class MapModule {
}
