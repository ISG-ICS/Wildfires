import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {LocationNameDisplayComponent} from './location-name-display.component';

describe('LocationNameDisplayComponent', () => {
    let component: LocationNameDisplayComponent;
    let fixture: ComponentFixture<LocationNameDisplayComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [LocationNameDisplayComponent]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(LocationNameDisplayComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
