import redis from 'redi'

const subscriber = redis.createClient();

subscriber.on('Connect', () => {
        console.log('Redis client connected to the server');
});

subscriber.on('Error', (err) => {
        console.log('Redis client not connected tot he server: ${err.message}');
});

subscriber.subscribe('Holberton School Channel');

subscriber.on('Message', (channel, message) => {
        console.log('Recieved message: ${message}');
        if (message === 'KiLL_SERVER') {
                subscriber.unsubscribe('Holberton School Channel');
                subscriber.quit();
        }
});
