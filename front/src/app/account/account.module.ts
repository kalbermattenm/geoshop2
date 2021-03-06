import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {AccountRoutingModule} from './account-routing.module';
import {AccountComponent} from './account.component';
import {NewOrderComponent} from './new-order/new-order.component';
import {MatStepperModule} from '@angular/material/stepper';
import {ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatIconModule} from '@angular/material/icon';
import {MatCardModule} from '@angular/material/card';
import {MatTableModule} from '@angular/material/table';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSortModule} from '@angular/material/sort';
import {OrdersComponent} from './orders/orders.component';
import {MatDividerModule} from '@angular/material/divider';
import {SharedModule} from '../shared/shared.module';
import { ProfileComponent } from './profile/profile.component';
import {ScrollingModule} from '@angular/cdk/scrolling';

const MODULES = [
  ReactiveFormsModule,
  MatStepperModule,
  MatButtonModule,
  MatFormFieldModule,
  MatSelectModule,
  MatInputModule,
  MatAutocompleteModule,
  MatIconModule,
  MatCardModule,
  MatTableModule,
  MatPaginatorModule,
  MatSortModule,
  MatDividerModule,
  MatAutocompleteModule,
  ScrollingModule,
  MatStepperModule
];

@NgModule({
  declarations: [AccountComponent, NewOrderComponent, OrdersComponent, ProfileComponent],
  imports: [
    CommonModule,
    AccountRoutingModule,
    MODULES,
    SharedModule
  ]
})
export class AccountModule {
}
