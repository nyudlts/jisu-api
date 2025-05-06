import pysolr
import ebooklib
from ebooklib import epub
import warnings
from bs4 import BeautifulSoup
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import base64

## Ingests all epub books in the 'docs' directory into Solr
## As documents with the following fields:
## href, content, chars, chapterTitle, bookTitle

# Solr setup - Update with your Solr URL and core/collection name
SOLR_COLLECTION = "bookCollection"
SOLR_URL = "http://localhost:8983/solr/" + SOLR_COLLECTION

def parse_epub(file_path):

    # supress ebooklib ignore_ncx warnings
    warnings.filterwarnings("ignore", message="In the future version we will turn default option ignore_ncx to True.")
    warnings.filterwarnings("ignore", message="This search incorrectly ignores the root element,")

    """
    Parses the EPUB file and extracts chapters as a list of dictionaries.
    Each dictionary represents a chapter with a title and content.
    """
    book = epub.read_epub(file_path)

    # Get base64 encoded filename since go-toolkit uses this as the book ID
    base64_filename = base64_encode(Path(file_path).name)

    # Get the root directory of the EPUB
    root_directory = get_root_directory(file_path)

    # Get the title from metadata
    meta_title = book.get_metadata('DC', 'title')
    book_title = meta_title[0][0] if meta_title else "Untitled"

    # Get the navigation (nav.xhtml) file 
    nav_item = book.get_item_with_id("nav")
    toc_nav = None
    
    if nav_item:
        # Decode and parse the nav file
        content = nav_item.get_content().decode("utf-8")
        nav_soup = BeautifulSoup(content, 'html.parser')

        # Find the toc <nav> element
        toc_nav = nav_soup.find("nav", {"epub:type": "toc"})


    # List of chapters
    chapters = []

    # Iterate over each chapter (spine item) in the EPUB
    for index, item in enumerate(book.spine):
        item_id = item[0]  # The spine item identifier
        item = book.get_item_with_id(item_id)

        if item:
            # get the href of the chapter
            href = item.get_name() if item.get_name() else "Untitled"

            # Create a BeautifulSoup object from the chapter
            chapter_soup = BeautifulSoup(item.get_body_content(), 'html.parser')

            # Try to get title of the chapter by matching the href with the TOC
            if toc_nav:
                # Find the <a> tag with the matching href
                a_tag = toc_nav.find("a", href=href)
                if a_tag:
                    # Extract the text content inside the <a> tag (even if wrapped in other tags)
                    chapter_title = a_tag.get_text(strip=True)
                else:
                    # Use the filename w/o extension as the title
                    chapter_title = Path(href).stem.capitalize()
            else:
                # Use the filename w/o extension as the title
                chapter_title = Path(href).stem.capitalize()            

            # Get the text content of the chapter
            content = chapter_soup.get_text(separator="\n", strip=True)
      
            #print('==================================')
            #print('Href : ', href)
            #print('bookID : ', base64_filename)
            #print('Chapter : ', chapter_title)

            # Create a full href path to match go-toolkit manifests
            full_href = root_directory + "/" + href
    
            # Add to the chapter list
            chapters.append({"href": full_href, "content": content, "chars": len(content), "chapterTitle":chapter_title, "bookTitle": book_title, "bookID": base64_filename})

    return chapters

def base64_encode(input_string: str) -> str:
    """Encodes a string using Base64."""
    encoded_bytes = base64.b64encode(input_string.encode("utf-8"))  # Convert string to bytes, then encode
    return encoded_bytes.decode("utf-8")  # Convert bytes back to string

def get_root_directory(epub_path):
    with zipfile.ZipFile(epub_path, 'r') as zf:
        # Open META-INF/container.xml
        with zf.open('META-INF/container.xml') as f:
            content = f.read().decode('utf-8')

    # Parse XML to find the <rootfile> path
    namespace = {'n': 'urn:oasis:names:tc:opendocument:xmlns:container'}
    root = ET.fromstring(content)
    rootfile_path = root.find('n:rootfiles/n:rootfile', namespace).attrib['full-path']

    # Extract the directory (before content.opf)
    root_directory = "/".join(rootfile_path.split("/")[:-1]) if "/" in rootfile_path else ""

    return root_directory

# Chunk text into desired size
def chunk_text(text, max_chars):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        # Check if adding the word exceeds the character limit
        if len(" ".join(current_chunk + [word])) > max_chars:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def save_to_solr(chapters):
    """
    Saves the list of chapters to Solr.
    Each chapter becomes a document in the Solr index.
    """
    solr = pysolr.Solr(SOLR_URL, always_commit=True)

    # Prepare documents for Solr
    solr_docs = []
    for i, chapter in enumerate(chapters, start=1):
        #print('==================================')
        #print('Href : ', chapter["href"])
        #print('chars : ', chapter["chars"])
        #print('chapterTitle : ', chapter["chapterTitle"])
        #print('bookTitle : ', chapter["bookTitle"])
        
        solr_docs.append({
            "id": str(i),  # Unique identifier
            "href": chapter["href"],
            "content": chapter["content"],
            "chars": chapter["chars"],
            "chapterTitle": chapter["chapterTitle"],
            "bookTitle": chapter["bookTitle"],
            "bookID": chapter["bookID"]
        })

    # Add documents to Solr
    solr.add(solr_docs)
    print(f"Added {len(solr_docs)} chapters as documents to '{SOLR_COLLECTION}'.")

if __name__ == "__main__":
    # Path to the EPUB file
    import os

    epub_dir = 'docs'
    total_chapters = []
    for epub_file in os.listdir(epub_dir):
        if epub_file.endswith('.epub'):
            bookChapters = []
            epub_file_path = os.path.join(epub_dir, epub_file)
            # Process each EPUB file
            print(f"Processing {epub_file}...")
            bookChapters = parse_epub(epub_file_path)
            print(f"Extracted {len(bookChapters)} chapters.")
            total_chapters.extend(bookChapters)

    # Save chapters to Solr
    save_to_solr(total_chapters)
    print("✅ Done!")
