import React, { useState } from 'react';
import { StyleSheet, View, Text, ImageBackground } from 'react-native';
import Swiper from 'react-native-deck-swiper';
import Like from "./TinderAssets/images/LIKE.png";
import Nope from "./TinderAssets/images/nope.png";
import users from "./TinderAssets/data/users";
import Animated from 'react-native-reanimated';

export default function HomeScreen({ navigation }) {
  const [showLike, setShowLike] = useState(false);
  const [showNope, setShowNope] = useState(false);
  const [index, setIndex] = useState(0);

  const handleSwipedLeft = (cardIndex) => {
    console.log('Swiped left:', cardIndex);
    setShowNope(true);
    setTimeout(() => {
      setShowNope(false);
    }, 500); // Show the nope image for 0.5 seconds
  };

  const handleSwipedRight = (cardIndex) => {
    console.log('Swiped right:', cardIndex);
    setShowLike(true);
    setTimeout(() => {
      setShowLike(false);
    }, 500); // Show the like image for 0.5 seconds

    // Navigate to DetailScreen
    navigation.navigate('Details', { user: users[cardIndex] });
  };

  return (
    <View style={styles.pageContainer}>
      <Swiper
        cards={users}
        renderCard={(user) => (
          <View style={styles.card}>
            <ImageBackground source={{ uri: user.image }} style={styles.image}>
              <View style={styles.cardInner}>
                <Text style={styles.name}>{user.name}</Text>
                <Text style={styles.bio}>{user.bio}</Text>
              </View>
            </ImageBackground>
          </View>
        )}
        onSwipedLeft={(cardIndex) => {
          handleSwipedLeft(cardIndex);
          setIndex(cardIndex + 1);
        }}
        onSwipedRight={(cardIndex) => {
          handleSwipedRight(cardIndex);
          setIndex(cardIndex + 1);
        }}
        onSwipedAll={() => {
          console.log('All cards swiped');
          setIndex(0); // Reset the index to loop the cards
        }}
        cardIndex={index}
        backgroundColor={'#ffffff'}
        stackSize={3}
        animateCardOpacity={true}
        verticalSwipe={false}
      />
      {showLike && (
        <Animated.Image 
          source={Like} 
          style={[styles.like]} 
          resizeMode="contain" 
        />
      )}
      {showNope && (
        <Animated.Image 
          source={Nope} 
          style={[styles.nope]} 
          resizeMode="contain" 
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  pageContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    width: "100%",
    height: "100%",
    borderRadius: 10,
    overflow: "hidden",
    justifyContent: "flex-end",
  },
  card: {
    flex: 1,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: "#E8E8E8",
    justifyContent: "center",
    backgroundColor: "white",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 11,
    },
    shadowOpacity: 0.36,
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
  },
  like: {
    width: 100,
    height: 100,
    position: "absolute",
    top: 50,
    left: '50%',
    transform: [{ translateX: -50 }],
    zIndex: 1000, // Ensure the like image appears above other elements
  },
  nope: {
    width: 100,
    height: 100,
    position: "absolute",
    top: 50,
    left: '50%',
    transform: [{ translateX: -50 }],
    zIndex: 1000, // Ensure the nope image appears above other elements
  },
});
