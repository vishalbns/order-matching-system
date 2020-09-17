import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrdermatchingsystemComponent } from './ordermatchingsystem.component';

describe('OrdermatchingsystemComponent', () => {
  let component: OrdermatchingsystemComponent;
  let fixture: ComponentFixture<OrdermatchingsystemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrdermatchingsystemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrdermatchingsystemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
