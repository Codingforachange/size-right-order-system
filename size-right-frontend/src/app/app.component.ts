import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OrderFormComponent } from './components/order-form/order-form.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, OrderFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'size-right-frontend';
}
