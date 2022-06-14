from neo4j import GraphDatabase

def main():

#query creazione relazione sede banche
    sedeBanche = '''
            MATCH (b:BANCA), (n:NAZIONE)
            WHERE toInteger(b.sede) = toInteger(n.id)
            CREATE (b)-[:SEDE]->(n)
            '''

#query creazione relazione sede aziende
    sedeAziende = '''
            MATCH (a:AZIENDA), (n:NAZIONE)
            WHERE toInteger(a.sede) = toInteger(n.id)
            CREATE (a)-[:SEDE_LEGALE]->(n)
            '''

#query assegnazione quote aziende
    quotaAzienda = '''
            call apoc.load.csv('file:///aziende25000.csv')
            yield map as row
            UNWIND apoc.convert.fromJsonList(row.quotazioni) as r
                match (n:AZIENDA),(m:AZIENDA)
                WHERE toInteger(n.id) = toInteger(row.id) AND toInteger(m.id) = toInteger(r.azionista)
                create (n)<-[:POSSIEDE {quota:r.quota}]-(m)
            '''

#query assegnazione quote persone
    quotaAziendaPersona = '''
            call apoc.load.csv('file:///aziende25000.csv')
            yield map as row
            UNWIND apoc.convert.fromJsonList(row.quotazioni) as r
                match (n:AZIENDA),(m:PERSONA)
                WHERE toInteger(n.id) = toInteger(row.id) AND toInteger(m.id) = toInteger(r.azionista)
                create (n)<-[:POSSIEDE {quota:r.quota}]-(m)
            '''

#query per creare le transazioni in uscita azienda->banca
    transazioniInUscita = """
            call apoc.load.csv('file:///transazioni15000.csv')
            yield map as row
            match (a:AZIENDA), (b:BANCA)
            where a.id = toInteger(row.emittente) and b.id = toInteger(row.banca)
            merge (a)-[t:TRANSAZIONE_IN_USCITA {id:toInteger(row.id), codice_transazione:row.codice_transazione, importo:toFloat(row.importo), beneficiario:toInteger(row.beneficiario) ,banca:toInteger(row.banca), data:row.data}]->(b)
            """
    
#query per creare le transazioni in entrata banca->azienda
    transazioniInEntrata = """
            call apoc.load.csv('file:///transazioni15000.csv')
            yield map as row
            match (a:AZIENDA), (b:BANCA)
            where a.id = toInteger(row.beneficiario) and b.id = toInteger(row.banca)
            merge (b)-[t:TRANSAZIONE_IN_ENTRATA {id:toInteger(row.id), codice_transazione:row.codice_transazione, importo:toFloat(row.importo), beneficiario:toInteger(row.beneficiario) ,banca:toInteger(row.banca), data:row.data}]->(a)
            """

#AREA ESECUZIONE QUERIES

    uri = "neo4j://localhost:7687" #uri per connettersi al db
    driver = GraphDatabase.driver(uri, auth=("neo4j", "progetto123")) #credenziali di accesso al db

    session = driver.session()

#    session.run(sedeBanche) #relazione banche->nazioni
#    session.run(sedeAziende) #relzione aziende->nazioni

    session.run(quotaAzienda) #relazione aziende->aziende
    session.run(quotaAziendaPersona) #relazione aziende->persone
    
    session.run(transazioniInUscita) #relazione aziende->banche
    session.run(transazioniInEntrata) #relazione banche->aziende

if __name__ == "__main__":
    main()