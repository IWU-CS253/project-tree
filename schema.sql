drop table if exists relationships;
drop table if exists characters;

CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT
);

CREATE TABLE relationships (
    character1 INT,
    character2 INT,
    type TEXT,
    description TEXT,
    PRIMARY KEY (character1, character2, type),
    FOREIGN KEY (character1) REFERENCES characters(id) ON DELETE CASCADE,
    FOREIGN KEY (character2) REFERENCES characters(id) ON DELETE CASCADE
);