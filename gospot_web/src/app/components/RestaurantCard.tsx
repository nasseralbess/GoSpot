import React, { useState, useRef, useEffect } from 'react';
import Modal from 'react-modal';
import styles from '../styles/RestaurantCard.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShareSquare, faBookmark, faStar } from '@fortawesome/free-solid-svg-icons';

const RestaurantCard = ({ restaurant, onSelection, isSelected }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [totalTimeSpent, setTotalTimeSpent] = useState(0); 
  const [selection, setSelection] = useState(null); 
  const [cardClass, setCardClass] = useState(`${styles.card} ${styles.selectedX}`); 
  const timerRef = useRef(null); 

  const openModal = () => {
    setModalIsOpen(true);
    timerRef.current = Date.now(); 
  };

  const closeModal = (event) => {
    event.stopPropagation(); 
    const timeSpent = (Date.now() - timerRef.current) / 1000; 
    setTotalTimeSpent((prevTime) => prevTime + timeSpent); 
    setModalIsOpen(false);
  };

  const handleSelection = (event, option) => {
    event.stopPropagation(); 
    setSelection(option); 
    onSelection(restaurant._id, option, totalTimeSpent); 
  };

  useEffect(() => {
    if (selection === 'check') {
      setCardClass(`${styles.card} ${styles.selectedCheck}`);
    } else if (selection === 'x') {
      setCardClass(`${styles.card} ${styles.selectedX}`);
    } else {
      setCardClass(styles.card); 
    }
  }, [selection]); 

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