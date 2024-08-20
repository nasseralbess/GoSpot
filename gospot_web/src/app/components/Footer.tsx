import React from 'react';
import Link from 'next/link';
import styles from '../styles/Footer.module.css'; // Adjust the path if necessary

const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContainer}>
        <div className={styles.footerLogo}>
          <Link href="/">
            GoSpot
          </Link>
        </div>
        <nav className={styles.footerNav}>
          <Link href="/privacy-policy">Privacy Policy</Link>
          <Link href="/terms-of-service">Terms of Service</Link>
          <Link href="/contact-us">Contact Us</Link>
        </nav>
        <div className={styles.footerText}>
          © 2024 GoSpot. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
