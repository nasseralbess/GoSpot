import React from 'react';
import styles from '../styles/UserGroupList.module.scss';

interface Group {
  _id: string;
  group_name: string;
}

interface UserGroupsListProps {
  groups: Group[];
}

const UserGroupsList: React.FC<UserGroupsListProps> = ({ groups }) => {
  return (
    <div className={styles.container}>
      {groups.map((group) => (
        <div key={group._id} className={styles.groupBox}>
          {group.group_name}
        </div>
      ))}
    </div>
  );
};

export default UserGroupsList;
