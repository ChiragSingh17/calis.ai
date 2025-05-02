import '@emotion/react';
import { Theme } from '@emotion/react';

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

const theme: Theme = {
  colors: {
    background: '#1a1a1a',
    text: '#ffffff',
    primary: '#ff6b6b',
    secondary: '#4ecdc4',
    accent: '#ffd166',
    gradient: 'linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%)'
  }
};

export default theme; 