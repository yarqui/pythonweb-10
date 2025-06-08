class Config:
    SQLALCHEMY_DATABASE_URL = (
        "postgresql+asyncpg://postgres:finalpassword@localhost:5432/contactapp-db"
    )


config = Config()
