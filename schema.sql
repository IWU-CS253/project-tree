drop table if exists characters;
drop table if exists relationships;

CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT not null,
    description TEXT
);

CREATE TABLE relationships (
    character1 INT,
    character2 INT,
    type TEXT not null,
    description TEXT,
    PRIMARY KEY (character1, character2),
    FOREIGN KEY (character1) references characters(id),
    FOREIGN KEY (character2) references characters(id)
);