from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field
from typing import Optional, List

# uvicorn library:app --reload    

app = FastAPI(
    title='Каталог библиотеки',
    description='RESTful API для управления каталогом книг',
    version='1.0.0'
)

class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description='Название книги')
    year: int = Field(..., ge=1000, le=2026, description='Год издания')
    author: str = Field(..., min_length=1, max_length=100, description='Автор книги')
    isbn: Optional[str] = Field(None, min_length=0, max_length=20, description='ISBN книги')
    genre: list[str] = Field(..., description='Жанр книги')
    pages: Optional[int] = Field(None, qt=0 ,description='Количество страниц')

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    year: Optional[int] = Field(None, ge=1000, le=2026)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=0, max_length=20)
    pages: Optional[int] = Field(None, qt=0)

class BookStats(BaseModel):
    count: int = Field(..., qt=1, description='Общее количество книг')
    avg: float = Field(..., qt=1, description='Средний год издания')
    authors: set = Field(..., description='Авторы')

books_db: dict[int, Book] = {
    1:  Book(title='Преступление и наказание', year=1866, author='Ф. Достоевский', pages=672, genre=('роман', 'психологический роман', 'драма')),
    2:  Book(title='Война и мир', year=1869, author='Л. Толстой', pages=1225, genre=('роман-эпопея', 'исторический роман')),
    3:  Book(title='Мастер и Маргарита', year=1967, author='М. Булгаков', pages=480, genre=('роман', 'мистика', 'сатира'), isbn='978-5-04-118123-4'),
    4:  Book(title='1984', year=1949, author='Дж. Оруэлл', pages=320, genre=('антиутопия', 'роман', 'фантастика')),
    5:  Book(title='Гарри Поттер и философский камень', year=1997, author='Дж. К. Роулинг', pages=332, genre=('фэнтези', 'роман', 'приключения'), isbn='978-5-389-07435-4'),
    6:  Book(title='Улисс', year=1922, author='Дж. Джойс', pages=732, genre=('модернизм', 'роман')),
    7:  Book(title='Три товарища', year=1936, author='Э. М. Ремарк', pages=384, genre=('роман', 'драма'), isbn='978-5-17-118123-4'),
    8:  Book(title='Гордость и предубеждение', year=1813, author='Дж. Остин', pages=432, genre=('роман', 'классика', 'любовный роман')),
    9:  Book(title='Идиот', year=1869, author='Ф. Достоевский', pages=640, genre=('роман', 'психологический роман', 'драма'), isbn='978-5-04-118124-1'),
    10: Book(title='Триумфальная арка', year=1945, author='Э. М. Ремарк', pages=480, genre=('роман', 'драма')),
    11: Book(title='Сто лет одиночества', year=1967, author='Г. Гарсиа Маркес', pages=480, genre=('магический реализм', 'роман'), isbn='978-5-17-118125-8'),
    12: Book(title='Мертвые души', year=1842, author='Н. Гоголь', pages=352, genre=('поэма', 'сатира', 'классика')),
    13: Book(title='Отцы и дети', year=1862, author='И. Тургенев', pages=288, genre=('роман', 'классика', 'драма'), isbn='978-5-04-118126-5'),
    14: Book(title='Над пропастью во ржи', year=1951, author='Дж. Сэлинджер', pages=224, genre=('роман', 'драма')),
    15: Book(title='Великий Гэтсби', year=1925, author='Ф. Фицджеральд', pages=256, genre=('роман', 'трагедия'), isbn='978-5-17-118127-2'),
    16: Book(title='Портрет Дориана Грея', year=1890, author='О. Уайльд', pages=320, genre=('роман', 'философия', 'драма')),
    17: Book(title='Анна Каренина', year=1877, author='Л. Толстой', pages=864, genre=('роман', 'драма', 'семейный роман'), isbn='978-5-04-118128-9'),
    18: Book(title='Братья Карамазовы', year=1880, author='Ф. Достоевский', pages=832, genre=('роман', 'философия', 'психологический роман')),
    19: Book(title='Тихий Дон', year=1940, author='М. Шолохов', pages=1600, genre=('роман-эпопея', 'исторический роман'), isbn='978-5-17-118129-6'),
    20: Book(title='Собачье сердце', year=1925, author='М. Булгаков', pages=160, genre=('повесть', 'сатира', 'фантастика')),
    21: Book(title='Мы', year=1920, author='Е. Замятин', pages=256, genre=('антиутопия', 'роман', 'фантастика'), isbn='978-5-04-118130-2'),
    22: Book(title='О дивный новый мир', year=1932, author='О. Хаксли', pages=320, genre=('антиутопия', 'роман', 'фантастика')),
    23: Book(title='451° по Фаренгейту', year=1953, author='Р. Брэдбери', pages=256, genre=('антиутопия', 'фантастика', 'роман'), isbn='978-5-17-118131-9'),
    24: Book(title='Марсианские хроники', year=1950, author='Р. Брэдбери', pages=320, genre=('фантастика', 'рассказы')),
    25: Book(title='Дюна', year=1965, author='Ф. Герберт', pages=704, genre=('фантастика', 'роман', 'приключения'), isbn='978-5-04-118132-6'),
    26: Book(title='Основание', year=1951, author='А. Азимов', pages=320, genre=('фантастика', 'роман')),
    27: Book(title='Кладбище домашних животных', year=1983, author='С. Кинг', pages=480, genre=('ужасы', 'роман'), isbn='978-5-17-118133-3'),
    28: Book(title='Сияние', year=1977, author='С. Кинг', pages=512, genre=('ужасы', 'роман', 'триллер')),
    29: Book(title='Убить пересмешника', year=1960, author='Х. Ли', pages=384, genre=('роман', 'драма', 'классика'), isbn='978-5-04-118134-0'),
    30: Book(title='Цветы для Элджернона', year=1966, author='Д. Киз', pages=320, genre=('фантастика', 'драма', 'роман')),
    31: Book(title='Маленький принц', year=1943, author='А. де Сент-Экзюпери', pages=112, genre=('сказка', 'философия', 'повесть'), isbn='978-5-17-118135-7'),
    32: Book(title='Хоббит, или Туда и обратно', year=1937, author='Дж. Р. Р. Толкин', pages=320, genre=('фэнтези', 'приключения', 'роман')),
    33: Book(title='Властелин колец', year=1954, author='Дж. Р. Р. Толкин', pages=1178, genre=('фэнтези', 'эпопея', 'роман'), isbn='978-5-04-118136-4'),
    34: Book(title='Игра престолов', year=1996, author='Дж. Мартин', pages=800, genre=('фэнтези', 'роман', 'эпопея')),
    35: Book(title='Ведьмак. Последнее желание', year=1993, author='А. Сапковский', pages=288, genre=('фэнтези', 'рассказы'), isbn='978-5-17-118137-1'),
    36: Book(title='Пикник на обочине', year=1972, author='А. и Б. Стругацкие', pages=256, genre=('фантастика', 'повесть', 'приключения')),
    37: Book(title='Трудно быть богом', year=1964, author='А. и Б. Стругацкие', pages=288, genre=('фантастика', 'роман', 'философия'), isbn='978-5-04-118138-8'),
    38: Book(title='Понедельник начинается в субботу', year=1965, author='А. и Б. Стругацкие', pages=256, genre=('фантастика', 'юмор', 'повесть')),
    39: Book(title='Звездные дневники Ийона Тихого', year=1957, author='С. Лем', pages=320, genre=('фантастика', 'сатира', 'рассказы'), isbn='978-5-17-118139-5'),
    40: Book(title='Солярис', year=1961, author='С. Лем', pages=288, genre=('фантастика', 'роман', 'философия')),
    41: Book(title='Москва-Петушки', year=1973, author='В. Ерофеев', pages=160, genre=('поэма', 'сатира', 'постмодернизм'), isbn='978-5-04-118140-1'),
    42: Book(title='Шум и ярость', year=1929, author='У. Фолкнер', pages=320, genre=('роман', 'модернизм')),
    43: Book(title='Старик и море', year=1952, author='Э. Хемингуэй', pages=128, genre=('повесть', 'драма', 'философия'), isbn='978-5-17-118141-8'),
    44: Book(title='Прощай, оружие!', year=1929, author='Э. Хемингуэй', pages=352, genre=('роман', 'драма', 'военный роман')),
    45: Book(title='По ком звонит колокол', year=1940, author='Э. Хемингуэй', pages=576, genre=('роман', 'драма', 'военный роман'), isbn='978-5-04-118142-5'),
    46: Book(title='Тень ветра', year=2001, author='К. Р. Сафон', pages=576, genre=('роман', 'мистика', 'драма')),
    47: Book(title='Имя розы', year=1980, author='У. Эко', pages=640, genre=('роман', 'детектив', 'исторический роман'), isbn='978-5-17-118143-2'),
    48: Book(title='Парфюмер. История одного убийцы', year=1985, author='П. Зюскинд', pages=384, genre=('роман', 'драма', 'триллер')),
    49: Book(title='Бойцовский клуб', year=1996, author='Ч. Паланик', pages=256, genre=('роман', 'сатира', 'контркультура'), isbn='978-5-04-118144-9'),
    50: Book(title='Американские боги', year=2001, author='Н. Гейман', pages=640, genre=('фэнтези', 'роман', 'мистика')),
    51: Book(title='Коралина', year=2002, author='Н. Гейман', pages=192, genre=('фэнтези', 'повесть', 'ужасы'), isbn='978-5-17-118145-6'),
    52: Book(title='Дом, в котором...', year=2009, author='М. Петросян', pages=960, genre=('роман', 'магический реализм', 'драма')),
}

