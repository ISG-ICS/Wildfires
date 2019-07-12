import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TemperatureRangeSliderComponent } from './temperature-range-slider.component';

describe('TemperatureRangeSliderComponent', () => {
  let component: TemperatureRangeSliderComponent;
  let fixture: ComponentFixture<TemperatureRangeSliderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TemperatureRangeSliderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TemperatureRangeSliderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
