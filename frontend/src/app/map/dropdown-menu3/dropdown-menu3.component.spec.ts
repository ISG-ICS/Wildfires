import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DropdownMenu3Component } from './dropdown-menu3.component';

describe('DropdownMenu3Component', () => {
  let component: DropdownMenu3Component;
  let fixture: ComponentFixture<DropdownMenu3Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DropdownMenu3Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DropdownMenu3Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
