import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Modal, Button, FlatList } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import uuid from 'react-native-uuid';

const GroupsScreen = () => {
  const [groupID, setGroupID] = useState<string>('');
  const [groupName, setGroupName] = useState<string>('');
  const [groups, setGroups] = useState<any[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<any>(null);
  const [joinGroupID, setJoinGroupID] = useState<string>('');
  const [modalVisible, setModalVisible] = useState<boolean>(false);
  const navigation = useNavigation();

  const handleCreateGroup = () => {
    const newGroup = {
      id: uuid.v4() as string,
      name: groupName,
      members: [],
    };
    setGroups([...groups, newGroup]);
    setGroupID(newGroup.id);
    setGroupName('');
    setModalVisible(true);
  };

  const handleJoinGroup = () => {
    const group = groups.find((g) => g.id === joinGroupID);
    if (group) {
      group.members.push({ id: uuid.v4() as string, name: `Member ${group.members.length + 1}` });
      setSelectedGroup(group);
    } else {
      alert('Group not found');
    }
    setJoinGroupID('');
  };

  const handleLeaveGroup = (groupId: string) => {
    const updatedGroups = groups.map((group) => {
      if (group.id === groupId) {
        group.members.pop(); // Simulating leaving the group
      }
      return group;
    });
    setGroups(updatedGroups);
    setSelectedGroup(null);
  };

  const renderGroupItem = ({ item }: { item: any }) => (
    <TouchableOpacity style={styles.groupItem} onPress={() => setSelectedGroup(item)}>
      <View style={styles.groupInfo}>
        <Text style={styles.groupName}>{item.name}</Text>
        <Text style={styles.groupId}>{item.id}</Text>
      </View>
    </TouchableOpacity>
  );

  const renderMemberItem = ({ item }: { item: any }) => (
    <View style={styles.memberItem}>
      <Text style={styles.memberName}>{item.name}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Groups</Text>
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Enter Group Name"
          value={groupName}
          onChangeText={setGroupName}
        />
        <Button title="Create Group" onPress={handleCreateGroup} />
      </View>
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Enter Group ID to Join"
          value={joinGroupID}
          onChangeText={setJoinGroupID}
        />
        <Button title="Join Group" onPress={handleJoinGroup} />
      </View>
      <FlatList
        data={groups}
        renderItem={renderGroupItem}
        keyExtractor={(item) => item.id}
      />
      {selectedGroup && (
        <Modal
          visible={!!selectedGroup}
          transparent={true}
          animationType="slide"
          onRequestClose={() => setSelectedGroup(null)}
        >
          <View style={styles.modalContainer}>
            <View style={styles.modalContent}>
              <Text style={styles.modalName}>{selectedGroup.name}</Text>
              <Text style={styles.modalId}>ID: {selectedGroup.id}</Text>
              <Text style={styles.modalMembers}>Members:</Text>
              <FlatList
                data={selectedGroup.members}
                renderItem={renderMemberItem}
                keyExtractor={(item) => item.id}
              />
              <Button title="Leave Group" onPress={() => handleLeaveGroup(selectedGroup.id)} />
              <Button title="Close" onPress={() => setSelectedGroup(null)} />
              <Button title="Start Swipping for Group!" onPress={() => {
                
                navigation.navigate('Home'); 
                setSelectedGroup(null);}

              }/>
            </View>
          </View>
        </Modal>
      )}
      <Modal
        visible={modalVisible}
        transparent={true}
        animationType="slide"
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalText}>Group Created Successfully!</Text>
            <Text style={styles.modalText}>Group ID: {groupID}</Text>
            <Button title="Close" onPress={() => setModalVisible(false)} />
            
          </View>
        </View>
      </Modal>
      
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingTop: 20,
    paddingHorizontal: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#333',
    textAlign: 'center',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  input: {
    flex: 1,
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    marginRight: 10,
  },
  groupItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: 10,
    marginVertical: 5,
    borderRadius: 10,
    width: '100%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  groupInfo: {
    flex: 1,
    justifyContent: 'center',
  },
  groupName: {
    fontSize: 18,
    fontWeight: '500',
    color: '#333',
    textAlign: 'left',
  },
  groupId: {
    fontSize: 14,
    color: '#999',
  },
  memberItem: {
    padding: 5,
  },
  memberName: {
    fontSize: 16,
    color: '#333',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    width: '80%',
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  modalId: {
    fontSize: 16,
    color: '#666',
    marginBottom: 20,
  },
  modalMembers: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  modalText: {
    fontSize: 18,
    marginBottom: 15,
    textAlign: 'center',
  },
});

export default GroupsScreen;
