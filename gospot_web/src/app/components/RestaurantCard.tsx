import React, { useState, useRef } from 'react';
import Modal from 'react-modal';
import styles from '../styles/RestaurantCard.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShareSquare, faBookmark, faStar } from '@fortawesome/free-solid-svg-icons'; // Import icons

const RestaurantCard = ({ restaurant }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const timerRef = useRef(null);

  const openModal = () => {
    setModalIsOpen(true);
    timerRef.current = Date.now();
  };

  const closeModal = async () => {
    const timeSpent = (Date.now() - timerRef.current) / 1000;
    setModalIsOpen(false);

    console.log(`User viewed ${restaurant.name} for ${timeSpent} seconds.`);

    // Uncomment the code below to send view time data to the backend
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

  const handleShare = () => {
    // Implement share functionality
    console.log('Share button clicked');
  };

  const handleSave = () => {
    // Implement save functionality
    console.log('Save to My Places button clicked');
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
        <button onClick={openModal} className={styles.moreDetailsButton}>
          More Details
        </button>
      </div>

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Restaurant Details Modal"
        className={styles.modal} // Apply custom modal styles
        overlayClassName={styles.modalOverlay} // Apply custom overlay styles
      >
        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitle}>{restaurant.name}</h2>
          <button onClick={closeModal} className={styles.modalCloseButton}>
            &times;
          </button>
        </div>
        <div className={styles.modalContent}>
          <div className={styles.modalSection}>
            <p className={styles.modalAddress}>{restaurant.location.display_address.join(', ')}</p>
            <p>Phone: {restaurant.display_phone}</p>
            <p>Distance: {restaurant.distance.toFixed(2)} meters</p>
            <p>Transactions: {restaurant.transactions.join(', ')}</p>
          </div>
        </div>
        <div className={styles.modalFooter}>
          <a
            href={restaurant.url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.modalCtaButton}
          >
            Visit Yelp Page
          </a>
          <div className={styles.modalButtons}>
            <button onClick={handleShare} className={styles.modalButton}>
              <FontAwesomeIcon icon={faShareSquare} />
            </button>
            <button onClick={handleSave} className={styles.modalButton}>
              <FontAwesomeIcon icon={faBookmark} />
            </button>
            <a
              href={restaurant.url}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.modalButton}
            >
              <FontAwesomeIcon icon={faStar} />
            </a>
          </div>
        </div>
      </Modal>
    </li>
  );
};

export default RestaurantCard;
