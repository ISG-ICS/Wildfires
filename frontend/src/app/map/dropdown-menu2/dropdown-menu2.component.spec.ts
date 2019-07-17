import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DropdownMenu2Component } from './dropdown-menu2.component';

describe('DropdownMenu2Component', () => {
  let component: DropdownMenu2Component;
  let fixture: ComponentFixture<DropdownMenu2Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DropdownMenu2Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DropdownMenu2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
