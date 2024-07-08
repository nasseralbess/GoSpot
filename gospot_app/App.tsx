import 'react-native-gesture-handler';
import { StatusBar } from 'expo-status-bar';
import { Pressable, Text, StyleSheet, View, useWindowDimensions } from 'react-native';
import Card from "./src/components/TinderCard/Index";
import users from "./TinderAssets/data/users";
import Animated, { useSharedValue, useAnimatedStyle, withSpring, interpolate, useDerivedValue } from 'react-native-reanimated';
import { GestureDetector, GestureHandlerRootView, PanGestureHandler, Gesture } from 'react-native-gesture-handler';


const jeff = {
  name: "Jeff",
  bio: "Im Jeff",
  image: "https://notjustdev-dummy.s3.us-east-2.amazonaws.com/avatars/elon.png",

}

export default function App() {
  const {width: screenWidth} = useWindowDimensions();
  const translateX = useSharedValue(0);
  const rotate= useDerivedValue(() => interpolate( translateX.value, [0, screenWidth],  [0,60]) + 'deg');

  const cardSyle = useAnimatedStyle(() => ({
    transform: [
      {
        translateX: translateX.value,

      },
      {
        rotate: rotate.value,
      }
    ],
    // opacity : sharedValue.value,
  }));
  const handlePress = () => {
    translateX.value = withSpring(Math.random()); // Example action
  };

  const panGesture = Gesture.Pan()
    .onStart(() => {
      console.log("started");
    })
    .onUpdate((event) => {
      translateX.value = event.translationX;
    })
    .onEnd(() => {
      translateX.value = withSpring(0);
    });


  return (
    <GestureHandlerRootView style={styles.pageContainer}>
      <GestureDetector gesture={panGesture}>
        <Animated.View style={[styles.AnimatedCards, cardSyle]}>
          <Card user={users[2]} />
        </Animated.View>
      </GestureDetector>
      <Pressable onPress={handlePress}>
        <Text>Change Value</Text>
      </Pressable>

    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  pageContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  AnimatedCards: {
    width: "100%",
    alignItems: 'center',
    justifyContent: 'center',
  },
});








