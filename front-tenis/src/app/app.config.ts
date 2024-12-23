import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideEnvironmentNgxMask} from 'ngx-mask'

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './interceptors/auth/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient(withInterceptors([authInterceptor])), provideEnvironmentNgxMask()]
};

export const LOCAL_STORAGE_KEYS = {
  TOKEN: 's6S4hQ47WF',
  NAME: 'FbhpLb7HZJ',
  EMAIL: 'FbdpLb9xZJ',
  ID: 'Z2tCujXnlZ'
};