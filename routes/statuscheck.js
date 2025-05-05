import { Router } from 'express';

const router = Router();
const SOLR_HOST = process.env.SOLR_HOST || 'http://localhost:8983';

router.get('/', (req, res) => {
    res.json({ message: "NYU Press API OK.", SOLR_HOST });
});

export default router;
