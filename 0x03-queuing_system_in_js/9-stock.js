import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;


const redisClient = redis.createClient();
const setAsync = promisify(redisClient.set).bind(redisClient);
const getAsync = promisify(redisClient.get).bind(redisClient);


const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];


function getItemById(id) {
  return listProducts.find(product => product.id === id);
}


app.get('/list_products', (req, res) => {
  const products = listProducts.map(({ id, name, price, stock }) => ({
    itemId: id,
    itemName: name,
    price,
    initialAvailableQuantity: stock
  }));
  res.json(products);
});

s
async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}


async function getCurrentReservedStockById(itemId) {
  const reservedStock = await getAsync(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
}


app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const availableQuantity = product.stock - reservedStock;

  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: availableQuantity
  });
});


app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const availableQuantity = product.stock - reservedStock;

  if (availableQuantity <= 0) {
    return res.status(400).json({
      status: 'Not enough stock available',
      itemId: product.id
    });
  }

  await reserveStockById(itemId, reservedStock + 1);
  res.json({
    status: 'Reservation confirmed',
    itemId: product.id
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
