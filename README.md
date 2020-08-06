GET:

0.0.0.0:5000/api/books (tum kitaplari listeler, baslangicta bostur)

0.0.0.0:5000/api/books/\<id\> (id'si verilen kitabi gosterir)

POST:

0.0.0.0:5000/api/books (yeni kitap ekler)

0.0.0.0:5000/api/books/\<id\> (mevcut kitabi gunceller)

DELETE:

0.0.0.0:5000/api/books/\<id\> (mevcut kitabi siler)

*Ekleme ve guncelleme icin json body ornegi:
```json
{
    "author": "George Orwell",   
    "title": "1984"
}
```
