import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms' 
import { HttpClient } from '@angular/common/http'
import { Subscription } from 'rxjs'
// import { format } from 'path';

@Component({
  selector: 'app-ordermatchingsystem',
  templateUrl: './ordermatchingsystem.component.html',
  styleUrls: ['./ordermatchingsystem.component.css']
})
export class OrdermatchingsystemComponent implements OnInit {

//  subscription: Subscription
//  constructor(private http: HttpClient) {
//    this.subscription = this.http.get('/realtimedata').subscribe(
//      data => {
//        console.log(data);
//      }
//    )
//   }
  ngOnInit(): void {
  }
  price: string;
  nprice: any;
  form = <HTMLFormElement>document.getElementById("newOrderForm");

  limit_market_price(value: string){
    if(value === 'market'){
      (<HTMLInputElement>document.getElementById("price")).disabled = true;
      (<HTMLInputElement>document.getElementById("price")).type = "hidden";
      (<HTMLInputElement>document.getElementById("priceLabel")).hidden = true;
      this.price = "200";
    }
    else {
      (<HTMLInputElement>document.getElementById("price")).disabled = false;
      (<HTMLInputElement>document.getElementById("price")).type = "show";
      (<HTMLInputElement>document.getElementById("priceLabel")).hidden = false;
      (<HTMLInputElement>document.getElementById("price")).value = "";
    }
  }
  display_order_placed(){
    console.log(this.price);
    this.nprice = parseFloat(this.price);
    console.log(this.nprice);
    if((this.nprice >= 190) && (this.nprice <=210)) {
      document.forms["newOrderForm"].submit();
      alert("Your order is placed! The success/failure of your order will be reflected soon!")
      //this.form.submit();
     }
     else {
       alert("Price not in circuit band.");
     }

    console.log(this.nprice);
  }
}
