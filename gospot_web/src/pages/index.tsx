// src/app/pages/index.tsx
import { useEffect } from 'react';
import RestaurantCard from '../app/components/RestaurantCard';
import { datas } from '../app/utils/data';

// Fetch data from the backend
export async function getServerSideProps() {
  try {
    // Fetch the first set of data
    const ids = await fetch('http://127.0.0.1:8080/user/get-next-spot?user_id=1');
    if (!ids.ok) {
      const text = await ids.text();
      throw new Error(`Failed to fetch ids: ${ids.status} - ${text}`);
    }

    const idData = await ids.json();
    console.log(idData)
    // Fetch the second set of data using POST
    const res = await fetch('http://127.0.0.1:8080/user/retrieve-details', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        spotLists: idData,
      }),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Failed to fetch data: ${res.status} - ${text}`);
    }

    const data = await res.json();
    

    // Pass data to the page via props
    return { props: { data } };
  } catch (error) {
    console.error('Error fetching data:', error.message);
    return { props: { data: [], error: error.message || 'Failed to load data' } };
  }
}




export default function Home({data}) {
  useEffect(() => {
    console.log(data)
  })
  return (
    <div style={{ padding: '20px' }}>
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
