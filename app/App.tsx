
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
import { LogtoProvider, LogtoConfig } from '@logto/rn';

const config: LogtoConfig = {
  endpoint: 'https://969ymo.logto.app/',
  appId: '3rhs9s1wql5940dy14ab5',
};


const Stack = createStackNavigator();
const App = () => {
  return (
    
   <LogtoProvider config={config}>
   <SafeAreaView style={styles.root}>
      <SavedProvider>
        <Navigation />
      </SavedProvider>
    </SafeAreaView>
 </LogtoProvider>
  );
};

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: '#F9FBFC',
  },
});

export default App;
