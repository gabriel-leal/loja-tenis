import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';
import { Login } from '../../interfaces/login/login';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  public api = environment.apiBase

  constructor(private http: HttpClient) { }

  public enviarDados(dados: Login): Observable<any> {
    return this.http.post(`${this.api}/login`, dados)
  }

}
