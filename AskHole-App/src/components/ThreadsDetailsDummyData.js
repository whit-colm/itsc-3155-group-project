import firebase from 'firebase';
import 'firebase/firestore';

// This is the implmentation for the dummy backend (firestore)
const firestore = firebase.firestore();

// This is just some dummy threads
const dummyThreads = async () => {
    try {
        await firestore,collection('threads').add({
            title: 'How do i get a girlfriend?',
            content: 'I just want a dommy mommy girlfriend, where can i find one?',
            answers: ['L', 'Get your money up not your funny up']
        });

        await firestore.collection('threads').add({
            title: 'Is there any hope for CS Degrees?',
            content: 'With the current job market, will the CS field lighten up when more jobs are created?',
            answers: ['Probably not, the market is oversaturated at the moment, but keeping pushing for a degree, it will be worth it in the meanwhile']
        });
    } catch (error) {
        console.error('Oopsies!, Nothing but chickens here', error);
    }
};
// calls preloaded dummyThreads
dummyThreads();