import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthRoutingModule } from './auth-routing.module';
import { AuthComponent } from './auth.component';
import { LoginComponent } from './login/login.component';
import {MatCardModule} from '@angular/material/card';
import {ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatButtonModule} from '@angular/material/button';
import { RegisterComponent } from './register/register.component';
import { ForgetComponent } from './forget/forget.component';
import {MatIconModule} from '@angular/material/icon';
import { ResetComponent } from './reset/reset.component';
import {MatStepperModule} from '@angular/material/stepper';

const MODULES = [
  MatCardModule,
  MatInputModule,
  MatButtonModule,
  MatIconModule,
  MatStepperModule
];

@NgModule({
  declarations: [AuthComponent, LoginComponent, RegisterComponent, ForgetComponent, ResetComponent],
  imports: [
    CommonModule,
    AuthRoutingModule,
    ReactiveFormsModule,
    MODULES,
  ]
})
export class AuthModule { }
