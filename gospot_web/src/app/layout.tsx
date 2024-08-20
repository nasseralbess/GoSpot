// src/app/layout.tsx
import { ReactNode } from 'react';
import './styles/globals.css';
import './styles/theme.css';
import Header from './components/Header';
import Footer from './components/Footer';

const Layout = ({ children }: { children: ReactNode }) => {
  return (
    <>
      <Header /> 
      <main>{children}</main>
      <Footer /> 
    </>
  );
};

export default Layout;
