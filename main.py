from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

books_db = [] # tady bude jednoho krásného dne nějaká lepší databáze, zatím řešeno listem

app.mount("/static", StaticFiles(directory="static"), name="static")

# cesta k zatím základnímu HTML souboru -> bude nahrazen index.html -> stránka s přihlášením a registrací
@app.get("/")
async def main():
    return HTMLResponse(content=open("static/novy_zaznam.html", "r").read(), status_code=200)

# data z formuláře
@app.post("/submit_book/")
async def submit_book(title: str = Form(...), author: str = Form(...), plot: str = Form(...)):
    books_db.append({"title": title, "author": author, "plot": plot}) # přiřazení do databáze
    
    return RedirectResponse(url="/", status_code=303) # vrátí zpět ná formulář pro přidání další knihy


@app.get("/all_books/", response_class=HTMLResponse) # sznam všech přidaných knih
async def display_all_books():
    books_links_html = ""
    for i, book in enumerate(books_db):
        books_links_html += f"<li><a href='/book/{i}'>{book['title']}</a></li>" # vytvoření odkazu na každou knihu (aby šlo jednotlivou knihu rozkliknout)
    
    # hrubá představa, jak by to mělo vypadat - pravděpodobně budu předělávat
    response_content = f"""
        <html>
            <head>
                <title>Všechny knihy</title>
            </head>
            <body>
                <h1>Všechny knihy</h1>
                <ul>{books_links_html}</ul>
                <a href="/"><button>Přidat novou knihu</button></a>
            </body>
        </html>
    """
    return response_content

# detail ke každé knize
@app.get("/book/{book_id}/", response_class=HTMLResponse)
async def display_book_details(book_id: int):
    if book_id >= len(books_db):
        return HTMLResponse(content="Kniha neexistuje.", status_code=404)
    
    book = books_db[book_id]
    
    book_details_html = f"""
        <h2>{book['title']}</h2>
        <p><strong>Autor:</strong> {book['author']}</p>
        <p><strong>Děj:</strong> {book['plot']}</p>
        <a href="/all_books/"><button>Zpět na seznam všech knih</button></a>
    """
    return book_details_html


### Problémy a nápady na pokrčování: ###
# Z nějakého důvodu mi nejdou české znaky (UTF-8) v novy_zaznam.html, když jej spustím přes uvicorn

# Zatím jen hrubý náčrt toho, jak by to mělo vypadat. Následně chci přidat jednu z SQL databází, ovšem nevím jaká možnost bude optimální
# Prozatím bez CSS, případně přemýšlím i nad SCSS (pokud máte nějaké zkušenosti, budu za ně rád)
# Samozřejmě je tu i možnost javascriptu, ale tomu bych se rád vyhnul