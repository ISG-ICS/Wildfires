import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {DropdownMenuComponent} from './dropdownMenu.component';

describe('DropdownMenuComponent', () => {
    let component: DropdownMenuComponent;
    let fixture: ComponentFixture<DropdownMenuComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [DropdownMenuComponent]
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(DropdownMenuComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
