CREATE TABLE characters (
    id PRIMARY KEY AUTOINCREMENT,
    name TEXT not null,
    description TEXT
)

CREATE TABLE relationships (
    character1 PRIMARY KEY AUTOINCREMENT,
    character2 PRIMARY KEY AUTOINCREMENT,
    type = TEXT not null,
    description TEXT,
    FOREIGN KEY character1 references characters,
    FOREIGN KEY character2 references characters
)