import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';


const app = express();
const port = 1245;


const redisClient = redis.createClient();
const setAsync = promisify(redisClient.set).bind(redisClient);
const getAsync = promisify(redisClient.get).bind(redisClient);


const queue = kue.createQueue();


const INITIAL_SEATS = 50;


let reservationEnabled = true;


async function reserveSeat(number) {
  await setAsync('available_seats', number);
}


async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return availableSeats ? parseInt(availableSeats, 10) : 0;
}


reserveSeat(INITIAL_SEATS);


app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});


app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  const job = queue.create('reserve_seat', {}).save(err => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});


app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    const newAvailableSeats = availableSeats - 1;

    if (newAvailableSeats < 0) {
      return done(new Error('Not enough seats available'));
    }

    await reserveSeat(newAvailableSeats);

    if (newAvailableSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});


app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
