import React from 'react';

const GroupActions = () => {
  return (
    <div className='container'>
      <div style={styles.actionBox}>
        Create a new group
      </div>
      <div style={styles.actionBox}>
        Join a group
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-around',
    padding: '20px',
  },
  actionBox: {
    border: '2px solid #0070f3',
    borderRadius: '8px',
    padding: '20px',
    textAlign: 'center',
    backgroundColor: '#f0f0f0',
    cursor: 'pointer',
    width: '150px',
    transition: 'background-color 0.3s, transform 0.3s',
  },
  actionBoxHover: {
    backgroundColor: '#0070f3',
    color: '#fff',
    transform: 'scale(1.05)',
  },
};

export default GroupActions;
