import { Routes } from '@angular/router';
import { HomeComponent } from './components/pages/home/home.component';
import { LoginComponent } from './components/pages/login/login.component';
import { RegisterComponent } from './components/pages/register/register.component';

export const routes: Routes = [
    {path: '', redirectTo: '/login', pathMatch: 'full'},
    {path: 'login', component: LoginComponent, title: 'Login / STYLISH'},
    {path: 'register', component: RegisterComponent, title: 'registrar-se / STYLISH'},
    {path: 'home', component: HomeComponent, title: 'Home / STYLISH'},
];
