import redis from 'redis'

const 
client = redis.createClient();

client.on('Connect', () => {
        console.log('Redis client connected to the server');
});

client.on('Error', (err) => {
        console.log('Redis client cannot connect to the server: ${err.message}');
});

function createHolbertonSchools() {
        client.hset('HolbertonSchools', 'Portland', 50, redis.print)
        client.hset('HolbertonSchools', 'Seattle', 80, redis.print)
        client.hset('HolbertonSchools', 'New York', 20, redis.print)
        client.hset('HolbertonSchools', 'Bogota', 20, redis.print)
        client.hset('HolbertonSchools', 'Cali', 40, redis.print)
        client.hset('HolbertonSchools', 'Paris', 2, redis.print)
}

function displayHolbertonSchools() {
        client.hgetall('HolbertonSchools', (err, result) => {
                if(err) {
                        console.error("Error retrieving hash: ${err.message}");
                        return;
                }
                console.log(result);
        });
}

createHolbertonSchools();
displayHolbertonSchools();
