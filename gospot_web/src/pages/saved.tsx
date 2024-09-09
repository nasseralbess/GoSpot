import React from 'react';
import { useState, useEffect } from 'react';
import { fetchData } from '../app/utils/fetchData';


const Saved: React.FC = () => {
    const [data, setData] = useState([]); // State to hold restaurant data

    // Fetch data when the component mounts
    useEffect(() => {
        fetchInitialCard();
    }, []); // Empty dependency array means this effect runs once when the component mounts


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



    return (
        <div>
            <h1>About Us Page</h1>
            <p>Welcome to the About Us page.</p>
        </div>
    );
};

export default Saved;
