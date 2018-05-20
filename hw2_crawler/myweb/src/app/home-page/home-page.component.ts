import { Component, OnInit, Input } from '@angular/core';
import { Query } from '@angular/compiler/src/core';

import { AppComponent } from '../app.component';
import { SearchQuery } from '../query' ;

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {
  query : SearchQuery ={
    name:'' 
  };


  constructor() { }

  ngOnInit() {
  }

}
