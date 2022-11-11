drop table if exists characters;
drop table if exists relationships;
drop table if exists trees;

CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT not null,
    description TEXT,
    tree_id_character INT
);

CREATE TABLE relationships (
    character1 TEXT,
    character2 TEXT,
    type TEXT,
    description TEXT,
    tree_id_relationship INT,
    PRIMARY KEY (character1, character2),
    FOREIGN KEY (character1) references characters(id),
    FOREIGN KEY (character2) references characters(id)
);

CREATE TABLE trees  (
    tree_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tree_name TEXT
);