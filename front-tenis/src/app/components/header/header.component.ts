import { Component } from '@angular/core';
import { LOCAL_STORAGE_KEYS } from '../../app.config';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {

  constructor(){}

  public logout(){
    localStorage.clear()
    window.location.reload()
  }

  public isLogged(): boolean {
    let id = localStorage.getItem(LOCAL_STORAGE_KEYS.ID);
    if (!id) {
        return false;
    }
    return true;
}
}
