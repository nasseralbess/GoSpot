// pages/index.js

import { useState, useEffect } from 'react';
import Modal from 'react-modal';
import RestaurantCard from '../app/components/RestaurantCard';
import { fetchData } from '../app/utils/fetchData';
import CategorySelector from '../app/components/CategorySelector';

// Set the app element for accessibility (only necessary with react-modal)
Modal.setAppElement('#__next');

// Fetch data from the backend
export async function getServerSideProps() {
  try {
    // Fetch the first set of data
    const idData = await fetchData('http://127.0.0.1:8080/user/get-next-spot?user_id=1', 'GET');

    // Fetch the second set of data using POST
    const data = await fetchData('http://127.0.0.1:8080/user/retrieve-details', 'POST', {}, {
      spotLists: idData,
    });

    // Pass data to the page via props
    return { props: { data } };
  } catch (error) {
    console.error('Error fetching data:', error.message);
    return { props: { data: [], error: error.message || 'Failed to load data' } };
  }
}

export default function Home({ data }) {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedCategories, setSelectedCategories] = useState([]);

  useEffect(() => {
    console.log(data);
  }, [data]);

  const openModal = () => {
    setModalIsOpen(true);
  };

  // If close with confirm selection, send data 
  const closeModal = async (categories) => {
    setSelectedCategories(categories); // Save the selected categories in the parent state

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

    console.log('Selected Categories:', price, categories.selectedCategories); // Handle the selected categories as needed
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
          <RestaurantCard key={restaurant._id} restaurant={restaurant} />
        ))}
      </ul>
      <button>Refresh Everything</button>
    </div>
  );
}
