import {Component, HostBinding, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {AppState} from '../../_store';
import {Store} from '@ngrx/store';
import { IIdentity} from '../../_models/IIdentity';
import {ApiService} from '../../_services/api.service';
import {catchError, map} from 'rxjs/operators';
import {Router} from '@angular/router';
import {of} from 'rxjs';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'gs2-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  @HostBinding('class') class = 'main-container dark-background';

  formCredentials = new FormGroup({
    passwords: new FormGroup({
      password: new FormControl('', Validators.required),
      passwordConfirm: new FormControl('', Validators.required),
    }, RegisterComponent.passwordMatchValidator),
    username: new FormControl('', {
      validators: Validators.required,
      asyncValidators: async () => this.loginMatchValidator,
      updateOn: 'blur'
    }),
  });
  formContact = new FormGroup({
    firstName: new FormControl('', Validators.required),
    lastName: new FormControl('', Validators.required),
    email: new FormControl('', Validators.compose([Validators.required, Validators.email])),
    phone: new FormControl('', Validators.required),
  });
  formAddress = new FormGroup({
    street: new FormControl('', Validators.required),
    street2: new FormControl('', Validators.required),
    postcode: new FormControl('', Validators.required),
    city: new FormControl('', Validators.required),
    country: new FormControl('', Validators.required),
  });
  formOthers = new FormGroup({
    companyName: new FormControl('', Validators.required),
  });

  get passwords() {
    return this.formCredentials.get('passwords');
  }

  get username() {
    return this.formCredentials.get('username');
  }

  get firstName() {
    return this.formContact.get('firstName');
  }

  get lastName() {
    return this.formContact.get('lastName');
  }

  get email() {
    return this.formContact.get('email');
  }

  get street() {
    return this.formAddress.get('street');
  }

  get street2() {
    return this.formAddress.get('street2');
  }

  get postcode() {
    return this.formAddress.get('postcode');
  }

  get city() {
    return this.formAddress.get('city');
  }

  get country() {
    return this.formAddress.get('country');
  }

  get companyName() {
    return this.formOthers.get('companyName');
  }

  get phone() {
    return this.formContact.get('phone');
  }

  get password() {
    return this.formCredentials.get('passwords')?.get('password');
  }

  get passwordConfirm() {
    return this.formCredentials.get('passwords')?.get('passwordConfirm');
  }

  constructor(private store: Store<AppState>, private apiService: ApiService,
              private router: Router,
              private snackBar: MatSnackBar,
  ) {
  }

  private static passwordMatchValidator(g: FormGroup) {
    const passValue = g.get('password')?.value;
    const passConfirmValue = g.get('passwordConfirm')?.value;
    return passValue === passConfirmValue ? null : {mismatch: true};
  }

  ngOnInit(): void {
  }

  submit() {
    if (this.formCredentials.valid && this.formContact.valid && this.formAddress.valid && this.formOthers.valid) {
      const user: IIdentity = {
        password1: this.password?.value,
        password2: this.passwordConfirm?.value,
        username: this.username?.value,
        first_name: this.firstName?.value,
        last_name: this.lastName?.value,
        email: this.email?.value,
        street: this.street?.value,
        street2: this.street2?.value,
        postcode: this.postcode?.value,
        city: this.city?.value,
        country: this.country?.value,
        company_name: this.companyName?.value,
        phone: this.phone?.value,
      };
      this.apiService.register(user)
        .pipe(
          catchError(errorXhr => {
            let message = '';
            for (const attr in errorXhr.error) {
              if (Array.isArray(errorXhr.error[attr])) {
                message += errorXhr.error[attr].join('\n');
              } else {
                message += errorXhr.error[attr];
              }
            }

            this.snackBar.open(message, 'Ok', {panelClass: 'notification-error'});
            return of(false);
          })
        )
        .subscribe(async (res) => {
          if (res) {
            await this.router.navigate(['/auth/login']);
          } else {
            this.formCredentials.markAsDirty();
            this.formContact.markAsDirty();
            this.formAddress.markAsDirty();
            this.formOthers.markAsDirty();
          }
        });
    }
  }


  private loginMatchValidator(g: FormGroup) {
    return this.apiService.checkLoginNotTaken(g.value && g.value.length > 0 && g.value.toLowerCase())
      .pipe(
        map(isAvailable => {
          return isAvailable.result ? {duplicate: true} : null;
        }));
  }
}
