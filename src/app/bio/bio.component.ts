import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-bio',
  templateUrl: './bio.component.html',
  styleUrls: ['./bio.component.css']
})
export class BioComponent implements OnInit {

  teamMembers = [
    {
      name: 'Ryan Simpson',
      photo: 'assets/headshot.jpg',
      description: 'Hi I\'m Ryan. I\'m a student software developer. at Appalachian state university.'
    },
    {
      name: 'Alex Somer',
      photo: 'path/to/photo2.jpg',
      description: 'This is member 2.'
    },

  ];

  constructor() { }

  ngOnInit(): void {
  }

}
