# my python testing with pytest

my excercises following [Python Testing with pytest, 2nd Edition](https://pythontest.com/pytest-book/)

`cards`, the simple app to follow along, fully rewritten with `click`instead of `typer` and `SQLite` + `SQLAlchemy` instead of `tynydb`

## ch03
refactored to separate context creations from `cli` module to `api`

too coupled

## ch03-1
simplyfied to the bone

likely further refactoring will be required to adapt the app structure to test - which is the point of this exercise

## ch03-2
most of db setup set in fixtures

## ch03-3
refactored to use fixtures db setp only



## next steps
once finished this project, [Test-Driven Development with Python](https://www.obeythetestinggoat.com/pages/book.html)
aka **Obey the Testing Goat!**

(in fact, took the idea of branching every chapter from there)

in the 'the goat book' the project is developed with `Django` and the tests implemented with `unittest`

I'll take the same approach as here, and use `Flask` and `pytest`





