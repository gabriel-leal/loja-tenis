import {HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { environment } from '../../environments/environment';
import { LOCAL_STORAGE_KEYS } from '../../app.config';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem(LOCAL_STORAGE_KEYS.TOKEN);
  const authService = inject(AuthService);
  const isSecureURL = req.url.includes(environment.apiBase);

  if (token && isSecureURL) {
    if (authService.isTokenExpired(token)) {
      console.error('Token expirado');
      authService.logout();
      return next(req);
    } else {
      const clonedReq = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`,
        },
      });
      return next(clonedReq)
    }
  }
  return next(req);
}