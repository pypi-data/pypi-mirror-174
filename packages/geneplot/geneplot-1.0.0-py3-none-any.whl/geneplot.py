#!/usr/bin/env python

import os
import gffutils
import subprocess
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.colors import Color
from Bio.Graphics import GenomeDiagram
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Graphics.GenomeDiagram import CrossLink
import matplotlib.pyplot as pl
import logging


logfile = 'geneplot.all.err.log'
galllog = open(logfile, 'w'); galllog.close()
logging.basicConfig(filename=logfile, level=logging.DEBUG, filemode='a', force=True,
                format='%(asctime)s %(levelname)s %(name)s  %(funcName)s  %(module)s %(message)s')

logger=logging.getLogger(__name__)
logger.info('module initialized...'); print('--', logger)


def createGFFdb(gff3file):
    '''
    Creates a sqlite3 database of a GFF3 file with the gffutils Pyton package.
    
    :param gff3file: path to the GFF3 file
    :type gff3file: str
    '''
    
    gffutils.create_db(gff3file, dbfn=gff3file + '.db', force=True, 
                       keep_order=True, merge_strategy='merge', 
                       sort_attribute_values=True)
    
    if os.path.isfile(gff3file + '.db') == True:
        print(os.path.basename(gff3file) + '.db', 'has been created')


