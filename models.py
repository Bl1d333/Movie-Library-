import json
import os
from typing import List, Dict, Optional

DATA_FILE = "movies.json"

class Movie:
    def __init__(self, title: str, genre: str, year: int, rating: float):
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "author": self.genre,
            "year": self.year,
            "isbn": self.rating
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Movie':
        return Movie(data["title"], data["author"], data["year"], data["isbn"])

class MovieLibrary:
    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.movies: List[Movie] = []
        self.load_movies()

    def add_movie(self, title: str, genre: str, year_str: str, rating_str: str) -> Movie:
        """Добавляет фильм с валидацией."""
        if not title.strip():
            raise ValueError("Название не может быть пустым.")
        if not genre.strip():
            raise ValueError("Жанр не может быть пустым.")
        
        try:
            year = int(year_str)
            if year < 1888 or year > 2030:
                raise ValueError("Год должен быть от 1888 до 2030.")
        except ValueError:
            raise ValueError("Год должен быть целым числом.")
        
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError("Рейтинг должен быть от 0 до 10.")
        except ValueError:
            raise ValueError("Рейтинг должен быть числом от 0 до 10.")
        
        movie = Movie(title.strip(), genre.strip(), year, rating)
        self.movies.append(movie)
        self.save_movies()
        return movie

    def delete_movie(self, index: int):
        if 0 <= index < len(self.movies):
            del self.movies[index]
            self.save_movies()

    def filter_movies(self, genre: str = "", year: str = "") -> List[Movie]:
        result = self.movies
        
        if genre.strip():
            result = [m for m in result if m.genre.lower() == genre.strip().lower()]
        
        if year.strip():
            try:
                y = int(year)
                result = [m for m in result if m.year == y]
            except ValueError:
                pass
        
        return result

    def get_all_genres(self) -> List[str]:
        return sorted(list(set(m.genre for m in self.movies)))

    def save_movies(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in self.movies], f, ensure_ascii=False, indent=4)

    def load_movies(self):
        if not os.path.exists(self.filepath):
            self.movies = []
            return
        with open(self.filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                self.movies = [Movie.from_dict(item) for item in data]
            except json.JSONDecodeError:
                self.movies = []
