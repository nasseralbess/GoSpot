import React, { useEffect, useState } from 'react';
import style from '../styles/preferences.module.scss';
import { fetchData } from '../utils/fetchData';

const CategorySelector = ({ onClose }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [priceRange, setPriceRange] = useState(2); // default value is $$

  useEffect(() => {
    retrieveDataFirst();
  }, [])

  const retrieveDataFirst = async () => {
    try {
      const preferenceData = await fetchData('http://127.0.0.1:8080/user/retrieve_current_preferences?user_id=1', 'GET')
      console.log(preferenceData)
      let pricing;
      switch (preferenceData.price) {
        case '$':
          pricing = 1;
          break;
        case '$$':
          pricing = 2;
          break;
        case '$$$':
          pricing = 3;
          break;
        case '$$$$':
          pricing = 4;
          break;
        default:
          pricing = 1; // Default to 1 if the price doesn't match any case
      }
      setSelectedCategories(preferenceData.categories)
      setPriceRange(pricing)

    }
    catch (err) {

    }


  }

  const categories = 
    ['American', 'Asian', 'European', 'Latin American', 'Middle Eastern', 'African', 'Seafood', 'Fast Food', 'Vegetarian and Vegan', 'Breakfast and Brunch', 'Bakeries and Desserts', 'Cafes and Coffee Shops', 'Bars and Pubs', 'Specialty Food', 'Food Trucks and Stands', 'Grocery', 'Nightlife', 'Arts and Entertainment', 'Outdoor Activities', 'Fitness and Sports', 'Shopping', 'Beauty and Spas', 'Hotels and Accommodation', 'Event Planning and Services', 'Automotive', 'Professional Services', 'Education', 'Pets', 'Religious Organizations', 'Other']

    
  ;


  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleCategoryClick = (category) => {
    if (!selectedCategories.includes(category)) {
      setSelectedCategories([...selectedCategories, category]);
    }
    setSearchTerm(''); // Clear the search term after selection
  };

  const handleRemoveCategory = (category) => {
    setSelectedCategories(selectedCategories.filter(c => c !== category));
  };

  const filteredCategories = categories.filter(
    (category) => category.toLowerCase().includes(searchTerm.toLowerCase()) && !selectedCategories.includes(category)
  );

  const handleConfirmSelection = () => {
    onClose({ selectedCategories, priceRange });
  };

  const handleSliderChange = (e) => {
    setPriceRange(parseInt(e.target.value));
  };

  const getLabelClass = (range) => {
    return priceRange === range ? style.selected_label : '';
  };

  return (
    <div className={style.overall_modal}>

      <div className={style.texts}>
        <h1 className={style.main_text}>Edit your preferences</h1>
        <p>Keep in mind these preferences are your overall preference</p>
        <hr className={style.hr_line} />


      </div>


      <div className={style.category_selection}>
        <div style={{ textAlign: 'left', marginBottom: '20px', position: 'relative' }}>
          <input
            type="text"
            value={searchTerm}
            onChange={handleSearchChange}
            placeholder="Add your preferences..."
            className={style.search_input}
          />

          {searchTerm && filteredCategories.length > 0 && (
            <div className={style.drop_down}>
              {filteredCategories.map((category) => (
                <div
                  key={category}
                  onClick={() => handleCategoryClick(category)}
                  className={style.dropdown_item}
                >
                  {category}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className={style.selected_categories_container} style={{ marginTop: '20px' }}>
          {selectedCategories.map((category) => (
            <div
              key={category}
              onClick={() => handleRemoveCategory(category)}
              className={style.categoryTag}
            >
              {category}
            </div>
          ))}
        </div>
      </div>

      <hr />

      <div className={style.slider_container}>
        <label className={style.slider_label}>Select Price Range:</label>
        <input
          type="range"
          min="1"
          max="4"
          value={priceRange}
          onChange={handleSliderChange}
          className={style.slider}
        />
        <div className={style.slider_labels}>
          <span className={getLabelClass(1)}>$</span>
          <span className={getLabelClass(2)}>$$</span>
          <span className={getLabelClass(3)}>$$$</span>
          <span className={getLabelClass(4)}>$$$$</span>
        </div>
      </div>

      <button
        onClick={handleConfirmSelection}
        className={style.confirmButton}
      >
        Confirm Selection
      </button>
    </div>
  );
};

export default CategorySelector;