class genome(object):
    '''
    Instantiates a genome object with genome-associated as paths pointing to the
    data source and set as class attributes. Data include the GFF3 file of 
    genome annotation (positional), InterproScan output of protein domains 
    identified on protein-coding genes (keyword), and directory with VCF files 
    of polymorphisms (keyword).
    
    :param gff3file: path to the GFF3 file
    :type gff3file: str
    :param iprfile: path to the InterproScan's output file
    :type iprfile: str
    :param vcffiles: path to the VCF files directory
    :type vcffiles: str
    '''

    _snpimpact = {'LOW':Color(0,150/255,50/255), 'MODERATE':Color(204/255,153/255,0/255),
                 'MODIFIER':Color(255/255,0/255,255/255),
                 'HIGH':Color(255/255,0,0), 'NOANN':Color(0,0,0)}


    def __init__(self, gff3file, iprfile=None, vcffiles=None):

        print('Initializing genome class...')
        genome.gff3file = gff3file
        genome.iprfile = iprfile
        genome.vcffiles = vcffiles
        logger.info(' genome class initialized')


    class gene(object):
        '''
        Instantiates a gene object with the method plot() to represent the 
        intron/exon structure of the gene from a GFF3 file, the protein domain 
        topology from InterproScan's output, and single nucleotide 
        polymofphisms (SNPs) from VCF files.

        :param mRNAid: gene identifier (ID) according to the GFF3 file annotations.
        :type mRNAid: str
        :param proteinid: protein identifier (ID) from the InterproScan output
        :type proteinid: str
        :param description: user-defined description of the gene
        :type description: str
        '''



        def __init__(self, mRNAid, proteinid=None, description=None):

            print('Initializing gene class...')
            self.id = mRNAid
            self.proteinid = proteinid
            self.gff3file = genome.gff3file
            self.iprfile = genome.iprfile
            self.vcffiles = genome.vcffiles
            self.description = description
            self.db = gffutils.FeatureDB(genome.gff3file + '.db', keep_order=True); db = self.db

            assert db[mRNAid].featuretype == 'mRNA', 'only mRNA features are supported for \
                                                this version of the library'

            self.chrom = db[mRNAid].chrom
            self.start = db[mRNAid].start
            self.end = db[mRNAid].end
            self.strand = db[mRNAid].strand
            logger.info(self.id + ' gene class initialized')


        def _transcriptpos_to_genomepos(self):
            '''
            Calculates genome coordinates for every nucleotide position
            of the transcript according to the GFF3 and FASTA
            files provided as input during the instantiation of the gene class.
            '''
            logger.info('starting...')
            db = self.db
            try:
                mrna = self.id
                coors = []
                lencdsaccum = 0
                for cds in db.children(db[mrna], featuretype='CDS', order_by='start'):
                    lencds = cds.end + 1 - cds.start
                    coors.append(list(range(cds.start, cds.end+1)))
                    lencdsaccum += lencds
                coors = sum(coors, [])
                if db[mrna].strand == '-':
                    coors.reverse()
                dcoors = {}
                for pos in range(lencdsaccum):
                    dcoors[pos+1] = coors[pos]
                self.dcoors = dcoors
                return dcoors
            except Exception as e:
                logger.error(e)
                raise

        def _proteindoms(self, iprfile, proteinid):
            '''
            Builds a dictionary from the InterproScan file provided as input of the
            class "gene".

            :param iprfile: path to the InterproScan's output file
            :type iprfile: str
            :param proteinid: protein identifier (ID) from the InterproScan output
            :type proteinid: str
            '''
            logger.info('starting...')
            try:
                mrna = self.id
                f = open(iprfile, 'r')
                doms = {}
                for i in f:
                    if i.split('\t')[0] == proteinid:
                        doms.setdefault(i.split('\t')[3], []).append((i.split('\t')[4], 
                                                                      i.split('\t')[5], 
                                                                      int(i.split('\t')[6]), 
                                                                      int(i.split('\t')[7])))
                f.close()
                #
                print(len(doms), 'domain types found')
                print(', '.join(doms.keys()))
                self.doms = doms
                return doms
            except Exception as e:
                logger.error(e)
                raise


        def _getsnppos(self, sp, vcffiles, onlycoding=True):
            '''
            Selects SNP data overlapping with genome coordinates
            of the gene ID (class object) from a VCF file whose sample ID matches
            the "sp" parameter of the function. SNP annotation by
            SNPEff is retrieved from the VCF file. If absent, de novo annotation
            of selected SNPs is performed.

            :param sp: Species ID to select SNP data from the VCF file
            :type sp: str
            :param vcffiles: path to the VCF files directory
            :type vcffiles: str
            :param onlycoding: to plot only SNPs located on coding areas of the gene
            :type onlycoding: boolean
            '''
            logger.info('starting...')
            try:
                mrna = self.id
                db = self.db
                phvcfs = vcffiles
                galllog = open(logfile, 'a')
                fsp = 'file not found'
                for ffile in os.listdir(phvcfs):
                    if ffile.endswith('.vcf'):
                        logger.debug(ffile)
                        p0 = subprocess.run(['vcf-query -l '+os.path.join(phvcfs, ffile)], shell=True, 
                                            stdout=subprocess.PIPE, stderr=galllog)
                        sample = p0.stdout.decode().strip()
                        if sp == sample:
                            print('getting SNPs from...', self.id, sample, ffile)
                            fsp = ffile

                dcds, varssall, dmrna, dvarss = {}, [], {'snps':{}, 'posgposp':{}}, {}
                lencdsaccum = 0

                # SNPs on coding areas
                if onlycoding == True:
                    print('plotting only SNPs on coding areas...')
                    for cds in db.children(db[mrna], featuretype='CDS', order_by='start'):
                        lencds = cds.end + 1 - cds.start
                        p1 = subprocess.run(['vcftools --vcf ' + os.path.join(phvcfs, fsp) +\
                                             ' --chr '+db[mrna].chrom+' --from-bp '+\
                                                str(cds.start)+' --to-bp '+str(cds.end)+\
                                             ' --recode --recode-INFO-all --stdout'], 
                                            shell=True, 
                                            stdout=subprocess.PIPE, stderr=galllog)

                        for var in p1.stdout.decode().split('\n')[:-1]:
                            if var[0] != '#':
                                if len(var.split('\t')[3]) == 1 and len(var.split('\t')[4]) == 1:
                                    varssall.append(var)
                                    if var.split('\t')[9].split(':')[0] == '0/1':
                                        dcds[int(var.split('\t')[1])-cds.start+1+lencdsaccum] = \
                                        var.split('\t')[3] + '/' + var.split('\t')[4]
                                        dvarss[var.split('\t')[0]+':'+var.split('\t')[1]] = \
                                        var.split('\t')[3] + var.split('\t')[4]
                                        dmrna['posgposp'][var.split('\t')[0]+':'+var.split('\t')[1]] = \
                                        int(var.split('\t')[1])-cds.start+1+lencdsaccum
                                    if var.split('\t')[9].split(':')[0] == '1/1':
                                        dcds[int(var.split('\t')[1])-cds.start+1+lencdsaccum] = \
                                        var.split('\t')[4]
                                        dmrna['posgposp'][var.split('\t')[0]+':'+var.split('\t')[1]] = \
                                        int(var.split('\t')[1])-cds.start+1+lencdsaccum
                                        dvarss[var.split('\t')[0]+':'+var.split('\t')[1]] = \
                                        var.split('\t')[4] + var.split('\t')[4]
                        lencdsaccum += lencds

                # all SNPs
                else:
                    p2 = subprocess.run(['vcftools --vcf ' + os.path.join(phvcfs, fsp) +\
                                        ' --chr '+db[mrna].chrom+' --from-bp '+\
                                        str(self.start)+' --to-bp '+str(self.end) +\
                                        ' --recode --recode-INFO-all --stdout'], 
                                        shell=True, 
                                        stdout=subprocess.PIPE, stderr=galllog)

                    for var in p2.stdout.decode().split('\n')[:-1]:
                        if var[0] != '#':
                            if len(var.split('\t')[3]) == 1 and len(var.split('\t')[4]) == 1:
                                varssall.append(var)
                                if var.split('\t')[9].split(':')[0] == '0/1':
                                    dvarss[var.split('\t')[0]+':'+var.split('\t')[1]] = \
                                    var.split('\t')[3] + var.split('\t')[4]
                                if var.split('\t')[9].split(':')[0] == '1/1':
                                    dvarss[var.split('\t')[0]+':'+var.split('\t')[1]] = \
                                    var.split('\t')[4] + var.split('\t')[4]

                varssall = list(set(varssall))

                #
                # SNPEff annotation
                dsnpsann = {}
                headerann = 'Allele | Annotation | Annotation_Impact | Gene_Name | Gene_ID | \
                Feature_Type | Feature_ID | Transcript_BioType | Rank | HGVS.c | HGVS.p | \
                cDNA.pos / cDNA.length | CDS.pos / CDS.length | AA.pos / AA.length | Distance |\
                ERRORS / WARNINGS / INFO'
                def getann(item):
                    dsnpsann = {}
                    for i in item:
                        if '#' not in i:
                            for item in i.split('\t')[7].split(';'):
                                if item.startswith('ANN'):
                                    ann = item[4:]
                                    dtmpann = {}
                                    for field in range(len(headerann.split('|'))):
                                        dtmpann[headerann.split('|')[field].strip()] = \
                                        ann.split('|')[field]
                                    dsnpsann[':'.join(i.split('\t')[:2])] = dtmpann
                    return dsnpsann
                dsnpsann = getann(varssall)
                #
                if len(dsnpsann) == 0:
                    pass
                #
                dmrna['len'] = lencdsaccum
                if db[mrna].strand == '-':
                    dtmp = {}
                    for item in dcds:
                        dtmp[dmrna['len']-item+1] = dcds[item]
                #
                    dcds = dtmp

                    dtmp = {}
                    for item in dmrna['posgposp']:
                        dtmp[item] = dmrna['len']-dmrna['posgposp'][item]+1
                #
                    dmrna['posgposp'] = dtmp
                    del(dtmp)
                galllog.close()
                self.dcds = dcds
                self.varssall = varssall
                self.dmrna = dmrna
                self.dsnpsann = dsnpsann
                self.dvarss = dvarss
                return dsnpsann, dvarss
            except (TypeError):
                pass
            except Exception as e:
                logger.error(e)
                raise


        def plot(self, domtype='Pfam', sp=None, onlycoding=True):
            '''
            Plots features of the gene ID (class object) previously generated
            by the functions of the class, including exon and UTR features
            (the latter only if present in the GFF3 file), Interpro protein
            domains and SNPs. SNP data are labelled with the genotype according
            to the VCF file information, and colored based on SNPEff impact,
            i.e. LOW: green, MODERATE: amber, MODIFIER: pink, HIGH: red.
            A PNG image is generated.

            :param domtype: protein domain type (as specified in the InterproScan output)
                            to be plotted (Pfam by default).
            :type domtype: str
            :param sp: Species ID to select SNP data from the VCF file.
            :type sp: str
            :param onlycoding: to plot only SNPs located on coding areas of the gene
            :type onlycoding: boolean
            '''
            logger.info('starting...')
            try:
                mrna = self.id
                dcoors = self._transcriptpos_to_genomepos()
                doms = self._proteindoms(self.iprfile, self.proteinid) if \
                (self.iprfile is not None and self.proteinid is not None) else {}
                dsnpsann, dvarss = self._getsnppos(sp, self.vcffiles, onlycoding) if \
                self.vcffiles is not None else ({}, {})

                db = self.db
                domsgncoors = []

                ccolor = '#c5cc78'
                gdd = GenomeDiagram.Diagram('gene')
                sscale = 1
                if self.end-self.start > 40000:
                    sscale = 0
                gdt_features = gdd.new_track(0, greytrack=True, name=mrna, greytrack_labels=1, 
                                             greytrack_font_color='black', 
                                             greytrack_fontsize=20, greytrack_font_rotation=90,
                                             scale=sscale, scale_largetick_interval=5000, 
                                             scale_smalltick_interval=500,
                                             scale_fontsize=10, scale_fontangle=0)
                #
                gds_features = gdt_features.new_set()
                #
                for ft in db.children(mrna):
                    if 'UTR' in ft.featuretype:
                        ccolor = '#a6a6a6'
                    feature = SeqFeature(FeatureLocation(ft.start, ft.end), strand=int(ft.strand+'1'))
                    null = gds_features.add_feature(feature, name=ft.id, label=False, color=ccolor, 
                                                    sigil='BIGARROW', label_size=0, 
                                                    arrowshaft_height=1.0, arrowhead_length=0.1)
                #
                #protein domain independent
                gdt_features = gdd.new_track(1, greytrack=True, name='Dom', greytrack_labels=1, 
                                             greytrack_font_color='black', greytrack_fontsize=30, 
                                             height=0.3, scale=0, scale_largetick_interval=1000, 
                                             scale_smalltick_interval=100)
                #
                gds_features = gdt_features.new_set()
                #
                cmap = pl.cm.get_cmap('tab20')
                # sort doms by size and define ldoms
                ldoms = []
                for dom in doms.get(domtype, []):
                    ldoms.append((dom[3]-dom[2],) + dom)
                ldoms = [dom[1:] for dom in sorted(ldoms, reverse=True)]
                # use ldoms from now on
                for indx,dom in enumerate(ldoms):
                    pdcoors = sorted((dcoors[dom[2]*3-2], dcoors[dom[3]*3]))
                    domsgncoors.append((dom[0], dom[1], pdcoors[0], pdcoors[1]))
                    domcolor = Color(cmap(indx)[0], cmap(indx)[1], cmap(indx)[2], cmap(indx)[3])
                    #feature for domain name
                    feature = SeqFeature(FeatureLocation(pdcoors[0], pdcoors[1]), strand=0)
                    null = gds_features.add_feature(feature, name=dom[0], label=True, color='white', 
                                                    sigil='BOX', label_size=30, border=False, 
                                                    label_angle=25, label_position='start', 
                                                    label_color=domcolor)
                    #
                    for pos in range(pdcoors[0], pdcoors[1]):
                        if pos in dcoors.values():
                            feature = SeqFeature(FeatureLocation(pos, pos+1), strand=0)
                            null = gds_features.add_feature(feature, name='', label=False, 
                                                            color=domcolor, sigil='BOX',
                                                            label_size=0)
                        if pos not in dcoors.values():
                            feature = SeqFeature(FeatureLocation(pos, pos+1), strand=0)
                            null = gds_features.add_feature(feature, name='.', label=True, 
                                                            color='white', border=False, sigil='BOX',
                                                            label_size=10, label_strand=-1, 
                                                            label_color=domcolor)
                #
                #SNP positions
                snpimpact = genome._snpimpact
                gdt_features = gdd.new_track(2, greytrack=True, name='SNPs', greytrack_labels=1, 
                                             greytrack_font_color='black',
                                            greytrack_fontsize=30, height=0.3,
                                            scale=0, scale_largetick_interval=1000, 
                                             scale_smalltick_interval=100)
                #
                gds_features = gdt_features.new_set()
                #
                for snp in dvarss:
                    snpcolor = snpimpact[dsnpsann.get(snp, 
                                        {'Annotation_Impact': 'NOANN'})
                                         ['Annotation_Impact']]
                    feature = SeqFeature(FeatureLocation(int(snp.split(':')[1])-1, 
                                                         int(snp.split(':')[1])+1), strand=0)
                    null = gds_features.add_feature(feature, name=dvarss[snp], label=True, 
                                                    color=snpcolor, sigil='OCTO', label_size=20, 
                                                    label_angle=90, label_position='middle', 
                                                    label_color=snpcolor)
                #
                gdd.draw(format='linear', pagesize=(100*cm,20*cm), fragments=1,
                         start=db[mrna].start-100, end=db[mrna].end)
                #
                gdd.write('geneplot.' + str(self.id).replace(':', '_') + '.png', "png")
                #
                self.domsgncoors = domsgncoors
            except Exception as e:
                logger.error(e)
                raise



                
