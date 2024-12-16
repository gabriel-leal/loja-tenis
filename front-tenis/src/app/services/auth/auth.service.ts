import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  constructor(private router: Router){}

  logout() {
    localStorage.clear();
    this.router.navigate(['/login'])    
  }

  isTokenExpired(token: string): boolean {
    const jwtDecode = (token: string) => JSON.parse(atob(token.split('.')[1]));
    const decodedToken: any = jwtDecode(token);
    return decodedToken.exp * 1000 < Date.now();
  }
}
