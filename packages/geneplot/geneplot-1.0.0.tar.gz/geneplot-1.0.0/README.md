## geneplot library

A Python library for plotting single nucleotide polymorhpysm (SNP) data and 
protein domain information on the exon-intron structure of a gene. it takes as 
input standard files and formats generated from  popular tools, including 
InterproScan, the General Feature Format v3 (GFF3) and the Variant Call 
Format (VCF). For more details see:



## Code availability

https://github.com/gonzalezibeas/geneplot

## Installation
```
pip install geneplot
´´´
## Documentation

https://geneplot.readthedocs.io/en/latest/#

## Get started
Plot geneID (from the GFF3 file) and proteinID domains (from IPR file)
and SNPs listed on sample_ID from the VCF files directory.

```Python
import geneplot as gp

#input data
filegff = '/path-to-data/file.gff3'
iprfile = '/path-to-data/file.ipr'
vcffiles = '/path-to-data/'

# class instantiation (genome object)
genome_1 = gp.genome(filegff, iprfile=iprfile, vcffiles=vcffiles)

# class instantiation (gene object)
gene_1 = genome_1.gene(mRNAid='transcriptID', proteinid='proteinID')

# plot
gene_1.plot('Pfam', sp='sampleID', onlycoding=True)


