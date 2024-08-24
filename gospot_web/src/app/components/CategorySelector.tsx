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
      const preferenceData = await fetchData('http://127.0.0.1:8080/user/retrieve-current-preferences?user_id=1', 'GET')
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

  const categories = [
    'American', 'New American', 'Southern', 'Soul Food', 'Cajun/Creole', 'Tex-Mex',
    'Chinese', 'Japanese', 'Korean', 'Thai', 'Vietnamese', 'Indian', 'Pakistani', 'Bangladeshi',
    'Taiwanese', 'Filipino', 'Malaysian', 'Indonesian', 'Singaporean', 'Burmese',
    'Cambodian', 'Laotian', 'Mongolian', 'Nepalese', 'Sri Lankan', 'Asian Fusion',
    'Italian', 'French', 'Spanish', 'German', 'Greek', 'British', 'Irish', 'Scottish',
    'Polish', 'Russian', 'Ukrainian', 'Hungarian', 'Czech', 'Austrian', 'Belgian',
    'Dutch', 'Swiss', 'Scandinavian', 'Portuguese',
    'Mexican', 'Brazilian', 'Peruvian', 'Argentine', 'Colombian', 'Venezuelan',
    'Cuban', 'Puerto Rican', 'Dominican', 'Salvadoran', 'Honduran', 'Nicaraguan',
    'Guatemalan', 'Ecuadorian', 'Bolivian', 'Chilean',
    'Lebanese', 'Turkish', 'Persian/Iranian', 'Israeli', 'Moroccan', 'Egyptian',
    'Syrian', 'Armenian', 'Afghan', 'Iraqi', 'Uzbek', 'Georgian',
    'Ethiopian', 'Nigerian', 'Ghanaian', 'Senegalese', 'South African', 'Eritrean',
    'Somali', 'Kenyan', 'Tanzanian', 'Ugandan',
    'Seafood', 'Sushi Bars', 'Fish & Chips', 'Poke',
    'Fast Food', 'Burgers', 'Pizza', 'Sandwiches', 'Hot Dogs', 'Chicken Wings',
    'Vegetarian', 'Vegan', 'Raw Food',
    'Breakfast & Brunch', 'Pancakes', 'Waffles', 'Bagels', 'Donuts',
    'Bakeries', 'Desserts', 'Ice Cream & Frozen Yogurt', 'Cupcakes', 'Patisserie/Cake Shop', 'Gelato',
    'Cafes', 'Coffee & Tea', 'Bubble Tea',
    'Bars', 'Pubs', 'Sports Bars', 'Wine Bars', 'Beer Gardens', 'Cocktail Bars', 'Dive Bars', 'Hookah Bars',
    'Cheese Shops', 'Butcher', 'Farmers Market', 'Specialty Food', 'Organic Stores', 'Health Markets',
    'Food Trucks', 'Food Stands', 'Street Vendors',
    'Grocery', 'International Grocery', 'Convenience Stores',
    'Nightlife', 'Dance Clubs', 'Karaoke', 'Comedy Clubs', 'Jazz & Blues',
    'Museums', 'Art Galleries', 'Performing Arts', 'Music Venues', 'Theaters', 'Cinema',
    'Parks', 'Beaches', 'Hiking', 'Botanical Gardens', 'Playgrounds', 'Dog Parks',
    'Gyms', 'Yoga', 'Martial Arts', 'Swimming Pools', 'Tennis', 'Basketball Courts', 'Soccer',
    'Shopping Centers', 'Clothing', 'Shoes', 'Jewelry', 'Books', 'Electronics', 'Home & Garden',
    'Hair Salons', 'Nail Salons', 'Day Spas', 'Massage',
    'Hotels', 'Hostels', 'Bed & Breakfast',
    'Wedding Planning', 'Party & Event Planning', 'Caterers', 'Photographers',
    'Car Dealers', 'Auto Repair', 'Car Wash', 'Gas Stations',
    'Lawyers', 'Accountants', 'Real Estate', 'Insurance',
    'Schools', 'Colleges', 'Tutoring', 'Cooking Classes', 'Art Schools',
    'Pet Stores', 'Veterinarians', 'Pet Groomers', 'Dog Walkers',
    'Churches', 'Mosques', 'Synagogues', 'Temples',
    'Other'
  ];


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
