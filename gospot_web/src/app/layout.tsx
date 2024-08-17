// src/app/layout.tsx
import { ReactNode } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import './styles/globals.css';
import './styles/theme.css';

const Layout = ({ children }: { children: ReactNode }) => {
  return (
    <>
      {/* <Header /> */}
      <main>{children}</main>
      {/* <Footer /> */}
    </>
  );
};

export default Layout;
