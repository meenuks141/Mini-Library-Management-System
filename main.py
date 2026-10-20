from datetime import datetime, timedelta
import os
BOOKS_FILE = "books.txt"
RECORDS_FILE = "borrowing_records.txt"
BORROWING_PERIOD = 14
books = []
borrowing_records = []
def load_books():
    """Load book details from the text file."""
    global books
    if not os.path.exists(BOOKS_FILE):
        books = [
            {
                "id": 1,
                "title": "Python Basics",
                "author": "John Smith",
                "available": True,
                "borrower": None
            },
            {
                "id": 2,
                "title": "Data Structures",
                "author": "Mark Allen",
                "available": True,
                "borrower": None
            },
            {
                "id": 3,
                "title": "Introduction to AI",
                "author": "Sarah James",
                "available": True,
                "borrower": None
            }
        ]
        save_books()
        return

    books = []
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.rstrip("\n").split("|")
            if len(parts) != 5:
                continue
            book_id, title, author, available, borrower = parts
            books.append({
                "id": int(book_id),
                "title": title,
                "author": author,
                "available": available == "True",
                "borrower": borrower if borrower else None
            })
def save_books():
    """Save book details to a text file."""
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        for book in books:
            borrower = book["borrower"] or ""
            file.write(
                f'{book["id"]}|{book["title"]}|{book["author"]}|'
                f'{book["available"]}|{borrower}\n'
            )
