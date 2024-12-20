import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { FooterComponent } from '../../footer/footer.component';
import { ProdutosService } from '../../../services/produtos/produtos.service';
import { CommonModule } from '@angular/common';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';
import { CarrinhoService } from '../../../services/carrinho/carrinho.service';

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


  constructor(private produtosService: ProdutosService, private carrinhoService: CarrinhoService){}

  ngOnInit(): void {
    this.produtosService.listaProdutos().subscribe({
      next: (res) => {
        this.produtos_array = res.content
        this.produtos = res
      },
      error: (err) => {
        console.log(err)
      }
    })
    this.carrinhoService.listaCarrinho(this.id).subscribe({
      next: (res) => {
        this.carrinho_array = res.content
        this.carrinho = res
        this.carrinho_array.forEach(element => {
          this.total = this.total + element.preco
        });
      },
      error: (err) => {
        console.log(err)
      }
    })
  }

  public submit(index: number){
    const produto = this.produtos_array[index]
    console.log(this.id, produto)
  }
}
