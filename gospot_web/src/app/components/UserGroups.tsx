import React from 'react';
import styles from '../styles/UserGroupList.module.scss';

const UserGroups = ({ groups }) => {
  return (
    <div className='container'>
      {groups.map((group) => (
        <div key={group._id} className={styles.groupBox}>
          {group.group_name}
        </div> 
      ))}
    </div>
  );
};

export default UserGroups;
