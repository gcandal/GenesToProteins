from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import json


def read_ensemble_gene_ids(filename):
    return [gene.strip() for gene in open(filename)]


def get_protein_info(url):
    protein_page = BeautifulSoup(urllib.urlopen(url).read())
    name = protein_page.find(id='content-protein').findChildren('h1')[0].getText()
    organism = protein_page.find(id='content-organism').findChildren('em')[0].getText()
    pdb_url = 'http://www.rcsb.org/pdb/protein/' + url[url.rfind('/'):]

    return {'name': name, 'uniprot_url': url, 'pdb_url': pdb_url, 'organism': organism}


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