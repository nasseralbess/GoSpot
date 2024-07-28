
// /**
//  * Sample React Native App
//  * https://github.com/facebook/react-native
//  *
//  * @format
//  * @flow strict-local
//  */

import React from 'react';
import {SafeAreaView, StyleSheet, Text} from 'react-native';
import Navigation from './src/navigation';
import { createStackNavigator } from '@react-navigation/stack';
import { SavedProvider } from './src/context/SavedContext';

const Stack = createStackNavigator();
const App = () => {
  return (
    <SafeAreaView style={styles.root}>
      <SavedProvider>
      <Navigation />
      </SavedProvider>
    </SafeAreaView>
   
  );
};

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: '#F9FBFC',
  },
});

export default App;


////////
// import React from 'react';
// import {SafeAreaView, StyleSheet, Text} from 'react-native';
// import { NavigationContainer } from '@react-navigation/native';
// import { createStackNavigator } from '@react-navigation/stack';
// import HomeScreen from './src/screens/HomeScreen';
// import DetailScreen from './src/screens/DetailScreen/DetailScreen';
// import Navigation from './src/navigation';

// const Stack = createStackNavigator();

// export default function App() {
//   return (
//     <NavigationContainer>
//       <Stack.Navigator initialRouteName="Home">
//         <Stack.Screen name="Home" component={HomeScreen} options={{ headerShown: false }} />
//         <Stack.Screen name="Details" component={DetailScreen} options={{ title: 'User Details' }} />
//       </Stack.Navigator>
//     </NavigationContainer>
//   );
// }