next_id: int = len(books_db) + 1

# ДЗ пункт 2 <-----------------------------------------------------
@app.get('/books/stats',
         response_model = BookStats,
         status_code=200,
         summary='Статистика',
         description='Возвращает статистику: количество книг, средний год издания, список уникальных авторов')
async def stats_books():
    global books_db
    data = books_db
    count = len(data)
    if count == 0:
        raise HTTPException(status_code=404, detail=f'База данных пуста')
    avg = sum([book.year for book in data.values()]) / count
    authors = {book.author for book in data.values()}
    return BookStats(count = count, avg = avg, authors = authors)

@app.get('/books', 
         response_model=List[Book],
         summary='Получить список всех книг',
         description='Возвращает список всех книг'
         )
async def get_books(
    page: int = Query(1, ge=1, description='Номер страницы'),
    limit: int = Query(10, le=100, description='Кол-во книг на странице'),
    year_from: Optional[int] = Query(None, ge=1000, le=2026, description='Год издания (от)'),
    year_to: Optional[int] = Query(None, ge=1000, le=2026, description='Год издания (до)')
    ):
    all_books = list(books_db.values())
    if year_from is not None:
        all_books = [b for b in all_books if b.year >= year_from]
    if year_to is not None:
        all_books = [b for b in all_books if b.year <= year_to]
    
    start = (page - 1) * limit
    end = start + limit
    return all_books[start:end]

