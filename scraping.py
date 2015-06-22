from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import json
import sys
import sqlite3
import time


'''
campos da tabela  "Family Domains"
'''


def read_ensemble_gene_ids(filename):
    return [gene.strip() for gene in open(filename)]


def get_protein_info(url):
    if url.find('uniprot') < 0:
        return {}

    protein_page = BeautifulSoup(urllib.urlopen(url).read())
    function = protein_page.find(id='function')
    annotations = []
    keywords = []
    sites = {}
    enzyme_and_pathway = {}

    if function:
        annotations = function.findAll('div', {"class": "annotation"})
        keywords = function.findChildren('span', recursive=False)
        sites = function.find(id='sitesAnno_section')
        enzyme_and_pathway = function.find('table', {"class": "databaseTable PATHWAY"})

    return {'name': protein_page.find(id='content-protein').findChildren('h1')[0].getText(),
            'uniprot_url': url,
            'pdb_url': 'http://www.rcsb.org/pdb/protein' + url[url.rfind('/'):],
            'organism': protein_page.find(id='content-organism').findChildren('em')[0].getText(),
            # 'catalytic_activity': annotations[1].span.find(text=True, recursive=False) if len(annotations) > 2 else [],
            'keywords_molecular_function': ", ".join(
                [keyword.getText() for keyword in keywords[0].findChildren('a')]
                if len(keywords) > 2 else []),
            'keywords_biological_process': ", ".join(
                [keyword.getText() for keyword in keywords[1].findChildren('a')]
                if len(keywords) > 2 else []),
            'keywords_ligand': ", ".join(
                [keyword.getText() for keyword in keywords[2].findChildren('a')]
                if len(keywords) > 2 else []),
            # 'pathway': annotations[2].a.getText() if len(annotations) > 2 else [],
            'interactions': ", ".join(parse_table_interactions(protein_page.find(id="interaction"))),
            'names_and_taxonomy': parse_table_names_and_taxonomy(protein_page.find(id="names_and_taxonomy")),
            'sites': parse_sites(sites),
            'enzyme_and_pathway': parse_pathway(enzyme_and_pathway) if enzyme_and_pathway else {}}


def parse_table_names_and_taxonomy(names_and_taxonomy_table):
    if not names_and_taxonomy_table:
        return {}

    table = names_and_taxonomy_table.findChildren('table')[0]
    trs = table.findChildren('tr')

    if len(trs) < 6:
        offset = -1
    else:
        offset = 0

    protein_names = trs[0 + offset].findChildren('td')[1].getText().replace(
        "Alternative", "\nAlternative").replace("Synon", "\nSynon")

    organism = trs[2 + offset].findChildren('td')[1].getText()

    return {'protein_names': protein_names[:protein_names.find("Imported")],
            'organism': organism[:organism.find("Imported") + 1],
            'taxonomic_identifier': trs[3 + offset].findChildren('td')[1].findChildren('a')[0].getText(),
            'taxonomic_lineage': " > ".join(
                [taxonomy.getText() for taxonomy in
                 trs[4 + offset].findChildren('td')[1].findChildren('a', recursive=False)]),
            'proteomes': ", ".join(
                [proteome.getText() for proteome in trs[5 + offset].findChildren('td')[1].findChildren('a')])
            }


def parse_table_interactions(interactions_table):
    if not interactions_table:
        return {}

    table = interactions_table.findAll('table', {'class': 'databaseTable INTERACTION'})

    if not table or table:
        return {}

    table = table[0]
    trs = table.findChildren('tr')
    results = []

    for tr in trs:
        tds = tr.findChildren('td')
        results.append(tds[0].span.find(text=True, recursive=False) + " - " + tds[1].getText())

    return results


def parse_sites(sites_table):
    if not sites_table:
        return {}

    trs = sites_table.findChildren('tr')[1:]
    results = []

    for tr in trs:
        tds = tr.findChildren('td')
        results.append({
            'feature_key': tds[0].span.find(text=True, recursive=False),
            'positions': tds[1].getText(),
            'length': tds[2].getText(),
            'description': tds[3].findChildren('span', recursive=False)[0].getText()
        })

    return results


def parse_pathway(pathway_table):
    if not pathway_table:
        return {}

    trs = pathway_table.findChildren('tr')
    results = []

    for tr in trs:
        tds = tr.findChildren('td')
        results.append(tds[0].span.find(text=True, recursive=False) + ": " + tds[1].a.getText())

    return results


