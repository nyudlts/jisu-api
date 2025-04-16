const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;
const SOLR_HOST = process.env.SOLR_HOST || 'http://localhost:8983';
const SOLR_COLLECTION = 'bookCollection';

const allowedOrigins = [
  "http://localhost:3000",
  "http://nyu-press-reader:3000"
];

const options = {
  origin: allowedOrigins,
};

// Enable CORS for frontend requests
app.use(cors({ origin: '*' }));

// Status Check route
app.get('/status-check', (req, res) => {
  res.json({ message: "NYU Press API v2. SOLR_HOST: ", SOLR_HOST });
});

// Route to create a Solr collection
app.get('/create-collection', async (req, res) => {
  try {
    const params = {
      action: "CREATE",
      name: "bookCollection",
      numShards: "1",
      collection_configName: "_default"
    };

    const response = await axios.get(`${SOLR_HOST}/solr/admin/collections`, { params });
    res.json({ message: "Solr Collection Created Successfully", solrResponse: response.data });
  } catch (error) {
    console.error("Error creating Solr collection:", error.message);
    res.status(500).json({ error: "Failed to create Solr collection" });
  }
});

// Route to search Solr index and return highlights
app.get('/search', async (req, res) => {
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
    
    //const response = await axios.get(`${SOLR_HOST}/solr/bookCollection/select`);
    const response = await axios.get(url);
    res.json(response.data);
  } catch (error) {
    console.error("Error querying Solr:", error.message);
    res.status(500).json({ error: "Failed to query Solr" });
  }
});

app.get('/chapters', async (req, res) => {
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
    
    //const response = await axios.get(`${SOLR_HOST}/solr/bookCollection/select`);
    const response = await axios.get(url);
    res.json(response.data);
  } catch (error) {
    console.error("Error querying Solr:", error.message);
    res.status(500).json({ error: "Failed to query Solr" });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`NYU Press API running on port ${PORT}`);
});
