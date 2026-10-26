import express from 'express';

type Item = { id: number; name: string };

const app = express();
app.use(express.json());

const items = new Map<number, Item>();
let nextId = 1;

app.get('/items', (_req, res) => {
  res.json([...items.values()]);
});

app.post('/items', (req, res) => {
  const item: Item = { id: nextId++, name: String(req.body?.name ?? '') };
  items.set(item.id, item);
  res.status(201).json(item);
});

app.get('/items/:id', (req, res) => {
  const item = items.get(Number(req.params.id));
  if (!item) return void res.status(404).json({ detail: 'Item not found' });
  res.json(item);
});

app.put('/items/:id', (req, res) => {
  const item = items.get(Number(req.params.id));
  if (!item) return void res.status(404).json({ detail: 'Item not found' });
  item.name = String(req.body?.name ?? item.name);
  res.json(item);
});

app.delete('/items/:id', (req, res) => {
  const item = items.get(Number(req.params.id));
  if (!item) return void res.status(404).json({ detail: 'Item not found' });
  items.delete(item.id);
  res.json(item);
});

const port = Number(process.env.PORT ?? 3000);
app.listen(port, () => console.log(`app1 listening on port ${port}`));