def get_ensemble_transcripts(gene):
    gene_page = BeautifulSoup(urllib.urlopen('http://www.ensembl.org/Gene/Summary?db=core;g=' + gene).read())
    transcripts_table = gene_page.find(id='transcripts_table')

    if not transcripts_table:
        #print 'http://www.ensembl.org/Gene/Summary?db=core;g=' + gene + " - Nao tem ID na tabela ou nao tem tabela"
        return []

    transcripts_table_rows = transcripts_table.tbody.findChildren('tr')

    result = []
    for row in transcripts_table_rows:
        # print row
        transcript = str(row.findChildren('td')[1].a.getText())
        protein = row.findChildren('td')[6].a
        if protein:
            protein = get_protein_info(str(protein.get('href')))
        else:
            protein = {}
        transcript_url = 'http://www.ensembl.org' + str(row.findChildren('td')[1].a.get('href'))

        result.append({'transcript': transcript,
                       'protein': protein,
                       'transcript_url': transcript_url})

    return result


def get_ensemble_transcripts_for_list(gene_list):
    return [{'gene': gene, 'transcripts': get_ensemble_transcripts(gene)} for gene in gene_list]


def erase_trailing_dots(string):
    return string[:string.find('.')]


def get_ensemble_three_prime(transcript_url):
    transcript_url = transcript_url.replace("/Summary?", "/Web/ExonsSpreadsheet?").replace("/Transcript/",
                                                                                           "/Component/Transcript/")
    exons_page = BeautifulSoup(urllib.urlopen(transcript_url).read())
    exons_row = exons_page.findAll('tr')[-1]
    three_prime_td = exons_row.findChildren('td')[-1]

    return erase_trailing_dots(str(three_prime_td.div.div.pre.span.getText()))


def get_ensemble_three_prime_for_list(genes):
    for gene in genes:
        if gene['transcripts']:
            gene['three_prime'] = get_ensemble_three_prime(gene['transcripts'][0]['transcript_url'])
        #else:
            #print "Missing transcripts for " + gene['gene']


def get_proteins_for_three_prime(three_prime):
    try:
        proteins_page = urllib2.urlopen("http://rbpdb.ccbr.utoronto.ca//cgi-bin/sequence_scan.pl",
                                        urllib.urlencode({"seq": three_prime,
                                                          "thresh": 0.8})).read()

        proteins_page = BeautifulSoup(proteins_page)
        table_rows = proteins_page.findAll('tr')[1:]

        return [str(row.findChildren('td')[2].getText()) for row in table_rows]
    except urllib2.HTTPError, error:
        return ['Error. Probably the three_prime is invalid']


def add_three_prime_proteins_for_list(genes):
    for gene in genes:
        if 'three_prime' in gene:
            gene['three_prime_proteins'] = get_proteins_for_three_prime(gene['three_prime'])
        #else:
            #print "Missing three_prime for " + gene['gene']


def move_organism_up(genes):
    for gene in genes:
        for transcript in gene['transcripts']:
            if 'protein' in transcript:
                protein = transcript['protein']
                if 'organism' in protein:
                    organism = protein['organism']

                    gene['organism'] = organism
                    protein.pop('organism')


def full_process(gene_ids):
    # gene_ids = [gene_ids[0]]

    genes = get_ensemble_transcripts_for_list(gene_ids)
    #print 'Got Transcripts'

    move_organism_up(genes)

    get_ensemble_three_prime_for_list(genes)
    #print 'Got ThreePrimes'

    add_three_prime_proteins_for_list(genes)
    #print 'Got ThreePrime Proteins'

    return genes


if __name__ == "__main__":
    infilename = "genes.ensemble"
    outfilename = "teste.json"

    single = False
    if len(sys.argv) > 1:
        single = True
        final = full_process([str(sys.argv[1])])
    else:
        final = full_process(read_ensemble_gene_ids(infilename))

    #print json.dumps(final)

    if not single:
        with open(outfilename, 'w') as data_output:
            data_output.write(json.dumps(final))
            data_output.close()
    else:
        con = None
        try:
            con = sqlite3.connect('../../proteinDatabase.db')
            data = final
            with con:
                cur = con.cursor()
                for gene in data:
                    cur.execute("INSERT OR IGNORE INTO Genes VALUES(?, ?, ?, ?, ?)", (gene['gene'], gene.get('organism') , gene.get('three_prime') , time.strftime("%H:%M:%S") , time.strftime("%H:%M:%S")))
                    for transcripts in gene['transcripts']:
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
                            cur.execute("INSERT OR IGNORE INTO ThreePrimeProtein VALUES(?, ?, ?, ?)", (time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S"), three_prime_protein, gene['gene']))

                print '0'
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
        finally:
            if con:
                con.commit()
                con.close()

    '''
    with open('teste.json') as data_file:
        data = json.load(data_file)
        print json.dumps(data)
    '''