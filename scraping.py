from BeautifulSoup import BeautifulSoup
import urllib
import json


def read_ensemble_gene_ids(filename):
    return [gene.strip() for gene in open(filename)]


def get_ensemble_transcripts(gene):
    gene_page = BeautifulSoup(urllib.urlopen('http://www.ensembl.org//Gene/Summary?db=core;g=' + gene).read())
    transcripts_table = gene_page.find(id='transcripts_table')
    transcripts_table_rows = transcripts_table.tbody.findChildren('tr')

    return [(str(row.findChildren('td')[1].a.getText()),
             'http://www.ensembl.org' + str(row.findChildren('td')[1].a.get('href')))
            for row in transcripts_table_rows]


def get_ensemble_transcripts_for_list(gene_list):
    return {gene: get_ensemble_transcripts(gene) for gene in gene_list}


def erase_trailing_dots(string):
    return string[:string.find('.')]


def get_ensemble_three_prime(transcript_url):
    transcript_url = transcript_url.replace("/Summary?", "/Web/ExonsSpreadsheet?").replace("/Transcript/","/Component/Transcript/")
    exons_page = BeautifulSoup(urllib.urlopen(transcript_url).read())
    exons_row = exons_page.findAll('tr')[-1]
    three_prime_td = exons_row.findChildren('td')[-1]

    return erase_trailing_dots(str(three_prime_td.div.div.pre.span.getText()))


def replace_ensemble_url_with_three_prime(genes):
    for gene in genes:
        for transcript in xrange(len(genes[gene])):
            genes[gene][transcript] = (genes[gene][transcript][0], get_ensemble_three_prime(genes[gene][transcript][1]))

    return genes


def full_process(filename):
    return replace_ensemble_url_with_three_prime(get_ensemble_transcripts_for_list(read_ensemble_gene_ids(filename)))


#final = full_process('genes.ensemble')
#print json.dumps(final)

