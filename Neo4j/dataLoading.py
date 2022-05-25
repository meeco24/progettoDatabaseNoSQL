from neo4j import GraphDatabase

#CONNESSIONE AL DB
uri = "neo4j://localhost:7687" #uri per connettersi al db
driver = GraphDatabase.driver(uri, auth=("neo4j", "dioporco123")) #credenziali di accesso al db

#query per caricare il csv con i dati sulle PERSONE sul database
loadPersone = """
call apoc.load.csv('file:///persone.csv')
yield map as row
merge (p:PERSONA {nome:row.nome, id:toInteger(row.id), data_nascita:row.data_nascita, nazionalita:row.nazionalita})
        """

#query per caricare il csv con i dati sulle AZIENDE sul database
loadAziende = """
call apoc.load.csv('file:///aziende.csv')
yield map as row
merge (a:AZIENDA {nome:row.nome, id:toInteger(row.id), data_fondazione:row.data_fondazione, sede:row.sede})
        """

#query per caricare il csv con i dati sulle AZIENDE posseduto da persone sul database
loadAziendePersona = """
call apoc.load.csv('file:///aziende2.csv')
yield map as row
merge (a:AZIENDA {nome:row.nome, id:toInteger(row.id), data_fondazione:row.data_fondazione, sede:row.sede})
        """

#query per caricare il csv con i dati sulle BANCHE sul database
loadBanche = """
call apoc.load.csv('file:///banche.csv')
yield map as row
merge (b:BANCA {id:toInteger(row.id), nome:row.nome, sede:row.sede})
        """

#query per caricare il csv con i dati sulle NAZIONI sul database
loadNazioni = """
call apoc.load.csv('file:///nazioni.csv')
yield map as row
merge (n:NAZIONE {id:toInteger(row.id), nome:row.nome})
        """

#ESECUZIONE QUERIES
session = driver.session()

session.run(loadPersone)
session.run(loadAziende)
session.run(loadAziendePersona)
session.run(loadBanche)
session.run(loadNazioni)
