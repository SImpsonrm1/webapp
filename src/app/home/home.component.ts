import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  duration: number = 30;
  description: string = '';
  musicUrl: string = '';
  imageUrl: string = '';
  isLoading = false;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  runModel(): void {
    this.isLoading = true;
    const payload = { duration: this.duration, description: this.description };
    this.http.post<any>('http://localhost:5000/generate-music', payload).subscribe(
      response => {
        this.musicUrl = `http://localhost:5000/generated/${response.file}.wav`;
        this.imageUrl = `http://localhost:5000/generated/${response.file}.png`;
        this.isNotLoading();
      },

      error => {
        console.error('Error occurred while calling API:', error);
      }

    );
  }
  isNotLoading(): boolean {
    return this.isLoading = false;
}
}
