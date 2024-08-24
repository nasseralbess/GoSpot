// src/app/components/RestaurantCard.tsx
import React from 'react';
import styles from '../styles/RestaurantCard.module.css';

const RestaurantCard = ({ restaurant }) => {
  const handleClose = () => {
    // Logic to handle card close (e.g., setting state to hide the card)
    console.log('Close card');
  };

  return (
    <li className={styles.card}>
      <div className={styles.closeButton} onClick={handleClose}>
        &times; {/* Unicode for "X" mark */}
      </div>
      <div className={styles.cardImageWrapper}>
        <img src={restaurant.image_url} alt={restaurant.name} className={styles.cardImage} />
      </div>
      <div className={styles.cardContent}>
        <h2 className={styles.cardTitle}>{restaurant.name}</h2>
        <p className={styles.cardDescription}>
          {restaurant.location.display_address.join(', ')}
        </p>
        <p>Phone: {restaurant.display_phone}</p>
        <p>Distance: {restaurant.distance.toFixed(2)} meters</p>
        <p>Transactions: {restaurant.transactions.join(', ')}</p>
        <a href={restaurant.url} target="_blank" rel="noopener noreferrer" className={styles.ctaButton}>
          Visit Yelp Page
        </a>
        <a href={`/restaurants/${restaurant.id}`} className={styles.moreDetailsButton}>
          More Details
        </a>
      </div>
    </li>
  );
};

export default RestaurantCard;
