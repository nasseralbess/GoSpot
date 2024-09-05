// src/app/components/GroupsActions.tsx
import React from 'react';
import styles from '../styles/GroupsActions.module.css';

const GroupsActions: React.FC = () => {
  return (
    <div className={styles.groupActionsContainer}>
      <div className={styles.actionBox}>
        Create a new group
      </div>
      <div className={styles.actionBox}>
        Join a group
      </div>
    </div>
  );
};

export default GroupsActions;
