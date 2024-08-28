import React, { useState, useRef, useEffect } from 'react';
import Modal from 'react-modal';
import styles from '../styles/RestaurantCard.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShareSquare, faBookmark, faStar } from '@fortawesome/free-solid-svg-icons';

const RestaurantCard = ({ restaurant, onSelection, isSelected }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [totalTimeSpent, setTotalTimeSpent] = useState(0); // State to track total time spent on the modal
  const [selection, setSelection] = useState(null); // State to track selection (check or X)
  const [cardClass, setCardClass] = useState(`${styles.card}`); // Initialize the cardClass with the default class
  const timerRef = useRef(null); // Ref to track the time when the modal is opened

  // Function to open the modal and start the timer
  const openModal = () => {
    setModalIsOpen(true);
    timerRef.current = Date.now(); // Start the timer when the modal is opened
  };

  // Function to close the modal and calculate the time spent
  const closeModal = (event) => {
    event.stopPropagation(); // Prevent click event from propagating to parent elements
    const timeSpent = (Date.now() - timerRef.current) / 1000; // Calculate time spent in seconds

    setTotalTimeSpent((prevTime) => prevTime + timeSpent); // Accumulate the time spent
    setModalIsOpen(false);

    console.log(`User viewed ${restaurant.name} for ${timeSpent} seconds.`);
    console.log(`Total time spent on ${restaurant.name}: ${totalTimeSpent + timeSpent} seconds.`);
  };

  // Function to handle selection of check or X, passing the total time
  const handleSelection = (event, option) => {
    event.stopPropagation(); // Prevent click event from propagating to parent elements
    setSelection(option); // Set the selection state to either 'check' or 'x'
    onSelection(restaurant._id, option, totalTimeSpent); // Pass the selection to the parent component
  };

  // useEffect to update the card class based on the selection
  useEffect(() => {
    if (selection === 'check') {
      setCardClass(`${styles.card} ${styles.selectedCheck}`);
    } else if (selection === 'x') {
      setCardClass(`${styles.card} ${styles.selectedX}`);
    } else {
      setCardClass(styles.card); // Reset to default class if no selection
    }
  }, [selection]); // Dependency array: run this effect when `selection` changes

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
        <p>Phone: {restaurant.display_phone}</p>
        <p>Distance: {restaurant.distance.toFixed(2)} meters</p>
        <p>Transactions: {restaurant.transactions.join(', ')}</p>
        <a
          href={restaurant.url}
          target="_blank"
          rel="noopener noreferrer"
          className={styles.ctaButton}
          onClick={(event) => event.stopPropagation()}
        >
          Visit Yelp Page
        </a>
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
          {/* Selection buttons: check and X */}
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
