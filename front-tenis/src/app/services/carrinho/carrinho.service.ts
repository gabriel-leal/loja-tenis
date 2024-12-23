import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CarrinhoService {

  api = environment.apiBase

  constructor(private http: HttpClient) { }

  public addCarrinho(dados: any, sku: string): Observable<any> {
    return this.http.post(`${this.api}/cart/${sku}`, dados)
  }
  
  
  public listaCarrinho(id: string): Observable<any>{
    return this.http.get(`${this.api}/cart/${id}`)
  }
}
