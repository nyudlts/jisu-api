# jisu-api
A simple Node.js Express server to enable api calls from the jisu-reader to the Solr database.  This project also contains python scripts for ingesting EPUB books into Solr and a 'docs' directory that should include all the EPUBs that will be available to the jisu-reader in production.

## Dev Setup
For development purposes it is possible to run this project locally.  

Dependencies:  
Node.js  
pnpm  

1.  Clone this project.
```
git clone https://github.com/nyudlts/jisu-api.git
```

2. Install npm dependencies and start the server on port 3001.
```
pnpm install
pnpm run start
```

3. Test the server.
```
//statuscheck - should show OK message and SOLR_HOST env var
http://localhost:3001/statuscheck  

//search - automatically searces for 'Poland', should see json search response
http://localhost:3001/search 

//chapters - reader bookID from querystring, should show json response
http://localhost:3001/chapters?q=OTc4MTQ3OTgxOTQ5Mi5lcHVi
```
  
## Production Setup
For production, use the [jisu-build](https://github.com/nyudlts/jisu-build) project which includes this project as a submodule. 

## Adding additional ebooks
For production, the python ingest_epub scripts will ingest all the EPUBs contained in the 'docs' directory here.  Note that 're-ingesting' existing EPUB files will not harm the data in Solr so the contents of the 'docs' directory should include all the EPUBs that will be available in jisu-reader.

The 'docs' directory here is also setup as a Docker Pages directory used by the [jisu-pub-server](https://github.com/nyudlts/jisu-pub-server) project.  See that project's ReadMe about adding new EPUB's for production.


