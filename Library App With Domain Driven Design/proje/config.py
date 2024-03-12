import os
from sqlalchemy import create_engine

class Config:
    # SQLite veritabanı varsayılan olarak kullanılır
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///mydatabase.db")

    def create_engine_with_isolation_level(self):
        if self.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
            # SQLite kullanılıyorsa, izolasyon seviyesi ayarlanmaz
            engine = create_engine(self.SQLALCHEMY_DATABASE_URI)
        else:
            # Diğer veritabanları için izolasyon seviyesini SERIALIZABLE olarak ayarla
            engine = create_engine(self.SQLALCHEMY_DATABASE_URI, isolation_level="SERIALIZABLE")

        return engine
