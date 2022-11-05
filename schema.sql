drop table if exists characters;
drop table if exists relationships;

CREATE TABLE characters (
    name TEXT not null,
    description TEXT
);

CREATE TABLE relationships (
    character1 TEXT,
    character2 TEXT,
    type TEXT ,
    description TEXT,
    PRIMARY KEY (character1, character2),
    FOREIGN KEY (character1) references characters(id),
    FOREIGN KEY (character2) references characters(id)
);