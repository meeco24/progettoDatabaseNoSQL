LOAD DATA
INFILE 'nazioni.csv'
INSERT INTO TABLE nazioni
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
id,
nome
)
