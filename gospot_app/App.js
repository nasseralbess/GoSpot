import React from "react";
import {Text, StyleSheet} from "react-native";
import Card from "./src/components/TinderCard/Index";
import users from "./assets/data/users"
const jeff = {
    name: "Jeff",
    bio: "Im Jeff", 
    image: "",

}
const App = () => {
    return (
        <View style = {styles.pageContainer}>
            <Card user = {user[0]} /> 

        </View>
    );

};

const styles = StyleSheet.create({
    pageContainer: {
        justifyContent: "center", 
        alignItems: "center", 
        flex: 1,
    },

}); 


export default App; 