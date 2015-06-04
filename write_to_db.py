import sqlite3
import sys
import json
import time


con = None

try:
    con = sqlite3.connect('./proteinDatabase.db')

    with open('result.json') as data_file:
        data = json.load(data_file)
        with con:
            cur = con.cursor()
            for gene in data:
                #print json.dumps(gene, indent=4, sort_keys=True)
                cur.execute("INSERT OR IGNORE INTO Genes VALUES(?, ?, ?, ?, ?)", (gene['gene'], gene.get('organism') , gene.get('three_prime') , time.strftime("%H:%M:%S") , time.strftime("%H:%M:%S")))
                for transcripts in gene['transcripts']:
                    #print json.dumps(transcripts, indent=4, sort_keys=True)
                    #print transcripts['protein'].get('name')
                    cur.execute("INSERT OR IGNORE INTO Transcripts VALUES(?, ?, ?, ?)", (transcripts['transcript'],transcripts['transcript_url'], time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S")))
                    if transcripts['protein'].get('name'):
                        cur.execute("INSERT OR IGNORE INTO Proteins VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" ,
                        (transcripts['protein']['name'], transcripts['protein']['uniprot_url'], transcripts['protein']['pdb_url'],
                         transcripts['protein']['names_and_taxonomy']['taxonomic_lineage'], transcripts['protein']['names_and_taxonomy']['organism'],
                         transcripts['protein']['names_and_taxonomy']['protein_names'], transcripts['protein']['names_and_taxonomy']['taxonomic_identifier'],
                         transcripts['protein']['names_and_taxonomy']['proteomes'][0], transcripts['protein']['interactions'],
                         transcripts['protein']['keywords_molecular_function'], transcripts['protein']['keywords_ligand'],
                         transcripts['protein']['keywords_biological_process'], time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S")))
                        cur.execute("INSERT OR IGNORE INTO GeneTranscript VALUES(?, ?, ?, ?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), transcripts['transcript'], gene['gene']))
                        cur.execute("INSERT OR IGNORE INTO TranscriptProtein VALUES(?,?,?,?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), transcripts['protein']['name'], transcripts['transcript']))
                    for three_prime_protein in gene['three_prime_proteins']:
                        #print json.dumps(three_prime_protein, indent=4, sort_keys=True)
                        cur.execute("INSERT OR IGNORE INTO ThreePrimeProtein VALUES(?, ?, ?, ?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), three_prime_protein, gene['gene']))




except sqlite3.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:

    if con:
        con.commit()
        con.close()
