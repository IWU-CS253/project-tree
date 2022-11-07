drop table if exists characters;
drop table if exists relationships;

CREATE TABLE characters (
    name TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE relationships (
    character1 TEXT,
    character2 TEXT,
    type TEXT,
    description TEXT,
    PRIMARY KEY (character1, character2, type),
    FOREIGN KEY (character1) REFERENCES characters(name) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (character2) REFERENCES characters(name) ON UPDATE CASCADE ON DELETE CASCADE
);