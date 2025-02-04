import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { FooterComponent } from '../../footer/footer.component';
import { ProdutosService } from '../../../services/produtos/produtos.service';
import { CommonModule } from '@angular/common';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';
import { CarrinhoService } from '../../../services/carrinho/carrinho.service';
import { Router } from '@angular/router';
import { style } from '@angular/animations';
import { AuthService } from '../../../services/auth/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [HeaderComponent, FooterComponent, CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {

  produtos_array: any[] = []
  produtos: any[] = []
  carrinho_array: any[] = []
  carrinho: any[] = []
  total: number = 0
  public id: string = localStorage.getItem(LOCAL_STORAGE_KEYS.ID) ?? '';


  constructor(private produtosService: ProdutosService, private carrinhoService: CarrinhoService, private router: Router, private authservice: AuthService){}

  ngOnInit(): void {
    this.listaProdutos();
    this.listaCarrinho();
  }

  listaProdutos(): void {
    this.produtosService.listaProdutos().subscribe({
      next: (res) => {
        this.produtos_array = res.content;
        this.produtos = res;
      },
      error: (err) => {
        console.log('Erro ao listar produtos:', err);
      }
    });
  }

  listaCarrinho(): void {
    this.total = 0;
    this.carrinhoService.listaCarrinho(this.id).subscribe({
      next: (res) => {
        this.carrinho_array = res.content;
        this.carrinho = res;
        this.carrinho_array.forEach((element: any) => {
          this.total += element.preco;
        });
      },
      error: (err) => {
        console.log('Erro ao listar carrinho:', err);
      }
    });
  }

  public submit(index: number): void {
    const produto = this.produtos_array[index];
    const dados = { id: this.id, qtd_compra: 1 };
    this.carrinhoService.addCarrinho(dados, produto.sku).subscribe({
      next: (res) => {
        this.listaCarrinho();
      },
      error: (err) => {
        console.log('Erro ao adicionar produto ao carrinho:', err);
      }
    });
  }

  public deleteCart(): void {
    this.carrinhoService.deleteCarrinho(this.id).subscribe({
      next: (res) => {
        console.log(res)
        window.location.reload()
      },
      error: (err) => {
        console.log(err)
      }
    })}

    public compra(): void {
      const backdrop = document.querySelector('.modal-backdrop.fade') as HTMLElement;
      if (backdrop) {
          backdrop.style.opacity = '0';
      }
      this.router.navigate(['/checkout'])
    }

    public isLogged(): boolean {
      let id = localStorage.getItem(LOCAL_STORAGE_KEYS.ID);
      if (!id) {
          return false;
      }
      return true;
    }

    public logout() {
      this.authservice.logout()
    }
}
