import express from 'express';
import {adjectives, generateMany, nouns} from 'unique-username-generator';

const app = express();
app.use(express.json());

// Log one line per request once it finishes; shows up in `docker compose logs username`.
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    console.log(`${new Date().toISOString()} ${req.method} ${req.originalUrl} ${res.statusCode} ${Date.now() - start}ms`);
  });
  next();
});

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

// The generator cuts every username to this many characters. Clients can't change it.
const USERNAME_LENGTH = 15;

app.get('/usernames', (req, res) => {
  const count = req.query.count === undefined ? DEFAULT_COUNT : Number(req.query.count);
  if (!Number.isInteger(count) || count < MIN_COUNT || count > MAX_COUNT) {
    res.status(400).json({detail: `count must be an integer between ${MIN_COUNT} and ${MAX_COUNT}`});
    return;
  }

  const usernames = generateMany({dictionaries: [adjectives, nouns], count, length: USERNAME_LENGTH, unique: true});
  res.json({count: usernames.length, usernames});
});

app.all('/usernames', (_req, res) => {
  res.set('Allow', 'GET, HEAD').status(405).json({detail: 'Method not allowed'});
});

const port = Number(process.env.PORT ?? 3000);
app.listen(port, () => console.log(`username listening on port ${port}`));
