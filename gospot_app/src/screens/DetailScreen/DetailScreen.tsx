import React, { useState } from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { useSaved } from '../../context/SavedContext';

const DetailsScreen = ({ route, navigation }) => {
  const { user } = route.params;
  const { addSavedItem } = useSaved();
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    addSavedItem(user);
    setSaved(true);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.name}>{user.name}</Text>
      <Text style={styles.bio}>{user.bio}</Text>
      <Button title="Save" onPress={handleSave} disabled={saved} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  name: {
    fontSize: 30,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  bio: {
    fontSize: 18,
    textAlign: 'center',
  },
});

export default DetailsScreen;
