import { Router } from 'express';
import axios from 'axios';

const router = Router();
const SOLR_HOST = process.env.SOLR_HOST || 'http://localhost:8983';
const SOLR_COLLECTION = 'bookCollection';

router.get('/', async (req, res) => {
    try {
        const term = req.query.q || 'Poland';  
        const query = "content:" + term;
    
        const params = new URLSearchParams({
          q: query,                                                 // Search query
          "q.op": "OR",                                             // Default operator
          fl: "id,href,bookTitle,chapterTitle,bookID,highlighting", // Fields to return
          hl: "true",                                               // Enable highlighting
          "hl.fl": "content",                                       // Field to highlight
          "hl.snippets": "100",                                     // Max number of snippets to return per 'content' field
          "hl.fragsize": "50",                                      // Max fragment size
          "hl.simple.pre": "[BEFORE]",                              // Highlight prefix
          "hl.simple.post": "[AFTER]",                              // Highlight suffix1
          "hl.maxAnalyzedChars": "900000",                          // Max number of characters to analyze. -1 causes an error
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
