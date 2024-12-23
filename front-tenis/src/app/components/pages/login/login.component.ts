import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';
import { Router, RouterModule } from '@angular/router';
import { jwtDecode } from 'jwt-decode';
import { LoginService } from '../../../services/login/login.service';
import { DecodedToken } from '../../../interfaces/decodedToken/decoded-token';
import { animate, query, style, transition, trigger } from '@angular/animations';
import { showContainerAnimation } from '../../../animations/show-container.animation';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  animations: [showContainerAnimation]  
})
export class LoginComponent implements OnInit {

  public form!: FormGroup

  constructor(private router: Router, private formBuilder: FormBuilder, private loginService: LoginService){}

  ngOnInit(): void {
    let token = localStorage.getItem(LOCAL_STORAGE_KEYS.TOKEN)
    if (token) {
      this.router.navigate(['/home'])
    } else {
      localStorage.clear()
      this.form = this.formBuilder.group({
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required]]
      })
    }
  }

  public submit(){
    const dados = {email: this.form.value.email, password: this.form.value.password}
    this.loginService.enviarDados(dados).subscribe({
      next: (res) => {
        let token = res.access_token
        localStorage.clear()
        localStorage.setItem(LOCAL_STORAGE_KEYS.TOKEN, token)
        const decoded = jwtDecode<DecodedToken>(token)
        localStorage.setItem(LOCAL_STORAGE_KEYS.NAME, decoded.name)
        localStorage.setItem(LOCAL_STORAGE_KEYS.EMAIL, decoded.email)
        localStorage.setItem(LOCAL_STORAGE_KEYS.ID, decoded.sub)
        this.router.navigate(['/home'])
      },
      error: (err) => {
        console.log('erro no login', err.error.detail)
        if(err.error.detail == "Invalid credentials"){
          document.querySelectorAll('span').forEach(span => {
            span.style.display = 'block';
          });
        }
      }
    })
  }

}