def load_records():
    """Load borrowing history from the text file."""
    global borrowing_records
    borrowing_records = []
    if not os.path.exists(RECORDS_FILE):
        return
    with open(RECORDS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.rstrip("\n").split("|")
            if len(parts) != 6:
                continue
            book_id, borrower, borrow_date, due_date, return_date, status = parts
            borrowing_records.append({
                "book_id": int(book_id),
                "borrower": borrower,
                "borrow_date": borrow_date,
                "due_date": due_date,
                "return_date": return_date if return_date else None,
                "status": status
            })
def save_records():
    """Save borrowing records to a text file."""
    with open(RECORDS_FILE, "w", encoding="utf-8") as file:
        for record in borrowing_records:
            file.write(
                f'{record["book_id"]}|'
                f'{record["borrower"]}|'
                f'{record["borrow_date"]}|'
                f'{record["due_date"]}|'
                f'{record["return_date"] or ""}|'
                f'{record["status"]}\n'
            )
def add_book():
    """Add a new book to the library."""
    print("\n--- Add a New Book ---")
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    if not title or not author:
        print("Error: Title and author cannot be empty.")
        return
    new_id = max((book["id"] for book in books), default=0) + 1
    book = {
        "id": new_id,
        "title": title,
        "author": author,
        "available": True,
        "borrower": None
    }
    books.append(book)
    save_books()
    print(f"Book added successfully! Book ID: {new_id}")
def display_books():
    """Display all books in the library."""
    print("\n--- All Library Books ---")
    if not books:
        print("No books available in the library.")
        return
    for book in books:
        status = "Available" if book["available"] else "Borrowed"
        print(f'\nID: {book["id"]}')
        print(f'Title: {book["title"]}')
        print(f'Author: {book["author"]}')
        print(f'Status: {status}')
        if book["borrower"]:
            print(f'Borrower: {book["borrower"]}')
def search_book():
    """Search for a book by title or author."""
    print("\n--- Search Books ---")
    keyword = input("Enter book title or author: ").strip().lower()
    if not keyword:
        print("Please enter a search term.")
        return
    found = False
    for book in books:
        if (
            keyword in book["title"].lower()
            or keyword in book["author"].lower()
        ):
            status = "Available" if book["available"] else "Borrowed"
            print(
                f'\nID: {book["id"]} | '
                f'Title: {book["title"]} | '
                f'Author: {book["author"]} | '
                f'Status: {status}'
            )
            found = True
    if not found:
        print("No matching books found.")
def borrow_book():
    """Allow a user to borrow an available book."""
    print("\n--- Borrow a Book ---")
    try:
        book_id = int(input("Enter book ID: "))
    except ValueError:
        print("Error: Please enter a valid numeric book ID.")
        return
    borrower = input("Enter your name: ").strip()
    if not borrower:
        print("Error: Borrower's name cannot be empty.")
        return
    book = next(
        (item for item in books if item["id"] == book_id),
        None
    )
    if book is None:
        print("Error: Book ID not found.")
        return
    if not book["available"]:
        print(f'Error: "{book["title"]}" is already borrowed.')
        return
    borrow_date = datetime.now().date()
    due_date = borrow_date + timedelta(days=BORROWING_PERIOD)
    book["available"] = False
    book["borrower"] = borrower
    record = {
        "book_id": book_id,
        "borrower": borrower,
        "borrow_date": borrow_date.isoformat(),
        "due_date": due_date.isoformat(),
        "return_date": None,
        "status": "Borrowed"
    }
    borrowing_records.append(record)
    save_books()
    save_records()
    print(f'\nSuccessfully borrowed "{book["title"]}".')
    print(f"Borrower: {borrower}")
    print(f"Borrow date: {borrow_date}")
    print(f"Due date: {due_date}")
def return_book():
    """Allow a user to return a borrowed book."""
    print("\n--- Return a Book ---")
    try:
        book_id = int(input("Enter book ID: "))
    except ValueError:
        print("Error: Please enter a valid numeric book ID.")
        return
    book = next(
        (item for item in books if item["id"] == book_id),
        None
    )
    if book is None:
        print("Error: Book ID not found.")
        return
    if book["available"]:
        print("This book is not currently borrowed.")
        return
    borrower = book["borrower"]
    active_record = None
    for record in reversed(borrowing_records):
        if (
            record["book_id"] == book_id
            and record["status"] == "Borrowed"
        ):
            active_record = record
            break
    if active_record is None:
        print("Error: No active borrowing record found.")
        return
    return_date = datetime.now().date()
    due_date = datetime.strptime(
        active_record["due_date"], "%Y-%m-%d"
    ).date()
    active_record["return_date"] = return_date.isoformat()
    active_record["status"] = "Returned"
    book["available"] = True
    book["borrower"] = None
    save_books()
    save_records()
    print(f'\nSuccessfully returned "{book["title"]}".')
    print(f"Borrower: {borrower}")
    print(f"Return date: {return_date}")
    if return_date > due_date:
        print(f"Notice: Book returned { (return_date - due_date).days } day(s) late.")
    else:
        print("Book returned on time.")
def display_overdue_books():
    """Identify borrowed books past their due dates."""
    print("\n--- Overdue Books ---")
    today = datetime.now().date()
    found = False
    for record in borrowing_records:
        if record["status"] != "Borrowed":
            continue
        due_date = datetime.strptime(
            record["due_date"], "%Y-%m-%d"
        ).date()
        if today > due_date:
            book = next(
                (
                    item for item in books
                    if item["id"] == record["book_id"]
                ),
                None
            )
            title = book["title"] if book else "Unknown Book"
            overdue_days = (today - due_date).days
            print(f'\nBook: {title}')
            print(f'Book ID: {record["book_id"]}')
            print(f'Borrower: {record["borrower"]}')
            print(f'Due date: {due_date}')
            print(f'Days overdue: {overdue_days}')
            found = True
    if not found:
        print("There are no overdue books.")
def display_borrowing_records():
    """Display all borrowing and returning records."""
    print("\n--- Borrowing History ---")
    if not borrowing_records:
        print("No borrowing records found.")
        return
    for record in borrowing_records:
        book = next(
            (
                item for item in books
                if item["id"] == record["book_id"]
            ),
            None
        )
        title = book["title"] if book else "Unknown Book"
        print(f'\nBook: {title}')
        print(f'Book ID: {record["book_id"]}')
        print(f'Borrower: {record["borrower"]}')
        print(f'Borrow date: {record["borrow_date"]}')
        print(f'Due date: {record["due_date"]}')
        print(f'Return date: {record["return_date"] or "Not returned"}')
        print(f'Status: {record["status"]}')
def library_summary():
    """Display statistics about the library."""
    print("\n--- Library Summary ---")
    total_books = len(books)
    available_books = sum(
        1 for book in books if book["available"]
    )
    borrowed_books = total_books - available_books
    active_records = [
        record for record in borrowing_records
        if record["status"] == "Borrowed"
    ]
    today = datetime.now().date()
    overdue_count = sum(
        1 for record in active_records
        if datetime.strptime(
            record["due_date"], "%Y-%m-%d"
        ).date() < today
    )
    print(f"Total books: {total_books}")
    print(f"Available books: {available_books}")
    print(f"Currently borrowed books: {borrowed_books}")
    print(f"Overdue books: {overdue_count}")
    print(f"Total borrowing records: {len(borrowing_records)}")
def main():
    """Run the library management application."""
    load_books()
    load_records()
    while True:
        print("\n" + "=" * 40)
        print("   MINI LIBRARY MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Add a book")
        print("2. Display all books")
        print("3. Search for a book")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. Display overdue books")
        print("7. Display borrowing history")
        print("8. Library summary")
        print("9. Save records and exit")
        choice = input("\nEnter your choice (1-9): ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            borrow_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            display_overdue_books()
        elif choice == "7":
            display_borrowing_records()
        elif choice == "8":
            library_summary()
        elif choice == "9":
            save_books()
            save_records()
            print("All records saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 9.")
if __name__ == "__main__":
    main()