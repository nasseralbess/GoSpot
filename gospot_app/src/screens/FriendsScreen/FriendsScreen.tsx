import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, FlatList, TouchableOpacity, Modal, Button } from 'react-native';

// Sample data for friends
const friendsData = [
  {
    id: '1',
    name: 'Alice Smith',
    image: 'https://example.com/alice-profile.jpg',
    bio: 'Loves hiking and outdoor adventures.',
    email: 'alice@example.com',
  },
  {
    id: '2',
    name: 'Bob Johnson',
    image: 'https://example.com/bob-profile.jpg',
    bio: 'A foodie and a tech enthusiast.',
    email: 'bob@example.com',
  },
  {
    id: '3',
    name: 'Carol White',
    image: 'https://example.com/carol-profile.jpg',
    bio: 'Enjoys painting and music.',
    email: 'carol@example.com',
  },
];

const FriendsScreen = () => {
  const [selectedFriend, setSelectedFriend] = useState<any>(null);

  const handlePress = (friend: any) => {
    setSelectedFriend(friend);
  };

  const handleCloseModal = () => {
    setSelectedFriend(null);
  };

  const renderFriendItem = ({ item }: { item: any }) => (
    <TouchableOpacity style={styles.friendItem} onPress={() => handlePress(item)}>
      <Image source={{ uri: item.image }} style={styles.friendImage} />
      <View style={styles.friendInfo}>
        <Text style={styles.friendName}>{item.name}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Friends</Text>
      <FlatList
        data={friendsData}
        renderItem={renderFriendItem}
        keyExtractor={(item) => item.id}
      />

      {/* Modal for displaying friend info */}
      {selectedFriend && (
        <Modal
          visible={!!selectedFriend}
          transparent={true}
          animationType="slide"
          onRequestClose={handleCloseModal}
        >
          <View style={styles.modalContainer}>
            <View style={styles.modalContent}>
              <Image source={{ uri: selectedFriend.image }} style={styles.modalImage} />
              <Text style={styles.modalName}>{selectedFriend.name}</Text>
              <Text style={styles.modalBio}>{selectedFriend.bio}</Text>
              <Text style={styles.modalEmail}>{selectedFriend.email}</Text>
              <Button title="Close" onPress={handleCloseModal} />
            </View>
          </View>
        </Modal>
      )}
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
  friendItem: {
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
  friendImage: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginRight: 10,
  },
  friendInfo: {
    flex: 1,
    justifyContent: 'center',
  },
  friendName: {
    fontSize: 18,
    fontWeight: '500',
    color: '#333',
    textAlign: 'left',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)', // Semi-transparent background
  },
  modalContent: {
    width: '80%',
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 15,
  },
  modalName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  modalBio: {
    fontSize: 16,
    color: '#666',
    marginBottom: 10,
  },
  modalEmail: {
    fontSize: 16,
    color: '#666',
    marginBottom: 20,
  },
});

export default FriendsScreen;
