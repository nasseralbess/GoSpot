import React from 'react';
import UserGroupsList from '@/app/components/UserGroupList';
import { groups } from '@/app/utils/data';
import GroupActions from '@/app/components/GroupActions';
import '../app/styles/Group.scss'

const Group: React.FC = () => {
  return (
    <div className='containers'>
      <UserGroupsList groups={groups}></UserGroupsList>
      <GroupActions></GroupActions>
    </div>
  );
};

export default Group;
