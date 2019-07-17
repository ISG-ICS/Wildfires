import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dropdown-menu3',
  templateUrl: './dropdown-menu3.component.html',
  styleUrls: ['./dropdown-menu3.component.css']
})
export class DropdownMenu3Component implements OnInit {
  private showMenu = 0;
  constructor() { }

  ngOnInit() {
  }

  expand = () => {
  if (this.showMenu === 0) {
    document.getElementById('menu').style.transform = 'scale(3)';
    document.getElementById('plus').style.transform = 'rotate(45deg)';
    this.showMenu = 1;
  } else {
    document.getElementById('menu').style.transform = 'scale(0)';
    document.getElementById('plus').style.transform = 'rotate(0deg)';
    this.showMenu = 0;
  }
}

}
