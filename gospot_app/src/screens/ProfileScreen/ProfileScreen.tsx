import React , { useEffect, useState }from 'react';
import { View, Text, StyleSheet, Image, Button} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useLogto } from '@logto/rn';
import {useNavigation} from '@react-navigation/native';


const ProfileScreen = () => {
  const { signIn, signOut, isAuthenticated, fetchUserInfo } = useLogto();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigation = useNavigation();

  const handleSignOut = async () => {
    setLoading(true);
    try {
      await signOut();
      await AsyncStorage.removeItem('user');
      setUser(null);
      navigation.navigate('SignIn');

    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }

  };

  return (
    <View style={styles.container}>
      <Image
        source={{ uri: 'https://example.com/your-profile-image.jpg' }}
        style={styles.profileImage}
      />
      <Text style={styles.name}>John Doe</Text>
      <Text style={styles.email}>john.doe@example.com</Text>
      <View style={styles.infoContainer}>
        <Text style={styles.infoTitle}>Bio</Text>
        <Text style={styles.infoText}>This is a sample bio.</Text>
      </View>
      <View style={styles.infoContainer}>
        <Text style={styles.infoTitle}>Favorite Cuisine</Text>
        <Text style={styles.infoText}>Italian, Chinese</Text>
      </View>

      <Button title="Sign out" onPress={handleSignOut} />

    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 20,
  },
  profileImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 20,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  email: {
    fontSize: 18,
    color: 'gray',
    marginBottom: 20,
  },
  infoContainer: {
    width: '80%',
    marginVertical: 10,
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  infoText: {
    fontSize: 16,
    color: 'gray',
  },
});

export default ProfileScreen;
