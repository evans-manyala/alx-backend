import redis from 'redis'

const publisher = redis.createClient();

publisher.on('Connect', () => {
        console.log('Redis client connected to the server');
});

publisher.on('Error', (err) => {
        console.log('Redis client cannot connect to the server ${err.message}');
});

function publishMessage(message, time) {
        setTimeout (() => {
                console.log('About to send ${message');
                publisher.publish('holberton school channel', message);
        }, time);
}

publishMessage('Holberton Student #1 starts cpurse', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400)
