import React, { useState } from 'react';
import Modal from 'react-modal';
import styles from '../styles/RestaurantCard.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShareSquare, faBookmark, faStar } from '@fortawesome/free-solid-svg-icons';

const SavedPlace = ({ restaurant }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false); // State to control the restaurant details modal

  // Function to open the modal
  const openModal = () => {
    setModalIsOpen(true);
  };

  // Function to close the modal
  const closeModal = (event) => {
    event.stopPropagation(); 
    setModalIsOpen(false);
  };

  // Function to redirect to Google search
  const redirectToGoogleSearch = () => {
    const toEncode = restaurant.name + " New York";
    const query = encodeURIComponent(toEncode);
    const url = `https://www.google.com/search?q=${query}`;
    window.open(url, '_blank');
  };

  return (
    <li onClick={openModal} className={styles.card}>
      <div className={styles.cardImageWrapper}>
        <img src={restaurant.image_url} alt={restaurant.name} className={styles.cardImage} />
      </div>
      <div className={styles.cardContent}>
        <h2 className={styles.cardTitle}>{restaurant.name}</h2>
        <p className={styles.cardDescription}>
          {restaurant.location?.display_address ? 
            restaurant.location.display_address.join(', ') : 
            'Address not available'}
        </p>
        <button
          onClick={(event) => {
            event.stopPropagation();
            openModal();
          }}
          className={styles.moreDetailsButton}
        >
          More Details
        </button>
      </div>

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Restaurant Details Modal"
        className={styles.modal}
        overlayClassName={styles.modalOverlay}
      >
        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitle}>{restaurant.name}</h2>
          <button onClick={closeModal} className={styles.modalCloseButton}>&times;</button>
        </div>
        <div className={styles.modalContent}>
          <div className={styles.modalSection}>
            <p className={styles.cardDescription}>
              {restaurant.location?.display_address ? 
                restaurant.location.display_address.join(', ') : 
                'Address not available'}
            </p>
            <p>Phone: {restaurant.display_phone}</p>
            <p>Distance: {restaurant.distance.toFixed(2)} meters</p>
            <p>Transactions: {restaurant.transactions.join(', ')}</p>
          </div>
          <button
            onClick={redirectToGoogleSearch}
            className={styles.googleSearchButton}
          >
            Google Search
          </button>
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
            <button className={styles.modalButton}>
              <FontAwesomeIcon icon={faShareSquare} />
            </button>
            <button className={styles.modalButton}>
              <FontAwesomeIcon icon={faBookmark} />
            </button>
            <button className={styles.modalButton}>
              <FontAwesomeIcon icon={faStar} />
            </button>
          </div>
        </div>
      </Modal>
    </li>
  );
};

export default SavedPlace;
