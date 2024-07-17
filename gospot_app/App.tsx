import 'react-native-gesture-handler';
import React, { useEffect, useState } from 'react';
import { StyleSheet, View, useWindowDimensions } from 'react-native';
import Card from "./src/components/TinderCard/Index";
import users from "./TinderAssets/data/users";
import Animated, { useSharedValue, useAnimatedStyle, withSpring, interpolate, runOnJS} from 'react-native-reanimated';
import { GestureDetector, GestureHandlerRootView, Gesture } from 'react-native-gesture-handler';

const ROTATION = 60;
const SWIPE_VELOCITY = 800;

export default function App() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const currentUser = users[currentIndex % users.length];
  const nextUser = users[(currentIndex + 1) % users.length];

  const { width: screenWidth } = useWindowDimensions();
  const translateX = useSharedValue(0);
  const hiddenTranslateX = 2 * screenWidth;

  const cardStyle = useAnimatedStyle(() => ({
    transform: [
      {
        translateX: translateX.value,
      },
      {
        rotate: interpolate(translateX.value, [0, hiddenTranslateX], [0, ROTATION]) + 'deg',
      },
    ],
  }));

  const nextCardStyle = useAnimatedStyle(() => ({
    transform: [
      {
        scale: interpolate(translateX.value, [-hiddenTranslateX, 0, hiddenTranslateX], [1, 0.8, 1]),
      },
    ],
    opacity: interpolate(translateX.value, [-hiddenTranslateX, 0, hiddenTranslateX], [1, 0.6, 1]),
  }));

  const panGesture = Gesture.Pan()
    .onUpdate((event) => {
      translateX.value = event.translationX;
    })
    .onEnd((event) => {
      if (Math.abs(event.velocityX) < SWIPE_VELOCITY) {
        translateX.value = withSpring(0);
        return;
      }

      translateX.value = withSpring(
        hiddenTranslateX * Math.sign(event.velocityX),
        {},
        () => {
          runOnJS(setCurrentIndex)((currentIndex + 1) % users.length);
          translateX.value = 0; // Reset translateX after swipe
        }
      );
    });

  useEffect(() => {
    translateX.value = 0;
  }, [currentIndex]);

  return (
    <GestureHandlerRootView style={styles.pageContainer}>
      {nextUser &&<View style={styles.nextCardContainer}>
        <Animated.View style={[styles.animatedCards, nextCardStyle]}>
          <Card user={nextUser} />
        </Animated.View>
      </View>} 
      
      {currentUser && <GestureDetector gesture={panGesture}>
        <Animated.View style={[styles.animatedCards, cardStyle]}>
          <Card user={currentUser} />
        </Animated.View>
      </GestureDetector>} 
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  pageContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  animatedCards: {
    width: '90%',
    height: '70%',
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'center',
  },
  nextCardContainer: {
    ...StyleSheet.absoluteFillObject,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
