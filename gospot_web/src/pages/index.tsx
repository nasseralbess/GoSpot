import { useState, useEffect } from 'react';
import Modal from 'react-modal';
import RestaurantCard from '../app/components/RestaurantCard';
import { fetchData } from '../app/utils/fetchData';
import CategorySelector from '../app/components/CategorySelector';

Modal.setAppElement('#__next');

export async function getServerSideProps() {
  try {
    const idData = await fetchData('http://127.0.0.1:8080/user/get-next-spot?user_id=1', 'GET');

    const data = await fetchData('http://127.0.0.1:8080/user/retrieve-details', 'POST', {}, {
      spotLists: idData,
    });

    return { props: { data } };
  } catch (error) {
    console.error('Error fetching data:', error.message);
    return { props: { data: [], error: error.message || 'Failed to load data' } };
  }
}

export default function Home({ data }) {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedCategories, setSelectedCategories] = useState([]);
  
  // State to keep track of the user's selection (check or X) for each restaurant
  const [selections, setSelections] = useState({});

  // Keeping track of user interactions is done here
  useEffect(() => {
    console.log(("Running here"))
    console.log(Object.keys(selections).length)
    console.log(selections)
    // Check if the user has clicked either check or X for all restaurants
    if (Object.keys(selections).length === data.length && data.length > 0) {
      alert('All options clicked');
    }
  }, [selections, data.length]);

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
      const data = await fetchData('http://127.0.0.1:8080/user/update-preferences', 'PUT', {}, {
        user_id: 1,
        new_preferences: {
          price: price,
          categories: categories.selectedCategories,
          coordinates: [2131231.22, 312312312.22],
        }
      });

      console.log(data);
      setModalIsOpen(false);
    } catch (error) {
      console.error('Error fetching data:', error.message);
      alert("Unable to Register data");
      setModalIsOpen(false);
    }
  };
  // Added more functionalities here
  // Function to handle user's selection of check or X
  const handleSelection = (restaurantId, option,timeTaken) => {
    setSelections(prev => ({ ...prev, [restaurantId]: {option:option,timeTaken:timeTaken} }));
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
        {data.map((restaurant) => (
          // Pass the selection state and handler to each RestaurantCard
          <RestaurantCard
            key={restaurant._id}
            restaurant={restaurant}
            onSelection={handleSelection}
            isSelected={selections[restaurant._id]}
          />
        ))}
      </ul>
      <button>Refresh Everything</button>
    </div>
  );
}
