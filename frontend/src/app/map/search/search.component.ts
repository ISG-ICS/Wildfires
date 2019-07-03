import {Component, Input, OnInit} from '@angular/core';
import {MapService} from '../../services/map-service/map.service';
declare let L;


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  private map;
  constructor( private mapService: MapService) { }

  ngOnInit() {
    this.mapService.mapLoaded.subscribe( (map) => {
      this.map = map;
    });
  }

  keywordSearch = (event) => {
    if (event.key === 'Enter') {
      console.log(event.target.value);
      this.map.setView(L.latLng(34.0, -118.5), 9);
    }
  }

}
