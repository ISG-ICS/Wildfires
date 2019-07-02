import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';


import {MapModule} from './map/map.module';
import {AppComponent} from './app.component';
import { SearchComponent } from './map/search/search.component';

@NgModule({
  declarations: [
    AppComponent,
    SearchComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MapModule,

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
