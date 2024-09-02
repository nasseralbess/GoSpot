import React, { useState, useRef, useEffect } from 'react';
import Modal from 'react-modal';
import styles from '../styles/RestaurantCard.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShareSquare, faBookmark, faStar } from '@fortawesome/free-solid-svg-icons';

const RestaurantCard = ({ restaurant, onSelection, isSelected,index }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false); // State to control the restaurant details modal
  const [totalTimeSpent, setTotalTimeSpent] = useState(0); // Track the total time spent viewing the card
  const [selection, setSelection] = useState(null); // Track if the user has selected check or X
  const [cardClass, setCardClass] = useState(styles.card); // Track the CSS class applied to the card
  const timerRef = useRef(null); // Ref to track when the user starts viewing details

  // Function to open the modal and start the timer
  const openModal = () => {
    setModalIsOpen(true);
    timerRef.current = Date.now(); // Start timing when the modal opens
  };

  // Function to close the modal and stop the timer
  const closeModal = (event) => {
    event.stopPropagation(); // Prevent the click event from bubbling up
    const timeSpent = (Date.now() - timerRef.current) / 1000; // Calculate time spent in seconds
    setTotalTimeSpent((prevTime) => prevTime + timeSpent); // Update total time spent
    setModalIsOpen(false);
  };

  // Function to handle user's selection (check or X)
  const handleSelection = async (event, option) => {
    console.log(index)
    event.stopPropagation(); // Prevent the click event from bubbling up
    setSelection(option); // Set the user's selection state

    // Notify the parent component of the selection
    await onSelection(restaurant._id, option, totalTimeSpent);

    // Visually remove the card if "X" is selected
    if (option === 'x') {
      setCardClass(`${styles.card} ${styles.removed}`); // Apply the "removed" class to fade out the card
    }
  };

  // Update the CSS class based on the selection state
  useEffect(() => {
    
    if (selection === 'check') {
      setCardClass(`${styles.card} ${styles.selectedCheck}`);
    } else if (selection === 'x') {
      setCardClass(`${styles.card} ${styles.selectedX}`);
    } else {
      setCardClass(styles.card); // Reset to the default class if no selection
    }
  }, [selection]); // Dependency array ensures this effect runs whenever the selection changes

  return (
    <li onClick={openModal} className={cardClass}>
      <div className={styles.cardImageWrapper}>
        <img src={restaurant.image_url} alt={restaurant.name} className={styles.cardImage} />
      </div>
      <div className={styles.cardContent}>
        <h2 className={styles.cardTitle}>{restaurant.name}</h2>
        <p className={styles.cardDescription}>
          {restaurant.location.display_address.join(', ')}
        </p>
        <div className={styles.selectionButtons}>
          <button
            className={`${styles.selectionButton} ${isSelected === 'check' ? styles.selected : ''}`}
            onClick={(event) => handleSelection(event, 'check')}
          >
            ✔️
          </button>
          <button
            className={`${styles.selectionButton} ${isSelected === 'x' ? styles.selected : ''}`}
            onClick={(event) => handleSelection(event, 'x')}
          >
            ❌
          </button>
        </div>
        <button
          onClick={(event) => {
            event.stopPropagation(); // Prevent the click event from bubbling up
            openModal(); // Open the details modal
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
          <div className={styles.selectionButtons}>
            <button
              className={`${styles.selectionButton} ${isSelected === 'check' ? styles.selected : ''}`}
              onClick={(event) => handleSelection(event, 'check')}
            >
              ✔️
            </button>
            <button
              className={`${styles.selectionButton} ${isSelected === 'x' ? styles.selected : ''}`}
              onClick={(event) => handleSelection(event, 'x')}
            >
              ❌
            </button>
          </div>
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
