import React from 'react';
import UserGroupsList from '@/app/components/UserGroupList';
import { groups } from '@/app/utils/data';
import GroupsActions from '@/app/components/GroupsActions';
import '../app/styles/Group.scss';

const Group: React.FC = () => {
  return (
    <div className='group-container'>
      <div className='section'>
        <h2 className='section-title'>Group Actions</h2>
        <GroupsActions />
      </div>
      <div className='section'>
        <h2 className='section-title'>My Groups</h2>
        <UserGroupsList groups={groups} />
      </div>
    </div>
  );
};

export default Group;
