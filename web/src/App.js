
import React, { useState, useEffect, useRef } from 'react';
import logo from './logo.svg';
import './App.css';
import { storage } from './firebase';
import { useSpring, useSpringValue, animated } from 'react-spring';

const usePrefetchImages = (imageUrls) => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    let loadedCount = 0;
    const totalImages = imageUrls.length;

    const imageElements = imageUrls.map(url => {
      const img = new Image();
      img.src = url;
      img.onload = () => {
        loadedCount += 1;
        if (loadedCount === totalImages) {
          setIsLoaded(true);
        }
      };
      return img;
    });

    return () => {
      imageElements.forEach(img => {
        img.onload = null;  // Cleanup onload handlers to prevent memory leaks
      });
    };
  }, [imageUrls]);

  return isLoaded;
};


const CenterSquareSpanningImage = ({ src }) => {
  const [index, setIndex] = useState(0);
  const imgRef = useRef(null);
  const startTime = useRef(Date.now());
  const duration = 3000;  // Animation duration in milliseconds

  const imageUrls = Array.from({ length: 60 }, (_, i) => `https://storage.googleapis.com/hidden-clock/factory_768_576/out${i}.jpg`);
  const isLoaded = usePrefetchImages(imageUrls);

  const resizeImage = () => {
    const img = imgRef.current;
    const importantSize = Math.min(img.naturalWidth, img.naturalHeight);
    if (window.innerWidth > window.innerHeight) {
      const renderHeight = Math.floor(img.naturalHeight * window.innerHeight / importantSize);
      img.style.height = `${renderHeight}px`;
      img.style.width = 'auto';
    } else {
      const renderWidth = Math.floor(img.naturalWidth * window.innerWidth / importantSize);
      img.style.width = `${renderWidth}px`;
      img.style.height = 'auto';
    }
  };

  const animate = () => {
    const elapsed = Date.now() - startTime.current;
    const t = Math.min(elapsed / duration, 1);  // Normalize time to [0, 1]
    // const easedT = t * (2 - t);  // Ease out quad easing function
    // const easedT = 1 - Math.pow(1 - t, 12);
    const easedT = 1 - Math.pow(1 - t, 2);
    setIndex(Math.min(imageUrls.length - 1, Math.round(easedT * imageUrls.length)));

    if (elapsed < duration) {
      requestAnimationFrame(animate);
    }
  };

  useEffect(() => {
    if (isLoaded) {
      startTime.current = Date.now();
      window.addEventListener('resize', resizeImage);
      resizeImage();  // Initial resize
      animate();  // Start animation

      return () => {
        window.removeEventListener('resize', resizeImage);
      };
    }
  }, [isLoaded]);

  console.log(index);
  const imageUrl = `https://storage.googleapis.com/hidden-clock/out${index}.jpg`;

  if (!isLoaded) {
    return (<div>Yo</div>);
  }

  return (
    <div>
      <div>index:{index}</div>
      <animated.img ref={imgRef} src={imageUrl} alt="Full Screen" style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }} />
    </div>
  );
}

function App() {
  const src = "https://storage.googleapis.com/hidden-clock/out5.jpg";
  return (
    <div className="App">
      <CenterSquareSpanningImage src={src} />
    </div>
  );
}

export default App;
