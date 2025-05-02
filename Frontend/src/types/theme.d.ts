import '@emotion/react';

declare module '@emotion/react' {
  export interface Theme {
    colors: {
      background: string;
      text: string;
      primary: string;
      secondary: string;
      accent: string;
      gradient: string;
    };
  }
} 