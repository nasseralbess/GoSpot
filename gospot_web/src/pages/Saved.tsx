import React from 'react';
import { savedplaces } from '../app/utils/savedPlaces'; // Adjust the path if necessary
import '../app/styles/Saved.scss';

const Saved: React.FC = () => {
  return (
    <div className='saved-container'>
      <div className='section'>
        <h2 className='section-title'>Saved Places</h2>
        <div className='saved-list'>
          {savedplaces.map((place) => (
            <div key={place._id} className='saved-box'>
              <h3 className='place-name'>{place.group_name}</h3>
              {/* Add more details like rating and review if available */}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Saved;