LOAD DATA
INFILE 'aziende6250.csv'
INFILE 'aziende-6250.csv'
INSERT INTO TABLE aziende
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
id,
nome,
data_fondazione,
quotazioni FILLER char(300),
sede_legale
)
