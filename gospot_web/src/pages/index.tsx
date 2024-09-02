import { useState, useEffect } from 'react';
import Modal from 'react-modal';
import RestaurantCard from '../app/components/RestaurantCard';
import { fetchData } from '../app/utils/fetchData';
import CategorySelector from '../app/components/CategorySelector';

Modal.setAppElement('#__next');

export default function Home() {
  const [data, setData] = useState([]); // State to hold restaurant data
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedCategories, setSelectedCategories] = useState([]);
  
  // State to keep track of the user's selection (check or X) for each restaurant
  const [interaction, setinteraction] = useState({});

  // Fetching data for the cards
  const fetchInitialCard = async () => {
    try {
      const idData = await fetchData('http://127.0.0.1:8080/user/get_next_spot?user_id=1&num_items=5', 'GET');
      const detailsData = await fetchData('http://127.0.0.1:8080/user/retrieve_details', 'POST', {}, {
        spotLists: idData,
      });
      setData(detailsData);
    } catch (error:any) {
      console.error('Error fetching data:', error.message);
    }
  };

  // Fetch data when the component mounts
  useEffect(() => {
    fetchInitialCard();
  }, []); // Empty dependency array means this effect runs once when the component mounts


  // Keeping track of user interactions is done here
  useEffect(() => {
    // Check if the user has clicked either check or X for all restaurants
    if (Object.keys(interaction).length === data.length && data.length > 0) {
      // alert('All options clicked');
      sendingInteractions()

    }
  }, [interaction, data.length]);


  // THIS IS WHERE YOU ARE SENDING YOUR SPOT PREFENCES, OR THE DATA THAT WOULD SAY YOU LIKE OR NOT
  const sendingInteractions = async () => {
    const interactionResponse = await fetchData('http://127.0.0.1:8080/user/record_interaction', 'POST',{}, 
      {
        'user_id': 1,
        interaction
      }
    )
    // console.log( {
    //   'user_id': 1,
    //   'interaction' : {interaction}
    // })
  }

  // Replacing card at the specific index
  

  
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
      await fetchInitialCard()
    } catch (error) {
      console.error('Error fetching data:', error.message);
      alert("Unable to Register data");
      setModalIsOpen(false);
    }
  };

  // Function to handle user's selection of check or X
  const handleSelection = (restaurantId, option, timeTaken) => {
    let toSaveOrNot = 'False'
    if(option == 'check'){
      toSaveOrNot = 'True'
    }
    setinteraction(prev => ({ ...prev, [restaurantId]: 
      { "time_viewing": timeTaken, "pressed_save": toSaveOrNot }}));
  };

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={openModal}>Select Categories</button>

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

      <h1>Restaurants in New York</h1>
      <ul>
        {data.map((restaurant,index) => (
          // Pass the selection state and handler to each RestaurantCard
          <RestaurantCard
            key={restaurant._id}
            index ={index}
            restaurant={restaurant}
            onSelection={handleSelection}
            isSelected={interaction[restaurant._id]}
          />
        ))}
      </ul>
      <button onClick={() => window.location.reload()}>Refresh Everything</button>
    </div>
  );
}
