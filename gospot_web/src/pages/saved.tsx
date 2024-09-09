import React, { useEffect, useState } from 'react';
// import { savedplaces } from '../app/utils/savedPlaces'; // Adjust the path if necessary
import '../app/styles/Saved.scss';
import { savedplaces } from '../app/utils/savedPlaces';
import { fetchData } from '../app/utils/fetchData';
import SavedPlace from '@/app/components/SavedPlaces';

export default function Saved() {

    const [data, setData] = useState([]);
    // Fetching data for the cards
    const fetchInitialCard = async () => {
        try {
            const idData = await fetchData('http://127.0.0.1:8080/user/retrieve_all_saved?user_id=1', 'GET');
            const detailsData = await fetchData('http://127.0.0.1:8080/user/retrieve_details', 'POST', {}, {
                spotLists: idData,
            });
            setData(detailsData);
            console.log(detailsData)
        } catch (error: any) {
            console.error('Error fetching data:', error.message);
        }
    };
    useEffect(()=> {
        fetchInitialCard()
    },[])
    return(
        <div>
            <div className="title">List of saved restaurants</div>
            <div className="saved-container">
                {data.map((restaurant,index) => (
                    <SavedPlace 
                    key={restaurant._id}
                    
                    restaurant={restaurant}
                    
                    />
                ))}
            </div>
        </div>
    )
}


// const Saved: React.FC = () => {
//   return (
//     <div className='saved-container'>
//       <div className='section'>
//         <h2 className='section-title'>Saved Places</h2>
//         <div className='saved-list'>
//           {savedplaces.map((place) => (
//             <div key={place._id} className='saved-box'>
//               <h3 className='place-name'>{place.group_name}</h3>
//               {/* Add more details like rating and review if available */}
//             </div>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Saved;
