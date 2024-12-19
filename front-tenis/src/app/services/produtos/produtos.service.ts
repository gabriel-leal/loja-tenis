import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProdutosService {

  public api = environment.apiBase
  
  constructor(private http: HttpClient) { }

  public listaProdutos(): Observable<any> {
    return this.http.get(`${this.api}/products`)
  }
}
