import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dropdown-menu2',
  templateUrl: './dropdown-menu2.component.html',
  styleUrls: ['./dropdown-menu2.component.css']
})
export class DropdownMenu2Component implements OnInit {

  constructor() { }

  ngOnInit() {
  }
  displayHeatLayer = () => {
    console.log('Haha');
    /*displayHeatLayer = () => {
    this.mapService.heatLayerClickEvent.emit();*/
  }
}
