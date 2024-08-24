import React, { useState, useRef } from 'react';
import Modal from 'react-modal';
import styles from '../styles/RestaurantCard.module.css';
import { fetchData } from '../utils/fetchData'; // Ensure this is correctly imported

const RestaurantCard = ({ restaurant }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const timerRef = useRef(null); // Use useRef to persist the timer value

  const openModal = () => {
    setModalIsOpen(true);
    timerRef.current = Date.now(); // Store the current time in the ref
  };

  const closeModal = async () => {
    const timeSpent = (Date.now() - timerRef.current) / 1000; // Calculate time in seconds
    setModalIsOpen(false);

    console.log(`User viewed ${restaurant.name} for ${timeSpent} seconds.`);

    // Send view time data to the backend
    // try {
    //   await fetchData('http://127.0.0.1:8080/user/store-view-time', 'POST', {}, {
    //     user_id: 1, // Replace with actual user ID
    //     restaurant_id: restaurant._id,
    //     view_time: timeSpent,
    //   });
    // } catch (error) {
    //   console.error('Error storing view time:', error.message);
    // }
  };

  return (
    <li className={styles.card}>
      <div className={styles.closeButton} onClick={() => console.log('Close card')}>
        &times;
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
        <button onClick={openModal} className={styles.moreDetailsButton}>
          More Details
        </button>
      </div>

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Restaurant Details Modal"
        style={{
          content: {
            top: '50%',
            left: '50%',
            right: 'auto',
            bottom: 'auto',
            marginRight: '-50%',
            transform: 'translate(-50%, -50%)',
          },
        }}
      >
        <h2>{restaurant.name}</h2>
        <p>{restaurant.location.display_address.join(', ')}</p>
        <p>Phone: {restaurant.display_phone}</p>
        <p>Distance: {restaurant.distance.toFixed(2)} meters</p>
        <p>Transactions: {restaurant.transactions.join(', ')}</p>
        <a href={restaurant.url} target="_blank" rel="noopener noreferrer">
          Visit Yelp Page
        </a>
        <button onClick={closeModal}>Close</button>
      </Modal>
    </li>
  );
};

export default RestaurantCard;
