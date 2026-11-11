import express from 'express';
import {adjectives, generateMany, nouns} from 'unique-username-generator';

const app = express();
app.use(express.json());

// Let the test page (and other browser origins) call this API.
app.use((req, res, next) => {
  res.set({
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  if (req.method === 'OPTIONS') return void res.sendStatus(204);
  next();
});

const MIN_COUNT = 1;
const MAX_COUNT = 100;
const DEFAULT_COUNT = 10;

app.get('/usernames', (req, res) => {
  const count = req.query.count === undefined ? DEFAULT_COUNT : Number(req.query.count);
  if (!Number.isInteger(count) || count < MIN_COUNT || count > MAX_COUNT) {
    res.status(400).json({detail: `count must be an integer between ${MIN_COUNT} and ${MAX_COUNT}`});
    return;
  }

  const usernames = generateMany({dictionaries: [adjectives, nouns], count, unique: true});
  res.json({count: usernames.length, usernames});
});

app.all('/usernames', (_req, res) => {
  res.set('Allow', 'GET, HEAD').status(405).json({detail: 'Method not allowed'});
});

const port = Number(process.env.PORT ?? 3000);
app.listen(port, () => console.log(`app1 listening on port ${port}`));
