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
                        for transcriptProtein in transcripts:
                            cur.execute("INSERT OR IGNORE INTO Proteins VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S") ,transcriptProtein['name'],transcriptProtein['uniprot_url'] , transcriptProtein['pdb_url']  , transcriptProtein['taxonomic_lineage'], transcriptProtein['protein_names'] , transcriptProtein['taxonomic_identifier']  , transcriptProtein['proteomes'], transcriptProtein['interactions']  ,  transcriptProtein['keywords_molecular_function'], transcriptProtein['keywords_ligand']  ,  transcriptProtein['keywords_biological_process']))
                            cur.execute("INSERT OR IGNORE INTO Transcripts VALUES(?, ?, ?, ?)", (transcriptProtein['transcript'],transcriptProtein['transcript_url'], time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S")))
                            cur.execute("INSERT OR IGNORE INTO GeneTranscript VALUES(?, ?, ?, ?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), transcriptProtein['name'], transcriptProtein['transcript']))
                            cur.execute("INSERT OR IGNORE INTO TranscriptProtein VALUES(?,?,?,?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), gene['gene'], transcriptProtein['transcript']))



except sqlite3.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:

    if con:
        con.commit()
        con.close()
