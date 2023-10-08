// import firebase from 'firebase/app';
// import 'firebase/storage';
import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
    apiKey: "AIzaSyDG06nyqijbTTml3ccEw3gKRFRKCUaBYHs",
    authDomain: "hidden-clock.firebaseapp.com",
    projectId: "hidden-clock",
    storageBucket: "hidden-clock.appspot.com",
    messagingSenderId: "47080518506",
    appId: "1:47080518506:web:46efe8ad31ef4286a56b13",
    measurementId: "G-50H1ETDMCS"
};

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

export {
    storage
};

// const storage = firebase.storage();

// export {
//     storage, firebase as default
// }
