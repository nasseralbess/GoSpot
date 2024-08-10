import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ImageBackground } from 'react-native';
import Swiper from 'react-native-deck-swiper';
import Like from "../../../TinderAssets/images/LIKE.png";
import Nope from "../../../TinderAssets/images/nope.png";
import Animated from 'react-native-reanimated';

const HomeScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const [showLike, setShowLike] = useState(false);
  const [showNope, setShowNope] = useState(false);
  const [index, setIndex] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [cards, setCards] = useState<any[]>([]);
  const [swiperKey, setSwiperKey] = useState(0);

  useEffect(() => {
    fetchDataFirst();
   
  }, []);

  useEffect(() => {
    if (index < cards.length) {
      setStartTime(Date.now());
    }
  }, [index, cards]);

  const fetchDataFirst = async () => {
    try {
      // Remember to change hte user id dynamically
      const response = await fetch('http://127.0.0.1:5000/user/get-next-spot?user_id=2');
      const data: any[] = await response.json();
      const convertedData = data.map((item, index) => ({
        id: (index + 1).toString(),
        name: item.name,
        image: item.image_url,
        bio: item.display_phone ? `Contact: ${item.display_phone}` : 'No contact information available',
      }));
      
      console.log(convertedData);
      setCards(convertedData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchingData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/user/get-next-spot?user_id=2');
      const data: any[] = await response.json();
      const convertedData = data.map((item, index) => ({
        id: (index + 1).toString(),
        name: item.name,
        image: item.image_url,
        bio: item.display_phone ? `Contact: ${item.display_phone}` : 'No contact information available',
      }));
      
      return convertedData
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  const handleSwipedLeft = (cardIndex: number) => {
    const timeSpent = Date.now() - (startTime ?? Date.now());
    console.log('Swiped left:', cardIndex, 'Time spent on card:', timeSpent, 'ms');

    setShowNope(true);
    setTimeout(() => {
      setShowNope(false);
    }, 500); // Show the nope image for 0.5 seconds
  };

  const handleSwipedRight = (cardIndex: number) => {
    const timeSpent = Date.now() - (startTime ?? Date.now());
    console.log('Swiped right:', cardIndex, 'Time spent on card:', timeSpent);

    setShowLike(true);
    setTimeout(() => {
      setShowLike(false);
    }, 500); // Show the like image for 0.5 seconds

    // Navigate to DetailScreen
    navigation.navigate('Details', { user: cards[cardIndex] });
  };

  const handleSwipedAll = async () => {
    console.log('All cards swiped');
    const newCards =  await fetchingData();
    setCards(newCards)
    console.log(newCards)
    setIndex(0); // Reset the index to loop the cards
    setSwiperKey((prevKey) => prevKey + 1);
  }

  let DEFAULT_IMAGE_URL = "https://t3.ftcdn.net/jpg/02/79/75/74/360_F_279757406_PjHAMPHNAEyf5NvyEYlC7mJNRKHHkmCz.jpg";

  return (
    <View style={styles.pageContainer}>
      <Swiper
        cards={cards}
        key={swiperKey} // Force rerender when cards change
        renderCard={(card) => (
          card ? (
            <View style={styles.card}>
              <ImageBackground
                source={{ uri: card.image || DEFAULT_IMAGE_URL }}
                style={styles.image}
              >
                <View style={styles.cardInner}>
                  <Text style={styles.name}> {card.name} </Text>
                  <Text style={styles.bio}> {card.bio} </Text>
                </View>
              </ImageBackground>
            </View>
          ) : null
        )}
        onSwipedLeft={(cardIndex) => {
          handleSwipedLeft(cardIndex);
          setIndex(cardIndex + 1);
        }}
        onSwipedRight={(cardIndex) => {
          handleSwipedRight(cardIndex);
          setIndex(cardIndex + 1);
        }}
        onSwipedAll={handleSwipedAll}
        
        cardIndex={index}
        backgroundColor={'#ffffff'}
        stackSize={3}
        marginBottom={20}
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
};

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

export default HomeScreen;
