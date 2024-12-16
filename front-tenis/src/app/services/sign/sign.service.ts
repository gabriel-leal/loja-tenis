import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SignService {

  public api = environment.apiBase

  constructor(private http: HttpClient) { }


  public enviaDados(dados: any): Observable<any> {
    return this.http.post(`${this.api}/sign`, dados)
  }
}