result = {"ENSRNOG00000008691": [["ENSRNOT00000012257", "aaaactgggtctcattattttcttaaacaacagcattttgtatatatgga"]], "ENSRNOG00000015288": [["ENSRNOT00000020634", "tctcatcaccttggtttccacagactttctacggacgtgaccgtttttct"]], "ENSRNOG00000028501": [["ENSRNOT00000045657", "gaaggctgaacacttcctggactacaggcatccatcctccctcctcctcc"], ["ENSRNOT00000039273", "gaaggctgaacacttcctggactacaggcatccatcctccctcctcctcc"]], "ENSRNOG00000021051": [["ENSRNOT00000028588", "cagatgccctcatttcttgggtttgggagagctgagaacccatcctcctg"]], "ENSRNOG00000025580": [["ENSRNOT00000035048", "gcaaagggttcgattgttttgttttaagcatatacgtggatccacctttt"]], "ENSRNOG00000015533": [["ENSRNOT00000020819", "gagtattgtaggaacatttgagttatttcaatcagaaaatttcacaggca"]], "ENSRNOG00000002544": [["ENSRNOT00000063810", "atcagcactgtccaactctcatttttacgactaaaaaaaaaaatctatgg"]], "ENSRNOG00000003988": [["ENSRNOT00000005317", "cactggtctgctggctgcattgatttgttgagaccctgatcttggtgtaa"]], "ENSRNOG00000015295": [["ENSRNOT00000020646", "actattctgcctctgtggttttttttttctttttgggaggggacttggag"]], "ENSRNOG00000049066": [["ENSRNOT00000008121", "gcccagagagttattaagtcttcattcagcggcctgtgcttagtttgcat"]], "ENSRNOG00000009068": [["ENSRNOT00000011999", "atgctgtctgctgagtgaaattcttttaactacgggacacctagggcctt"]], "ENSRNOG00000009134": [["ENSRNOT00000055658", "cgggatgaacgagagtaggagaaagctgccctgatctccatcaagcccca"], ["ENSRNOT00000012193", "aaccgaacgggatgaacgagagtaggagaaagctgccctgatctccatca"], ["ENSRNOT00000076305", "ggtgggtgggactgggctggctctctccagcaccaaagcggtttgtccca"]], "ENSRNOG00000020179": [["ENSRNOT00000027351", "ggcagactgaaaaccctgagcacccatcaagtctgacggactcgtggggg"]], "ENSRNOG00000006539": [["ENSRNOT00000008986", "atccagcacgcggctctgtgtccatcagccacacctctcctggcagctct"]], "ENSRNOG00000021872": [["ENSRNOT00000030704", "gcctctcattctttagctggcttttctgagtgagaagcgtggaagttatc"]], "ENSRNOG00000015840": [["ENSRNOT00000021646", "tccctcactgcttctctctgcattgatcccctgtatttcatgaatttccc"]], "ENSRNOG00000011254": [["ENSRNOT00000066549", "agatgaatgttttgattcagttgctggattctgtctttctccttcctctc"]], "ENSRNOG00000020937": [["ENSRNOT00000064283", "aaaaaatggtcttgatatgcgtaggatgtgtgtgaagcactgtgtgtgtg"], ["ENSRNOT00000048418", "aaaaaatggtcttgatatgcgtaggatgtgtgtgaagcactgtgtgtgtg"]], "ENSRNOG00000021881": [["ENSRNOT00000031571", "attttaatgtctacgattgtaattctaaacagaaagctgcttgagtgtgg"], ["ENSRNOT00000030056", "tccaaagccaactcaacgtctttattttctaagctttgttggaacacatt"]], "ENSRNOG00000012795": [["ENSRNOT00000017187", "caccaatgtgtgtgtgagcgtgagtctcagtggcttgtacactcagcttc"]], "ENSRNOG00000001621": [["ENSRNOT00000002209", "agacaagcccttgtccactgaactatttccctggccctcttttcactttt"]], "ENSRNOG00000025545": [["ENSRNOT00000029359", "aaaactagtatttctcatggtcttctttatcggggagggggatgctgaag"]], "ENSRNOG00000028359": [["ENSRNOT00000036155", "ctgtgttgtgagatttttcttctgattccttttgcacaatgtgtctgtgg"]], "ENSRNOG00000048373": [["ENSRNOT00000075591", "actcctgtgttggttcttaccctcctgctcctaaagggagtgagatggtt"]], "ENSRNOG00000003234": [["ENSRNOT00000004416", "accccaaggcagccaggctgtcattgctgctttctttcaccttacagatg"]], "ENSRNOG00000016829": [["ENSRNOT00000022620", "aggaccgaaccattattgggtttggggggcatcacgggggctacaggggt"]], "ENSRNOG00000016800": [["ENSRNOT00000032454", "ttttctcatttgtttctttaaattagatctctttgactcttactgttttg"]], "ENSRNOG00000016940": [["ENSRNOT00000023139", "atttatttaagtctgagccttcctttccagtttttagaccaaaaaactaa"], ["ENSRNOT00000058482", "tggaggaccaagtgttgtcttgcatacatacataagccggtcgttttcct"]], "ENSRNOG00000022173": [["ENSRNOT00000027943", "ttgcacctccacacctggcttgtaactttcctgtctatccctggggaggt"]], "ENSRNOG00000047625": [["ENSRNOT00000075174", "cctgtggttgtgactttcaggttgtctgtgggaagacaaggctctggcag"]], "ENSRNOG00000022745": [["ENSRNOT00000039234", "ttagctatgtttttgttttgattttttattgttggaggggttattatgac"]], "ENSRNOG00000013217": [["ENSRNOT00000017665", "aaaaagagtttcttttcctttttctttcagtggggaggttaacctaaact"]], "ENSRNOG00000001424": [["ENSRNOT00000001928", "aacaaaaaaaagaaaaaaaaagaaaagtcacatcaggaaaaatatctgat"], ["ENSRNOT00000059486", "aacaaaaaaaagaaaaaaaaagaaaagtcacatcaggaaaaatatctgat"], ["ENSRNOT00000075031", "cccccaggctcactggagatgtattggctgctaccctgtcccttgcttga"], ["ENSRNOT00000044841", "cccccaggctcactggagatgtattggctgctaccctgtcccttgcttga"]], "ENSRNOG00000004246": [["ENSRNOT00000005653", "aatagaaatgtggatactaaactagtggtggcgcatgcctttaatcctag"]], "ENSRNOG00000029264": [["ENSRNOT00000044291", "gggcctgctggtcactagactgcttaatcttggccattgtgtggccacag"]], "ENSRNOG00000011489": [["ENSRNOT00000015869", "cctgctgtgtgcttatttttggggttggtggggtgggagagatgagacta"]], "ENSRNOG00000011953": [["ENSRNOT00000016288", "taagcacagctgagctaaaggcagagcgggctggtgtctggtcttaggtt"]], "ENSRNOG00000010940": [["ENSRNOT00000038383", "tgtttcttattgtcattttacggtgtgaataccattggaaaaatagctag"]], "ENSRNOG00000017905": [["ENSRNOT00000067141", "acctgtcctgagtgttctctcatggtgtcagcatgggagccgcatcctgc"], ["ENSRNOT00000051352", "ccacagaacagaaaacttaaatatgattttttcttttgttatgagacagt"]], "ENSRNOG00000036662": [["ENSRNOT00000054918", "aagtatgcatgttaccttatgtgtatttaatcatgaaacttaattttgca"]], "ENSRNOG00000020417": [["ENSRNOT00000027677", "nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"]], "ENSRNOG00000016452": [["ENSRNOT00000065909", "ataagaaataaataagtggttcctcagccccttcttactggcacagcggg"]], "ENSRNOG00000010702": [["ENSRNOT00000015232", "aaagtggcaggctgcgtctctccgtgatccacatgctctcctggcctaac"]], "ENSRNOG00000049876": [["ENSRNOT00000071153", "actcggctgtcaccgcttctctgtgcagtgctagtgttcaacctgggcag"]], "ENSRNOG00000013514": [["ENSRNOT00000018240", "agatggaacttggaagtttgtgggggcggggcctgcgtcgtgggcggggc"]], "ENSRNOG00000006833": [["ENSRNOT00000061884", "aataaaaacattatatgtgcctggctcacgcctataaatccagcactcaa"]], "ENSRNOG00000024780": [["ENSRNOT00000037371", "gggtttcctcttttccttttttttttttttttttttctccatgatggagg"]], "ENSRNOG00000010230": [["ENSRNOT00000013845", "aaaaagagcgactgatgtcttttcattttctcccttatcttgcggtatca"]], "ENSRNOG00000019995": [["ENSRNOT00000027194", "agtactctactatctgctaactttgttgggcagagagctgcagcggatgg"]], "ENSRNOG00000017195": [["ENSRNOT00000023741", "cctgggtgtccttttttatttttatttttttctcctcaataacacattaa"]], "ENSRNOG00000008218": [["ENSRNOT00000010853", "gattttgcagccaagctctggcctctgctcagtttgccagctgccacatg"]], "ENSRNOG00000015717": [["ENSRNOT00000021359", "aaaaattggaataacatgttaaggtcaaatgctatctgggaagacatata"], ["ENSRNOT00000021379", "aaaaattggaataacatgttaaggtcaaatgctatctgggaagacatata"]], "ENSRNOG00000020020": [["ENSRNOT00000027118", "cagtgtcctgccgctcctcattcccttttccttctccctaccaagaccaa"]], "ENSRNOG00000007001": [["ENSRNOT00000068017", "ccaagtgatcatgccagtttgtctacaaaacttcctcaggaaagctgagt"]], "ENSRNOG00000021441": [["ENSRNOT00000010521", "gtcatagtcataccttctgatgaagttgagccaacaccagcaaagtgtaa"], ["ENSRNOT00000061858", "agaatccaagtttgtttccctttccagcatacaatgtgtcccttcccgta"]], "ENSRNOG00000019162": [["ENSRNOT00000026001", "aactatgtatttattgtgtttggaaggcagagtgagggaggagaccccag"]], "ENSRNOG00000010134": [["ENSRNOT00000013515", "aaaactatggtgtccttcaatttttgggaattgttcccactctcatcttc"]], "ENSRNOG00000004864": [["ENSRNOT00000006549", "aaacttttgagtaatagttgaaatatccttgtcgggggcgggaaatcaat"]], "ENSRNOG00000018356": [["ENSRNOT00000024850", "tttttgctaggttcttgtggtgtgggtctctgatgggttggagtattggt"]], "ENSRNOG00000012295": [["ENSRNOT00000017108", "aagttcacctgtgcaatgtgtgccacgtacggatgtgctgttcccagccc"], ["ENSRNOT00000016827", "aagttcacctgtgcaatgtgtgccacgtacggatgtgctgttcccagccc"]], "ENSRNOG00000000778": [["ENSRNOT00000001011", "agctttgctggcagaaccatgtttcttttctctttctttggggttggggg"]], "ENSRNOG00000000964": [["ENSRNOT00000001279", "cgtggacattgtgtgttgctttggggattttttctgtttctttttttttt"]], "ENSRNOG00000016930": [["ENSRNOT00000022977", "aatttctatgcctgaagtgtctaggacctctgcctgtattgtggcttaga"]], "ENSRNOG00000020388": [["ENSRNOT00000027630", "cagtctccccctacccccatttttttctttagggtcttcagagtagttaa"]], "ENSRNOG00000018077": [["ENSRNOT00000024392", "aatttaggggctttgccttcattcccaagaaatgtgtttcttgccagtta"]], "ENSRNOG00000000395": [["ENSRNOT00000000444", "aactagcaagtgctttacccccctttttcttttaaaacaggatgtgtgtg"]], "ENSRNOG00000048989": [["ENSRNOT00000073860", "gaagactatgacttttgggctcccttgctgaagtattcttagtgctgggg"], ["ENSRNOT00000074644", "gaagactatgacttttgggctcccttgctgaagtattcttagtgctgggg"]], "ENSRNOG00000012734": [["ENSRNOT00000068334", "tcagagatctactgtagttatttattttttcctttgatgataagttttga"]], "ENSRNOG00000000557": [["ENSRNOT00000000673", "aacttgcctctttttttttttttttttttccactgatttgctctgagtga"]], "ENSRNOG00000027622": [["ENSRNOT00000029493", "aatggcattgtctgtcgcgtatcagtccatgtgctctcatggtcttaaat"]]}
