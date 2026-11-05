import express from 'express';

const app = express();
app.use(express.json());

const items = new Map<number, Item>();
let nextId = 1;

app.get('/usernames', (_req, res) => {
  const usernames = [...Array(10).keys()].map((v, i) => `username_${i}`)
  res.json({count: usernames.length, usernames});
});

const port = Number(process.env.PORT ?? 3000);
app.listen(port, () => console.log(`app1 listening on port ${port}`));
