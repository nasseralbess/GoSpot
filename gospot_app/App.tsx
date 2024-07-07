import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import Card from "./src/components/TinderCard/Index.tsx";
import users from "./TinderAssets/assets/data/users.tsx";
const jeff = {
    name: "Jeff",
    bio: "Im Jeff", 
    image: "https://notjustdev-dummy.s3.us-east-2.amazonaws.com/avatars/elon.png",

}

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Hello as</Text>
      <Card user = {users[3]} /> 
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




