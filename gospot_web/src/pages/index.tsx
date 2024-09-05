import { useState, useEffect } from 'react';
import Modal from 'react-modal';
import RestaurantCard from '../app/components/RestaurantCard';
import { fetchData } from '../app/utils/fetchData';
import CategorySelector from '../app/components/CategorySelector';
import '../app/styles/Home.css';

Modal.setAppElement('#__next');

export default function Home() {
  const [data, setData] = useState([]); // State to hold restaurant data
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedCategories, setSelectedCategories] = useState([]);

  // State to keep track of the user's selection (check or X) for each restaurant
  const [interaction, setinteraction] = useState({});
  const [pendingReplaceIndex, setPendingReplaceIndex] = useState(null); // To store the index that needs to be replaced

  // Fetching data for the cards
  const fetchInitialCard = async () => {
    try {
      const idData = await fetchData('http://127.0.0.1:8080/user/get_next_spot?user_id=1&num_items=5', 'GET');
      const detailsData = await fetchData('http://127.0.0.1:8080/user/retrieve_details', 'POST', {}, {
        spotLists: idData,
      });
      setData(detailsData);
    } catch (error: any) {
      console.error('Error fetching data:', error.message);
    }
  };

  // Fetch data when the component mounts
  useEffect(() => {
    fetchInitialCard();
  }, []); // Empty dependency array means this effect runs once when the component mounts

  // Use useEffect to monitor when to send interactions and replace card
  useEffect(() => {
    if (pendingReplaceIndex !== null) {
      sendingInteractions(); // Call this after the interaction state has been updated
      replaceCardAtIndex(pendingReplaceIndex);
      setPendingReplaceIndex(null); // Reset the pending index
    }
  }, [interaction, pendingReplaceIndex]);

  // THIS IS WHERE YOU ARE SENDING YOUR SPOT PREFERENCES, OR THE DATA THAT WOULD SAY YOU LIKE OR NOT
  const sendingInteractions = async () => {
    console.log(interaction);
    const interactionResponse = await fetchData('http://127.0.0.1:8080/user/record_interaction', 'POST', {},
      {
        'user_id': 1,
        interaction
      }
    );
    setinteraction({});
  };

  const replaceCardAtIndex = async (index) => {
    try {
      let newCardData;
      let isDuplicate = true;

      // Fetch a new card until it's not a duplicate of the one being replaced
      while (isDuplicate) {
        const newIdCard = await fetchData('http://127.0.0.1:8080/user/get_next_spot?user_id=1&num_items=1', 'GET');
        newCardData = await fetchData('http://127.0.0.1:8080/user/retrieve_details', 'POST', {}, {
          spotLists: newIdCard,
        });

        // Check if the new card is different from the current card at the index
        if (data[index]._id !== newCardData[0]._id) {
          isDuplicate = false;
        }
      }

      // Update only the card at the specific index
      setData(prevData => prevData.map((card, idx) => idx === index ? newCardData[0] : card));
    } catch (error) {
      console.error('Error replacing card:', error.message);
    }
  };





  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = async (categories) => {
    setSelectedCategories(categories);

    let price;
    switch (categories.priceRange) {
      case 1:
        price = '$';
        break;
      case 2:
        price = '$$';
        break;
      case 3:
        price = '$$$';
        break;
      case 4:
        price = '$$$$';
        break;
      default:
        price = '$';
    }

    try {
      const data = await fetchData('http://127.0.0.1:8080/user/update_preferences', 'PUT', {}, {
        user_id: 1,
        new_preferences: {
          price: price,
          categories: categories.selectedCategories,
          coordinates: [2131231.22, 312312312.22],
        }
      });

      console.log(data);
      setModalIsOpen(false);
      await fetchInitialCard();
    } catch (error) {
      console.error('Error fetching data:', error.message);
      alert("Unable to Register data");
      setModalIsOpen(false);
    }
  };

  // Function to handle user's selection of check or X
  const handleSelection = (restaurantId, option, timeTaken, pressedShare, index) => {
    let toSaveOrNot = option === 'check' ? 'True' : 'False';
    let toShareOrNot = pressedShare ? 'True' : 'False';
    // Update the interaction state first
    setinteraction(prev => ({
      ...prev,
      [restaurantId]: {
        "time_viewing": timeTaken,
        "pressed_save": toSaveOrNot,
        "pressed_share": toShareOrNot
      }
    }));

    // Set the index that needs replacement
    setPendingReplaceIndex(index);
  };
  return (
    <div className="home-container">
      

      <h1 className="home-title">Restaurants in New York</h1>

      <button className="category-button" onClick={openModal}>Select Categories</button>

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={() => closeModal(selectedCategories)}
        contentLabel="Category Selector Modal"
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
        <CategorySelector onClose={closeModal} />
      </Modal>
      
      <ul className="restaurant-list">
        {data.map((restaurant, index) => (
          <RestaurantCard
            key={restaurant._id}
            index={index}
            restaurant={restaurant}
            onSelection={handleSelection}
            isSelected={interaction[restaurant._id]}
          />
        ))}
      </ul>

      <button className="refresh-button" onClick={() => window.location.reload()}>Refresh Everything</button>
    </div>
  );

}
