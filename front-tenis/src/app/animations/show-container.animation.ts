import { animate, style, transition, trigger } from "@angular/animations";

export const showContainerAnimation = trigger('showContainer', [
      transition(':enter', [
        style({
          opacity: 0,
          transform: 'translateY(-100px)', 
        }),
        animate('700ms ease-out', style({
          opacity: 1,
          transform: 'translateY(0)',
        })),
      ]),
    ])