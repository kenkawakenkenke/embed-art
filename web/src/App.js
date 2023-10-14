
import React, { useState, useEffect, useRef } from 'react';
import './App.css';

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

function imageIndexForDate(date) {
  const hours = date.getHours() % 12;
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();
  // return hours * 60 + minutes;
  return (minutes % 12) * 60 + seconds;
}

const CenterSquareSpanningImage = ({ imageUrl }) => {
  const imgRef = useRef(null);

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

  useEffect(() => {
    window.addEventListener('resize', resizeImage);
    resizeImage();  // Initial resize

    return () => {
      window.removeEventListener('resize', resizeImage);
    };
  }, []);

  return (
    <img ref={imgRef} src={imageUrl} alt="Full Screen" style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }} />
  );
};

const useCurrentMinuteOfDay = () => {
  // const [seconds, setSeconds] = useState(0);
  // console.log("test: " + seconds);
  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setSeconds(seconds => seconds + 1);
  //   }, 1000);
  //   return () => clearInterval(interval);
  // }, []);

  const [currentImageIndex, setCurrentImageIndex] = useState(imageIndexForDate(new Date()));

  useEffect(() => {
    const checkTimeChange = () => {
      const now = new Date();
      const newIndex = imageIndexForDate(now);
      console.log("checkTimeChange: " + newIndex);
      if (newIndex !== currentImageIndex) {
        setCurrentImageIndex(newIndex);
      }
    };
    // const intervalId = setTimeout(checkTimeChange, 10 * 1000);
    const intervalId = setInterval(checkTimeChange, 1000);
    // return () => console.log("end");
    return () => {
      console.log("clear " + intervalId);
      clearInterval(intervalId);  // Clear the interval when the component is unmounted
    }
  }, []);

  return currentImageIndex;
}

function imageUrl(minuteOfDay) {
  // TODO: remove
  minuteOfDay = minuteOfDay % 100;
  return `https://storage.googleapis.com/hidden-clock/lightning_512_512/out${minuteOfDay % 720}.jpg`
}

const useLoadAnimation = (minuteOfDay) => {
  const animationStartMinuteOfDay = useRef(minuteOfDay);

  const [index, setIndex] = useState(0);

  const startTime = useRef(Date.now());
  const duration = 1000;  // Animation duration in milliseconds

  const backTrackLength = 38;
  const imageUrls = Array.from({ length: backTrackLength }, (_, i) => {
    const index = ((animationStartMinuteOfDay.current % 720) - (backTrackLength - 1) + i + 720) % 720;
    return imageUrl(index);
  });
  const isLoaded = usePrefetchImages(imageUrls);

  const animate = () => {
    const elapsed = Date.now() - startTime.current;
    const t = Math.min(elapsed / duration, 1);  // Normalize time to [0, 1]
    // const easedT = t * (2 - t);  // Ease out quad easing function
    // const easedT = 1 - Math.pow(1 - t, 12);
    const easedT = 1 - Math.pow(1 - t, 4);
    setIndex(Math.min(imageUrls.length - 1, Math.round(easedT * imageUrls.length)));

    if (elapsed < duration) {
      requestAnimationFrame(animate);
    }
  };

  useEffect(() => {
    if (isLoaded) {
      startTime.current = Date.now();
      animate();
    }
  }, [isLoaded]);

  return {
    isLoaded,
    imageUrl: index >= imageUrls.length - 1 ? imageUrl(minuteOfDay) : imageUrls[index],
  };
};

const ClockPage = ({ }) => {


  // const [seconds, setSeconds] = useState(0);
  // console.log("test: " + seconds);
  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setSeconds(seconds => seconds + 1);
  //   }, 1000);
  //   return () => clearInterval(interval);
  // }, []);

  const minuteOfDay = useCurrentMinuteOfDay();

  const animationInfo = useLoadAnimation(minuteOfDay);

  if (!animationInfo.isLoaded) {
    return (<div>Loading...</div>);
  }

  return (
    <CenterSquareSpanningImage imageUrl={animationInfo.imageUrl} />
  );
}

function App() {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const onClickView = () => {
    if (isFullscreen) {
      document.exitFullscreen();
      setIsFullscreen(false);
    } else {
      document.body.requestFullscreen();
      setIsFullscreen(true);
    }
  }

  return (
    <div className="App" onClick={onClickView}>
      <ClockPage />
    </div>
  );
}

export default App;
