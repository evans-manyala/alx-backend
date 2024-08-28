import kue from 'kue';
import { expect } from 'chai';
import { createPushNotificationsJobs } from './8-job.js'; // Adjust the path as needed

describe('createPushNotificationsJobs', () => {
    let queue;

    beforeEach(() => {
        // Create a new Kue queue
        queue = kue.createQueue();
        
        // Enter test mode
        queue.testMode.enter();
    });

    afterEach(() => {
        // Clear the queue and exit test mode
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('should create jobs and add them to the queue', () => {
        // Define sample jobs
        const jobs = [
            { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
            { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' }
        ];

        // Call the function to add jobs to the queue
        createPushNotificationsJobs(jobs, queue);

        // Validate the jobs in the queue
        const jobsInQueue = queue.testMode.jobs;

        expect(jobsInQueue).to.have.lengthOf(2);

        jobs.forEach((jobData, index) => {
            const job = jobsInQueue[index];
            expect(job.data).to.deep.equal(jobData);
            expect(job.type).to.equal('push_notification_code_3');
        });
    });
});
