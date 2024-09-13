import React, { useState, useRef } from 'react';
import Modal from 'react-modal';
import styles from '../styles/RestaurantCard.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShareSquare, faBookmark, faStar } from '@fortawesome/free-solid-svg-icons';

const RestaurantCard = ({ restaurant, onSelection, index }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false); // State to control the restaurant details modal
  const [totalTimeSpent, setTotalTimeSpent] = useState(0); // Track the total time spent viewing the card
  const [selection, setSelection] = useState(null); // Track if the user has selected check or X
  const [cardClass, setCardClass] = useState(styles.card); // Track the CSS class applied to the card
  const [pressedShare, setPressedShare] = useState(false) //track if the user pressed share or not
  const timerRef = useRef(null); // Ref to track when the user starts viewing details

  // Function to open the modal and start the timer
  const openModal = () => {
    setModalIsOpen(true);
    timerRef.current = Date.now(); // Start timing when the modal opens
  };

  // Function to calculate and record the time spent
  const recordTimeSpent = () => {
    if (timerRef.current) {
      const timeSpent = (Date.now() - timerRef.current) / 1000; // Calculate time spent in seconds
      setTotalTimeSpent((prevTime) => prevTime + timeSpent); // Update total time spent
      return timeSpent;
    }
    return 0;
  };

  // Function to close the modal
  const closeModal = (event) => {
    event.stopPropagation(); // Prevent the click event from bubbling up
    recordTimeSpent(); // Record the time spent in the modal
    setModalIsOpen(false);
  };

  // Function to handle user's selection (Save or No More of This)
  const handleSelection = async (event, option) => {
    event.stopPropagation(); // Prevent the click event from bubbling up
    const timeSpent = recordTimeSpent(); // Record the time spent before proceeding

   

    // Update the card class based on selection
    if (option === 'check') {
      setCardClass(`${styles.card} ${styles.added}`);
    } else if (option === 'no_more') {
      setCardClass(`${styles.card} ${styles.removed}`); // Apply the "removed" class to fade out the card
    } else {
      setCardClass(styles.card); // Reset to the default class if no selection
    }

    // Notify the parent component of the selection with the correct total time spent
    await onSelection(restaurant._id, option, totalTimeSpent + timeSpent, pressedShare,index);

    // Close the modal if it is open
    if (modalIsOpen) {
      setModalIsOpen(false);
    }
  };

  // User has pressed share 
  const UserPressedShare = () => {
    setPressedShare(true)
  }

  // Function to redirect to Google search
  const redirectToGoogleSearch = () => {
    const toEncode = restaurant.name + " New York";
    const query = encodeURIComponent(toEncode);
    const url = `https://www.google.com/search?q=${query}`;
    window.open(url, '_blank');
  };

  return (
    <li onClick={openModal} className={cardClass}>
      <div className={styles.cardImageWrapper}>
        <img src={restaurant.image_url} alt={restaurant.name} className={styles.cardImage} />
      </div>
      <div className={styles.cardContent}>
        <h2 className={styles.cardTitle}>{restaurant.name}</h2>
        <p className={styles.cardDescription}>
          {/* Check if location and display_address exist before rendering */}
          {restaurant.location?.display_address ? 
            restaurant.location.display_address.join(', ') : 
            'Address not available'}
        </p>
        <div className={styles.selectionButtons}>
          {/* <button
            className={styles.saveButton}
            onClick={(event) => handleSelection(event, 'check')}
          >
            Save
          </button> */}
          <button
            className={styles.noMoreButton}
            onClick={(event) => handleSelection(event, 'no_more')}
          >
            Less like this
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
            <p className={styles.cardDescription}>
              {/* Check if location and display_address exist before rendering */}
              {restaurant.location?.display_address ? 
                restaurant.location.display_address.join(', ') : 
                'Address not available'}
            </p>
            <p>Phone: {restaurant.display_phone}</p>
            <p>Distance: {restaurant.distance.toFixed(2)} meters</p>
            <p>Transactions: {restaurant.transactions.join(', ')}</p>
          </div>
        </div>
        {/* New Google Search Button */}
        <button
          onClick={(event) => {
            event.stopPropagation(); // Prevent the click event from bubbling up
            redirectToGoogleSearch(); // Redirect to Google search
          }}
          className={styles.googleSearchButton} // Add a new CSS class for styling if needed
        >
          Google Search
        </button>
        <div className={styles.modalFooter}>
        <button
            className={styles.noMoreButton}
            onClick={(event) => handleSelection(event, 'no_more')}
          >
            Less like this
          </button>
          <a
            href={restaurant.url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.modalCtaButton}
          >
            Visit Yelp Page
          </a>
          <div className={styles.modalButtons}>
            <button 
            onClick={UserPressedShare}
            className={styles.modalButton}>
              <FontAwesomeIcon icon={faShareSquare} />
            </button>
            <button 
            onClick={(event) => handleSelection(event, 'check')}
            className={styles.modalButton}>
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
