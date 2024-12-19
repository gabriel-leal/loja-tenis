import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { FooterComponent } from '../../footer/footer.component';
import { ProdutosService } from '../../../services/produtos/produtos.service';
import { CommonModule } from '@angular/common';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';

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

  constructor(private produtosService: ProdutosService){}

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
  }

  public submit(index: number){
    const produto = this.produtos_array[index]
    const id = localStorage.getItem(LOCAL_STORAGE_KEYS.ID)
    console.log({id, produto})
  }

}
