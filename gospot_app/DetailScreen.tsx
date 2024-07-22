import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';

export default function DetailScreen({ route }) {
  const { user } = route.params;

  return (
    <View style={styles.container}>
      <Text> Woooow, U got more details!!!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  image: {
    width: 200,
    height: 200,
    borderRadius: 100,
    marginBottom: 20,
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
