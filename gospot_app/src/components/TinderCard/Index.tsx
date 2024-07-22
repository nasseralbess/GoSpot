import {Text, Image, ImageBackground ,View, StyleSheet} from "react-native";
import Swiper from 'react-native-deck-swiper';

const Card = (props) => {
    const {name, image, bio} = props.user;
 return (

        // <View style = {styles.card}>
                // <ImageBackground source ={{uri:image }}  style={styles.image}  > 
                //     <View style = {styles.cardInner}>
                //         <Text style = {styles.name}> {name} </Text>
                //         <Text style = {styles.bio} >{bio} </Text>
                //     </View>
                // </ImageBackground>
        //     </View>
        <Swiper
        cards={users}
        renderCard={(user) => (
          <View style={styles.card}>
            {/* <Image source={{ uri: user.image }} style={styles.image} /> */}
            <Text >{name}</Text>
            <Text>{bio}</Text>
          </View>
        )}
        onSwiped={(cardIndex) => {
          console.log(cardIndex);
          setIndex(cardIndex + 1);
        }}
        onSwipedAll={() => {
          console.log('All cards swiped');
          setIndex(0); // Reset the index to loop the cards
        }}
        cardIndex={index}
        backgroundColor={'#4FD0E9'}
        stackSize={3}
      />
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
        height: "90%",
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