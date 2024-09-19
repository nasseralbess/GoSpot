import React from 'react';
import Link from 'next/link';
import styles from '../styles/Header.module.css'; // Adjust the path if necessary

// Edit the navigation bar so that it is more spaced out
const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logo}>
          <Link href="/">GoSpot</Link>
        </div>
        <nav className={styles.nav}>
          <Link href="/" className={styles.navLink}>Solo</Link>
          <Link href="/group" className={styles.navLink}>Group</Link>
          <Link href="/aboutus" className={styles.navLink}>About Us</Link>
          <Link href="/save" className={styles.navLink}>Saved</Link>
          <Link href="/profile" className={styles.navLink}>Profile</Link>
          
        </nav>
      </div>
    </header>
  );
};

export default Header;
