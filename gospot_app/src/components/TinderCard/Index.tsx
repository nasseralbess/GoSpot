import {Text, Image, ImageBackground ,View, StyleSheet} from "react-native";

const Card = (props) => {
    const {name, image, bio} = props.user;
 return (

        <View style = {styles.card}>
                <ImageBackground source ={{uri:image }}  style={styles.image}  > 
                    <View style = {styles.cardInner}>
                        <Text style = {styles.name}> {name} </Text>
                        <Text style = {styles.bio} >{bio} </Text>
                    </View>
                </ImageBackground>
            </View>
 );
};


const styles = StyleSheet.create({

    image: 
    {
       width: "100%",
       height: "100%",
       borderRadius: 10, 
       overflow: "hidden", 
       justifyContent: "flex-end",

    },
    card: {
        width: "95%", 
        height: "70%",
        borderRadius: 10, 

        shadowColor: "#000000",
        shadowOffset: {
            width: 0,
            height: 11,
        },
        shadowOpacity:  0.36,
        shadowRadius: 11.78,
        elevation: 15,
    },
    cardInner: {
        padding: 10,

    },
    name: {
        fontSize: 30,
        color: "white", 
        fontWeight: "bold",
        marginHorizontal: 10, 


    },
    bio: {
        fontSize: 18,
        color: "white", 
        lineHeight: 25,
    }


}); 


export default Card;