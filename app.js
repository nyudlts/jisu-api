import express from 'express';
import cors from 'cors';
import statuscheck from './routes/statuscheck.js';
import search from './routes/search.js';
import chapters from './routes/chapters.js';

const app = express();
const PORT = 3001;

// List of allowed origins
const allowedOrigins = ['http://18.205.45.14:3000', 'http://localhost:3000'];

app.use(cors({
    origin: function (origin, callback) {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error('CORS policy error: Origin not allowed'));
      }
    }
  }));

// Use the statuscheck route
app.use('/statuscheck', statuscheck);
app.use('/search', search);
app.use('/chapters', chapters);

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});