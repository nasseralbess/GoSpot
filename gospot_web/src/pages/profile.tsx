import React from 'react';

const Profile: React.FC = () => {
  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Profile Page</h1>
      <div style={styles.profileContainer}>
        <div style={styles.imagePlaceholder}></div>
        <div style={styles.infoContainer}>
          <h2 style={styles.name}>John Doe</h2>
          <p style={styles.email}>john.doe@example.com</p>
          <p style={styles.bio}>
            Hi there! I love exploring new places to hang out, whether it's cozy coffee shops, scenic parks, or trendy bars. Let's connect and discover some awesome spots together!
          </p>
          <div style={styles.stats}>
            <div style={styles.statItem}>
              <strong>Favorites:</strong> 24 spots
            </div>
            <div style={styles.statItem}>
              <strong>Reviews:</strong> 18 reviews
            </div>
            <div style={styles.statItem}>
              <strong>Visited:</strong> 30 spots
            </div>
          </div>
          <button style={styles.editButton}>Edit Profile</button>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  header: {
    fontSize: '2rem',
    marginBottom: '20px',
  },
  profileContainer: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '20px',
    width: '100%',
    maxWidth: '600px',
    border: '1px solid #ccc',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  imagePlaceholder: {
    width: '150px',
    height: '150px',
    backgroundColor: '#eee',
    borderRadius: '50%',
    marginRight: '20px',
  },
  infoContainer: {
    flex: 1,
  },
  name: {
    fontSize: '1.5rem',
    marginBottom: '10px',
  },
  email: {
    fontSize: '1rem',
    marginBottom: '10px',
  },
  bio: {
    fontSize: '1rem',
    marginBottom: '20px',
  },
  stats: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '20px',
  },
  statItem: {
    fontSize: '1rem',
  },
  editButton: {
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
};

export default Profile;
