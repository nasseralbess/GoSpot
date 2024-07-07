import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import Card from "./src/components/TinderCard/Index";


export default function App() {
  return (
    <View style={styles.container}>
      <Text>Hello as</Text>
      <Card/>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});



// import Card from "./src/components/TinderCard/Index";
// import users from "./assets/data/users"
// const jeff = {
//     name: "Jeff",
//     bio: "Im Jeff", 
//     image: "",

// }
// const App = () => {
//     return (
//         <View style = {styles.pageContainer}>
//             <Card user = {user[0]} /> 

//         </View> 
//     );

// };




