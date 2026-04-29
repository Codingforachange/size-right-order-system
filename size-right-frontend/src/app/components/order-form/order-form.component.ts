import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { saveAs } from 'file-saver';

interface Product {
  wearerFunction: string;
  productCode: string;
  size: string;
  issueQty: number;
  price: number;
  emblemId: string;
}

interface Wearer {
  lkr: string;
  firstName: string;
  lastName: string;
  products: Product[];
}

interface FSItem {
  fsOrderType: string;
  description: string;
  productCode: string;
  billingMethod: string;
  price: number;
  abusEnabled: boolean;
  abusName: string;
  abusEmpNum: string;
  systematicReplace: boolean;
  replacePercent: number;
  replaceRate: number;
  orderMethod: string;
  soilCounted: string;
  circulatingQty: number;
  deliveryScheme: string;
  deliveryVarEnabled: boolean;
  deliveryVarType: string;
}

@Component({
  selector: 'app-order-form',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './order-form.component.html',
  styleUrls: ['./order-form.component.css']
})
export class OrderFormComponent {
  orderData = {
    customerNumber: '',
    customerName: '',
    location: '',
    date: new Date().toLocaleDateString(),
    facilityItems: [] as FSItem[],
    wearers: [] as Wearer[]
  };

  constructor(private http: HttpClient) {}

  addFacilityItem() {
    this.orderData.facilityItems.push({
      fsOrderType: 'New Product',
      description: '',
      productCode: '',
      billingMethod: 'Inventory Based',
      price: 0,
      abusEnabled: false,
      abusName: '',
      abusEmpNum: '',
      systematicReplace: false,
      replacePercent: 0,
      replaceRate: 0,
      orderMethod: 'Delayed Even Exchange',
      soilCounted: 'Manual',
      circulatingQty: 0,
      deliveryScheme: 'Weekly',
      deliveryVarEnabled: false,
      deliveryVarType: 'Full'
    });
  }

  removeFacilityItem(index: number) { this.orderData.facilityItems.splice(index, 1); }

  addWearer() { this.orderData.wearers.push({ lkr: '', firstName: '', lastName: '', products: [] }); }

  removeWearer(index: number) { this.orderData.wearers.splice(index, 1); }

  addProduct(wearerIndex: number) {
    this.orderData.wearers[wearerIndex].products.push({
      wearerFunction: '', productCode: '', size: '', issueQty: 0, price: 0, emblemId: ''
    });
  }

  removeProduct(wearerIndex: number, productIndex: number) {
    this.orderData.wearers[wearerIndex].products.splice(productIndex, 1);
  }

  resetForm() {
    if (confirm("Clear all order information?")) {
      this.orderData = {
        customerNumber: '',
        customerName: '',
        location: '',
        date: new Date().toLocaleDateString(),
        facilityItems: [],
        wearers: []
      };
    }
  }

  processOrder() {
    this.http.post('https://size-right-backend.onrender.com/generate-pdf', this.orderData, { responseType: 'blob' })
    .subscribe(blob => saveAs(blob, `UniFirst_Order_${this.orderData.customerNumber || 'Draft'}.pdf`));
  }
}
