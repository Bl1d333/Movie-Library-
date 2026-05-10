import tkinter as tk
from movie_app import MovieApp
from models import MovieLibrary

def main():
    root = tk.Tk()
    library = MovieLibrary()
    app = MovieApp(root, library)
    root.mainloop()

if __name__ == "__main__":
    main()
