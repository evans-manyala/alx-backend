import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
        phoneNumber: '+254729334556',
        message: 'Hello, this is a notification service',
};

const job = queue.create('push_notification_code', jobData)
        .save((err) => {
                if (err) {
                        console.error('Error creating job:', err);
                        return;
        }
        console.log('Notification job created: ${job.id}');
});

job.on('complete', () => {
        console.log('Notification job completed');
});

job.on('Fiaile', () => {
        console.log('Notification job failed');
});