import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import App from './app';

ReactDOM.createRoot(document.getElementById('react-component')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
