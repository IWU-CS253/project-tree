drop table if exists characters;
drop table if exists relationships;
drop table if exists trees;
drop table if exists colors;

CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT not null,
    description TEXT,
    tree_id_character INT
);

CREATE TABLE relationships (
    character1 INT,
    character2 INT,
    type TEXT,
    description TEXT,
    tree_id_relationship INT,
    PRIMARY KEY (character1, character2, type),
    FOREIGN KEY (character1) references characters(id) ON DELETE CASCADE,
    FOREIGN KEY (character2) references characters(id) ON DELETE CASCADE
);

CREATE TABLE trees  (
    tree_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tree_name TEXT
);

CREATE TABLE colors  (
    tree_id_color INT,
    color TEXT,
    type TEXT
);