# ДЗ пункт 1 <-----------------------------------------------------
@app.get('/books/search', 
         response_model=List[Book],
         summary='Поиск книг по автору',
         description='Возвращает список книг, у которых автор совпадает с запросом')
async def search_books(
    author: str | None = Query(None, min_length=1, max_length=100, description='Автор книги'),
    genres: set[str] | None = Query(None, description='Жанр книги'), # ДЗ: поиск книги по жанрам
    year_from: Optional[int] = Query(None, ge=1000, le=2026, description='Год издания (от)'),
    year_to: Optional[int] = Query(None, ge=1000, le=2026, description='Год издания (до)'),
):
    result = list(books_db.values())

    if author:
        result = [b for b in result if author.lower() in b.author.lower()]
    if genres:
        result = [b for b in result if genres & set(b.genre)]
    if year_from:
            result = [b for b in result if b.year >= year_from]
    if year_to:
        result = [b for b in result if b.year <= year_to]
    if not result: 
        raise HTTPException(status_code=404, detail='Books not found')
    return result   

# ДЗ пункт 3 <-----------------------------------------------------
class InvalidISBNException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(InvalidISBNException)
async def invalidISBNException_handler(request: Request, exc: InvalidISBNException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Книга с isbn {exc.name} не найдена"},
    )

@app.get('/books/isbn',
    response_model=Book,
    summary='Получить книгу по ID',
    description='Возвращает книгу с указаным индентификатором'
    )
async def book_isbn(
    isbn: str = Query(..., min_length=0, max_length=20, description='ISBN книги') # ДЗ: поиск книги по ISBN
):
    for b in books_db.values():
        if hasattr(b, 'isbn'):
            if b.isbn == isbn:
                return b
    raise InvalidISBNException(isbn)

# ДЗ пункт 4 <-----------------------------------------------------
class BookRead(Book):
    id: int = Field(..., description='ID книги')
    
@app.post('/books/bulk',
    response_model=list[BookRead],
    status_code=201,
    summary='Массовое добавление книг',
    description='Позволяет массово добавлять объекты Book'
    )
async def set_books(
    books: list[Book]
):
    global books_db
    current_id = len(books_db) + 1
    list_new_books = []
    for i, book in enumerate(books, current_id):
        books_db[i] = book
        list_new_books.append(BookRead(id = i, author=book.author, title = book.title, year = book.year, genre = book.genre, isbn = book.isbn, pages=book.pages))
    return list_new_books

@app.get('/books/{book_id}',
         response_model=Book,
         summary='Получить книгу по ID',
         description='Возвращает книгу с указаным индентификатором')
async def get_book(
    book_id: int = Path(..., ge=1, description='ID книги')
):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f'Book with if {book_id} not found')
    return books_db[book_id]

@app.post('/books',
          response_model=Book,
          status_code=201,
          summary='Добавить книгу',
          description='Добавляет новый объект Book и возвращает ее с присвоенным ID')
async def create_book(book: Book):
    global next_id
    current_id = next_id
    next_id += 1
    books_db[current_id] = book
    return books_db[current_id]

@app.delete('/books/{book_id}',
            status_code=204,
            summary='Удалить книгу',
            description='Удаляет книгу по переданному ID')
async def delete_book(
    book_id: int = Path(..., ge=1, description='ID книги')
):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f'Book with if {book_id} not found')
    del books_db[book_id]
    return None
