from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import json

'''
campos da tabela  "Family Domains"
'''


def read_ensemble_gene_ids(filename):
    return [gene.strip() for gene in open(filename)]


def get_protein_info(url):
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

    print url

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
            'interactions': parse_table_interactions(protein_page.find(id="interaction")),
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
            'organism': organism[:organism.find("Imported")],
            'taxonomic_identifier': trs[3 + offset].findChildren('td')[1].findChildren('a')[0].getText(),
            'taxonomic_lineage': " > ".join(
                [taxonomy.getText() for taxonomy in
                 trs[4 + offset].findChildren('td')[1].findChildren('a', recursive=False)]),
            'proteomes': [proteome.getText() for proteome in trs[5 + offset].findChildren('td')[1].findChildren('a')]
            }


def parse_table_interactions(interactions_table):
    if not interactions_table:
        return {}

    table = interactions_table.findChildren('table')

    if not table:
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
    gene_page = BeautifulSoup(urllib.urlopen('http://www.ensembl.org//Gene/Summary?db=core;g=' + gene).read())
    transcripts_table = gene_page.find(id='transcripts_table')
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
        gene['three_prime'] = get_ensemble_three_prime(gene['transcripts'][0]['transcript_url'])


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
        gene['three_prime_proteins'] = get_proteins_for_three_prime(gene['three_prime'])


def move_organism_up(genes):
    for gene in genes:
        for transcript in gene['transcripts']:
            if 'protein' in transcript:
                protein = transcript['protein']
                if 'organism' in protein:
                    organism = protein['organism']

                    gene['organism'] = organism
                    protein.pop('organism')


def full_process(filename):
    gene_ids = read_ensemble_gene_ids(filename)
    # gene_ids = [gene_ids[0]]
    print 'Got IDs'

    genes = get_ensemble_transcripts_for_list(gene_ids)
    print 'Got Transcripts'

    move_organism_up(genes)

    get_ensemble_three_prime_for_list(genes)
    print 'Got ThreePrimes'

    add_three_prime_proteins_for_list(genes)
    print 'Got ThreePrime Proteins'

    return genes


final = full_process('genes.ensemble')
# print json.dumps(final)
with open('teste.json', 'w') as data_output:
    data_output.write(json.dumps(final))
    data_output.close()

'''
with open('teste.json') as data_file:
    data = json.load(data_file)
    print json.dumps(data)
'''