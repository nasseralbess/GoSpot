import React, { createContext, useState, useContext } from 'react';

const SavedContext = createContext();

export const SavedProvider = ({ children }) => {
  const [savedItems, setSavedItems] = useState([]);

  const addSavedItem = (item) => {
    setSavedItems([...savedItems, item]);
  };

  return (
    <SavedContext.Provider value={{ savedItems, addSavedItem }}>
      {children}
    </SavedContext.Provider>
  );
};

export const useSaved = () => useContext(SavedContext);
