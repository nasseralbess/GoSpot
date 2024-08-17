// src/app/components/RestaurantCard.tsx
import styles from '../styles/RestaurantCard.module.css';

const RestaurantCard = ({ restaurant }) => {
  return (
    <li className={styles.card}>
      <img src={restaurant.image_url} alt={restaurant.name} />
      <div className={styles.cardContent}>
        <h2 className={styles.cardTitle}>{restaurant.name}</h2>
        <p className={styles.cardDescription}>
          {restaurant.location.display_address.join(', ')}
        </p>
        <p>Phone: {restaurant.display_phone}</p>
        <p>Distance: {restaurant.distance.toFixed(2)} meters</p>
        <p>Transactions: {restaurant.transactions.join(', ')}</p>
        <a href={restaurant.url} target="_blank" rel="noopener noreferrer">
          Visit Yelp Page
        </a>
      </div>
    </li>
  );
};

export default RestaurantCard;
