import sqlite3
import sys
import json
import time


con = None

try:
    con = sqlite3.connect('./proteinDatabase.db')

    with open('teste.json') as data_file:
        data = json.load(data_file)
        with con:
            cur = con.cursor()
            for gene in data:
                cur.execute("INSERT OR IGNORE INTO Genes VALUES(?, ?, ?, ?, ?)", (gene['gene'], gene['organism'] , gene['three_prime'] , time.strftime("%H:%M:%S") , time.strftime("%H:%M:%S")))
                for transcripts in gene['transcripts']:
                    print transcripts['protein']['interactions']
                    cur.execute("INSERT OR IGNORE INTO Proteins VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" ,
                                (transcripts['protein']['name'], transcripts['protein']['uniprot_url'], transcripts['protein']['pdb_url'],
                                 transcripts['protein']['names_and_taxonomy']['taxonomic_lineage'], transcripts['protein']['names_and_taxonomy']['organism'],
                                 transcripts['protein']['names_and_taxonomy']['protein_names'], transcripts['protein']['names_and_taxonomy']['taxonomic_identifier'],
                                 transcripts['protein']['names_and_taxonomy']['proteomes'][0], transcripts['protein']['interactions'],
                                 transcripts['protein']['keywords_molecular_function'], transcripts['protein']['keywords_ligand'],
                                 transcripts['protein']['keywords_biological_process'], time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S")))
                    cur.execute("INSERT OR IGNORE INTO Transcripts VALUES(?, ?, ?, ?)", (transcripts['transcript'],transcripts['transcript_url'], time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S")))
                    cur.execute("INSERT OR IGNORE INTO GeneTranscript VALUES(?, ?, ?, ?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), transcripts['name'], transcripts['transcript']))
                    cur.execute("INSERT OR IGNORE INTO TranscriptProtein VALUES(?,?,?,?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), gene['gene'], transcripts['transcript']))



except sqlite3.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:

    if con:
        con.commit()
        con.close()
