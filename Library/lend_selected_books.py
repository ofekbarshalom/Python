def update_loaned_books(book_title, books_df):
    # Find the book in books_df and get the copies_available
    try:
        copies_available = int(books_df.loc[books_df["title"] == book_title, "copies_available"].values[0])
    except IndexError:
        print(f"Book '{book_title}' not found in the main books.csv!")
        return

    # Check if copies_available - 1 is 0
    if copies_available - 1 == 0:

        # Update the is_loaned column in books.csv to "Yes"
        books_df.loc[books_df["title"] == book_title, "is_loaned"] = "Yes"
        books_df.to_csv(Paths.BOOKS.value, index=False)
        print(f"'{book_title}' has been marked as loaned in books.csv.")

        try:
            # Load loaned_books.csv
            loaned_books_df = pd.read_csv(Paths.LOANED_BOOKS.value)
            # Add the book to loaned_books.csv
            loaned_books_entry = pd.DataFrame({"title": [book_title]})
            loaned_books_df = pd.concat([loaned_books_df, loaned_books_entry], ignore_index=True)
            loaned_books_df.to_csv(Paths.LOANED_BOOKS.value, index=False)
            # Print success message
            print(f"'{book_title}' has been loaned out. All copies are now loaned!")
        except FileNotFoundError:
            print("File loaned_books.csv does not exist")

        try:
            # Load available_books.csv
            available_books_df = pd.read_csv(Paths.AVAILABLE_BOOKS.value)

            # Remove the book from available_books.csv
            available_books_df = available_books_df[available_books_df["title"] != book_title]

            # Save the updated available_books.csv
            available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)

            print(f"'{book_title}' has been removed from available_books.csv.")

        except FileNotFoundError:
            print("File available_books.csv does not exist")
    else:
        # Print remaining copies
        print(f"'{book_title}' still has {copies_available - 1} copies available.")
        # Decrement copies_available in available_books.csv and books.csv
        try:
            # Load available_books.csv
            available_books_df = pd.read_csv(Paths.AVAILABLE_BOOKS.value)

            # Decrement copies_available for the book in available_books.csv
            available_books_df.loc[available_books_df["title"] == book_title, "copies_available"] -= 1

            # Save the updated available_books.csv
            available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)
            print(f"'{book_title}' now has {copies_available - 1} copies available in available_books.csv.")
        except FileNotFoundError:
            print("File available_books.csv does not exist")

        # Decrement copies_available in books.csv
        books_df.loc[books_df["title"] == book_title, "copies_available"] -= 1

        # Save the updated books.csv
        books_df.to_csv(Paths.BOOKS.value, index=False)
        print(f"'{book_title}' now has {copies_available - 1} copies available in books.csv.")


def update_book_availability(book_title, books_df, alert_label):
    try:
        # Load available_books.csv
        available_books_df = pd.read_csv(Paths.AVAILABLE_BOOKS.value)

        # Check if the book already exists in available_books.csv
        if book_title in available_books_df["title"].values:
            # Decrement 'copies_available' by 1
            available_books_df.loc[available_books_df["title"] == book_title, "copies_available"] -= 1
        else:
            # If the book doesn't exist, fetch its total copies and add it with 'copies_available = total_copies - 1'
            total_copies = int(books_df.loc[books_df["title"] == book_title, "copies"].values[0])
            new_entry = pd.DataFrame({"title": [book_title], "copies_available": [total_copies - 1]})
            available_books_df = pd.concat([available_books_df, new_entry], ignore_index=True)

        # Save the updated available_books.csv
        available_books_df.to_csv(Paths.AVAILABLE_BOOKS.value, index=False)

        # Update books.csv by decrementing 'copies_available' by 1
        books_df.loc[books_df["title"] == book_title, "copies_available"] -= 1
        books_df.to_csv(Paths.BOOKS.value, index=False)

        update_loaned_books(book_title, books_df)

        # Show success message
        alert_label.config(text=f"'{book_title}' availability has been updated!", fg="green")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds

    except Exception as e:
        # Handle unexpected exceptions and display an inline error message
        alert_label.config(text=f"An error occurred: {e}", fg="red")
        alert_label.after(2000, lambda: alert_label.config(text=""))  # Clear message after 2 seconds


