import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideEnvironmentNgxMask} from 'ngx-mask'

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './interceptors/auth/auth.interceptor';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient(withInterceptors([authInterceptor])), provideEnvironmentNgxMask(), provideAnimationsAsync()]
};

export const LOCAL_STORAGE_KEYS = {
  TOKEN: 's6S4hQ47WF',
  NAME: 'FbhpLb7HZJ',
  EMAIL: 'FbdpLb9xZJ',
  ID: 'Z2tCujXnlZ'
};