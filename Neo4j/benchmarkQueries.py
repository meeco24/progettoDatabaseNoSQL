from neo4j import GraphDatabase

def executeAndRecord(query, session, titolo):
    f = open(f"/home/meeco/Documenti/BD2Project/files/risultati25%.txt","a")
    f.write(f"{titolo}:\n")
    for i in range(31):
        result = session.run(query).consume()
        f.writelines(str(result.result_available_after)+"\n")
        
    f.write("\n\n\n")
    f.close()

    session.run("CALL db.clearQueryCaches()")


def main():

    uri = "neo4j://localhost:7687" #uri per connettersi al db
    driver = GraphDatabase.driver(uri, auth=("neo4j", "progetto123")) #credenziali di accesso al db

    session = driver.session()

    #query1
    query1 = """
                MATCH (a:AZIENDA)
                WHERE toInteger(a.sede) = 2 
                RETURN a
    """
    titolo1 = "Query 1. Ricerca aziende con sede in una data nazione"
    executeAndRecord(query1, session, titolo1)

    #query2
    query2 = """
                MATCH (n)-[r:POSSIEDE]->(a:AZIENDA)
                WHERE a.id = 111
                RETURN n.nome as Azionisti"""
    titolo2 = "Query 2. Ricerca azionisti di una data azienda"
    executeAndRecord(query2, session, titolo2)

    #query3
    query3 = """
                MATCH
                    (p:PERSONA)-[:NAZIONALITÀ]->(n:NAZIONE),
                    (b:BANCA)-[:SEDE]->(n),
                    (a:AZIENDA)-[:SEDE_LEGALE]->(n)
                WHERE toInteger(n.id) = 0
                RETURN p, b, a, n.nome
    """
    titolo3 = "Query 3. Ricerca persone, banche e aziende con nazionalità comune"
    executeAndRecord(query3, session, titolo3)

    #query4
    query4 = """
            MATCH (b:BANCA)-[r:TRANSAZIONE_IN_ENTRATA]->(a:AZIENDA)
            WHERE a.id = 111
            RETURN COUNT(r) AS Numero_transazioni_in_entrata
    """
    titolo4 = "Query 4. Ricerca numero transazioni in entrata di una data azienda"
    executeAndRecord(query4, session, titolo4)

    #query5
    query5 = """
                MATCH (a:AZIENDA)-[t:TRANSAZIONE_IN_USCITA]->(b:BANCA),
                      (x)-[p:POSSIEDE]->(c:AZIENDA)
                WHERE t.id = 0 and c.id = t.beneficiario and p.quota >= 50
                RETURN x.nome AS maggiori_azionisti
    """
    titolo5 = "Query 5. Ricerca maggiori beneficiari di una data transazione"
    executeAndRecord(query5, session, titolo5)

if __name__ == "__main__":
    main()