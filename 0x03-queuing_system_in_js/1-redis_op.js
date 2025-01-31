import redis from 'redis';
const client = redis.createClient();
client.on('connect', () => {
        console.log('Redis client connected to the server');
});
client.on('error', (err) => {
        console.log('Redis client not connect4d to the server, ${err.message}');
});

function setNewSchool(schoolName, value) {
        client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
        client.get(schoolName, (err, result) => {
                if(err) {
                        console.error(err)
                        return;
                }
                console.log(result);
        });
}


displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
