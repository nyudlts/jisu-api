import { Router } from 'express';
import axios from 'axios';

const router = Router();
const SOLR_HOST = process.env.SOLR_HOST || 'http://localhost:8983';
const SOLR_COLLECTION = 'bookCollection';

router.get('/', async (req, res) => {
  try {
    const term = req.query.q || '';  
    const query = "bookID:" + term;

    const params = new URLSearchParams({
      q: query,                                                 // Search query
      "q.op": "OR",                                             // Default operator
      fl: "href,chars,chapterTitle",                            // Fields to return
      "rows": "250",                                            // Number of rows to return
      "start": "0"                                              // Starting row
      
    });

    const url = `${SOLR_HOST}/solr/${SOLR_COLLECTION}/select?${params.toString()}`;
    const response = await axios.get(url);
    res.json(response.data);
  } catch (error) {
    console.error("Error querying Solr:", error.message);
    res.status(500).json({ error: "Failed to query Solr" });
  }
});

export default router;
