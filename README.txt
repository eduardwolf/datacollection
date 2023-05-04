Tento projekt slouží pro stáhnutí dat inzerátů ze dvou slovenských realitních stránek, jejich nahrání do databáze, a umožnění zobrazení pomocí API.

Po spuštění scrape.py se začnou stahovat data inzerátů ze stránek yit.sk a slnecnice.sk, pro méně časově náročné
testování další funkčnosti jsem zvolil limit 3 stránek (u každého webu pouze první 3 stránky inzerátů),
ovšem přepíšete-li toto číslo na řádcích 82 a 83 (pro všechny stránky zvolte například číslo 100), program pojede dál
dokud nedocílí limitu či dokud nebude už žádná další dostupná stránka.

Funkce pro scrape stránky yit vždy dá do web browseru nové url s další stránkou a poté stáhne data, u slnecnice toto
kvůli jejich session-managementu nefunguje, tak bylo nutné implementovat automatické nalezení a kliknutí na tlačítko
pro další stránku.

Script scrape.py nakonec dá všechna nalezená homogenní data dohromady a nahraje je do sqlite databáze do složky database.db, kterou vytvoří.

Spuštěním app.py se data zpřístupní na portu 5000. API má základní CRUD operace:

Read by ID - GET http://localhost:5000/listings/"listing_id"
Read all - GET http://localhost:5000/listings
Create - POST http://localhost:5000/listings
Update - PUT http://localhost:5000/listings/"listing_id"
Delete - DELETE http://localhost:5000/listings/"listing_id"

Každý záznam má atributy:

listing_id = id inzerátu
status = stav (např. volný)
term = termín dokončení
rooms = počet místností
interior = interiér
exterior = exteriér
price = cena
floor = podlaží