import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { SignService } from '../../../services/sign/sign.service';
import { Router, RouterModule } from '@angular/router';
import { NgxMaskDirective, NgxMaskPipe } from 'ngx-mask';
import { showContainerAnimation } from '../../../animations/show-container.animation';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, RouterModule, NgxMaskDirective],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  animations: [showContainerAnimation]
})
export class RegisterComponent implements OnInit {

  public form!: FormGroup

  constructor(private formBuilder: FormBuilder, private signService: SignService, private router: Router){}

  ngOnInit(): void {
      this.form = this.formBuilder.group({
        firstName: ['', Validators.required],
        lastName: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        phone: ['', Validators.required],
        password: ['', Validators.required]
      })
  }

  public submit(){
    const dados = {firstName: this.form.value.firstName, lastName: this.form.value.lastName, email: this.form.value.email, phone: this.form.value.phone, password: this.form.value.password}
    this.signService.enviaDados(dados).subscribe({
      next: (res) => {
        this.router.navigate(['/login'])
      },
      error: (err) => {
        if (err.error.detail === 'account already exists') {
          document.querySelectorAll('span').forEach(span => {
            span.style.display = 'block';
          });
        }
      }
    })
  }
}
