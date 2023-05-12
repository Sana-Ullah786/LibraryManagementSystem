import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.book.router_init import router
from src.models.book import Book


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)) -> Book:
    """
    Endpoint to get book by id
    """
    book = db.execute(select(Book).where(Book.id == book_id)).scalars().first()
    if book:
        logging.info(f"Book with id : {book_id} requested")
        return book

    if not book:
        logging.info(f"Book id : {book_id} not Found")
        raise http_exception()


def http_exception() -> dict:
    return HTTPException(status_code=404, detail="Book not found")


def succesful_response() -> dict:
    return {"status": 201, "transaction": "succesful_response"}