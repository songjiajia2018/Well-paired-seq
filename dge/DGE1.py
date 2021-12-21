#!/usr/bin/env python
#coding=utf-8

import os
import argparse

parser = argparse.ArgumentParser(description='Extracting Digital Gene Expression (step1,cell selection finished) (fastq_remove_id_duplication.py, cell_selection.R are needed): \
                                              python DGE1.py \
                                              -p /path/to/picard.jar \
                                              -F1 fastq_file \
                                              -F2 fastq_file \
                                              -SM sample_name \
                                              -SR /path/to/STAR_REFERENCE \
                                              -RF /path/to/REFERENCE_FASTQ \
                                              -RG /path/to/REFERENCE_GTF')

parser.add_argument('-p', '--picard', type=str, default='/home/songjia/software/Drop-seq_tools-2.3.0/3rdParty/picard/picard.jar', help='/path/to/picard.jar')
parser.add_argument('-F1', '--FASTQ1', type=str, required=True, help='Input fastq file (optionally gzipped) for single end data, or first read in paired end')
parser.add_argument('-F2', '--FASTQ2', type=str, help='Input fastq file (optionally gzipped) for the second read of paired end data. Default value: null.')
parser.add_argument('-SM', '--SAMPLE_NAME', type=str, required=True, help='Sample name to insert into the read group header  Required.')
parser.add_argument('-SR', '--STAR_REFERENCE', type=str, default='/home/songjia/newdisk/YK/reference/hg19_mm10/STAR', help='/path/to/STAR_REFERENCE')
parser.add_argument('-RF', '--REFERENCE_FASTQ', type=str, default='/home/songjia/newdisk/YK/reference/hg19_mm10/hg19_mm10_transgenes.fasta', help='/path/to/REFERENCE_FASTQ')
parser.add_argument('-RG', '--REFERENCE_GTF', type=str, default='/home/songjia/newdisk/YK/reference/hg19_mm10/hg19_mm10_transgenes_species_gene_name.gtf', help='/path/to/REFERENCE_GTF')

args = parser.parse_args()

##FastqToSam
def FastqToSamTag():
    if args.FASTQ2:
        if args.FASTQ1.split('.')[-1] == 'gz':
            os.system("gunzip %s" %(args.FASTQ1))
            F1_raw=args.FASTQ1.replace('.gz','')
        else:
            F1_raw=args.FASTQ1
        if args.FASTQ2.split('.')[-1] == 'gz':
            os.system("gunzip %s" %(args.FASTQ2))
            F2_raw=args.FASTQ2.replace('.gz','')
        else:
            F2_raw=args.FASTQ2
        os.system("python fastq_remove_id_duplication.py -F1 %s -F2 %s" %(F1_raw, F2_raw))
        F1=F1_raw.split('/')[-1].split('.')[0]+'_remove_id_duplication.'+F1_raw.split('/')[-1].split('.')[-1]
        F2=F2_raw.split('/')[-1].split('.')[0]+'_remove_id_duplication.'+F2_raw.split('/')[-1].split('.')[-1]
        os.system("java -jar %s FastqToSam \
                   F1=%s \
                   F2=%s \
                   O=unaligned_read_pairs.bam \
                   SM=%s " %(args.picard, F1, F2, args.SAMPLE_NAME))

        ##TagBamWithReadSequenceExtended
        ##Cell Barcode
        os.system("TagBamWithReadSequenceExtended \
                   INPUT=unaligned_read_pairs.bam \
                   OUTPUT=unaligned_tagged_Cell.bam \
                   SUMMARY=unaligned_tagged_Cellular.bam_summary.txt \
                   BASE_RANGE=1-12 \
                   BASE_QUALITY=10 \
                   BARCODED_READ=1 \
                   DISCARD_READ=False \
                   TAG_NAME=XC \
                   NUM_BASES_BELOW_QUALITY=1")

    else:
        if args.FASTQ1.split('.')[-1] == 'gz':
            os.system("gunzip %s" %(args.FASTQ1))
            F1_raw=args.FASTQ1.replace('.gz','')
        else:
            F1_raw=args.FASTQ1
        os.system("python fastq_remove_id_duplication.py -F1 %s" %(F1_raw))
        F1=F1_raw.split('/')[-1].split('.')[0]+'_remove_id_duplication.'+F1_raw.split('/')[-1].split('.')[-1]
        os.system("java -jar %s FastqToSam \
                   F1=%s \
                   O=unaligned_read.bam \
                   SM=%s " %(args.picard, F1, args.SAMPLE_NAME))

        ##TagBamWithReadSequenceExtended
        ##Cell Barcode
        os.system("TagBamWithReadSequenceExtended \
                   INPUT=unaligned_read.bam \
                   OUTPUT=unaligned_tagged_Cell.bam \
                   SUMMARY=unaligned_tagged_Cellular.bam_summary.txt \
                   BASE_RANGE=1-12 \
                   BASE_QUALITY=10 \
                   BARCODED_READ=1 \
                   DISCARD_READ=False \
                   TAG_NAME=XC \
                   NUM_BASES_BELOW_QUALITY=1")

##Molecular Barcode
def TagMolecularBarcode():
    os.system("TagBamWithReadSequenceExtended \
               INPUT=unaligned_tagged_Cell.bam \
               OUTPUT=unaligned_tagged_CellMolecular.bam \
               SUMMARY=unaligned_tagged_Molecular.bam_summary.txt \
               BASE_RANGE=13-20 \
               BASE_QUALITY=10 \
               BARCODED_READ=1 \
               DISCARD_READ=True \
               TAG_NAME=XM \
               NUM_BASES_BELOW_QUALITY=1")

##FilterBam
def FilterBam():
    os.system("FilterBam \
               TAG_REJECT=XQ \
               INPUT=unaligned_tagged_CellMolecular.bam \
               OUTPUT=unaligned_tagged_filtered.bam ")

##TrimStartingSequence
def TrimStartingSequence():
    os.system("TrimStartingSequence \
               INPUT=unaligned_tagged_filtered.bam \
               OUTPUT=unaligned_tagged_trimmed_smart.bam \
               OUTPUT_SUMMARY=adapter_trimming_report.txt \
               SEQUENCE=AAGCAGTGGTATCAACGCAGAGTGAATGGG \
               MISMATCHES=0 \
               NUM_BASES=5")

##PolyATrimmer
def PolyATrimmer():
    os.system("PolyATrimmer \
               INPUT=unaligned_tagged_trimmed_smart.bam \
               OUTPUT=unaligned_mc_tagged_polyA_filtered.bam \
               OUTPUT_SUMMARY=polyA_trimming_report.txt \
               MISMATCHES=0 \
               NUM_BASES=6 \
               USE_NEW_TRIMMER=true")

##SamToFastq
def SamToFastq():
    os.system("java -Xmx4g -jar %s SamToFastq \
               INPUT=unaligned_mc_tagged_polyA_filtered.bam \
               FASTQ=unaligned_mc_tagged_polyA_filtered.fastq" %(args.picard))

##Alignment
##STAR
def STAR():
    os.system("STAR \
               --genomeDir %s \
               --readFilesIn unaligned_mc_tagged_polyA_filtered.fastq \
               --outFileNamePrefix star" %(args.STAR_REFERENCE))
##SortSam
def SortSam():
    os.system("java -Xmx4g -jar %s SortSam \
               I=starAligned.out.sam \
               O=aligned.sorted.bam \
               SO=queryname" %(args.picard))
##MergeBamAlignment
def MergeBamAlignment():
    os.system("java -Xmx4g -jar %s MergeBamAlignment \
               REFERENCE_SEQUENCE=%s \
               UNMAPPED_BAM=unaligned_mc_tagged_polyA_filtered.bam \
               ALIGNED_BAM=aligned.sorted.bam \
               OUTPUT=merged.bam \
               INCLUDE_SECONDARY_ALIGNMENTS=false \
               PAIRED_RUN=false" %(args.picard, args.REFERENCE_FASTQ))
##TagReadWithGeneExonFunction
def TagReadWithGeneExonFunction():
    os.system("TagReadWithGeneExonFunction \
               I=merged.bam \
               O=star_gene_exon_tagged_m.bam \
               ANNOTATIONS_FILE=%s \
               TAG=GE" %(args.REFERENCE_GTF))
##TagReadWithGeneFunction
def TagReadWithGeneFunction():
    os.system("TagReadWithGeneFunction \
               I=star_gene_exon_tagged_m.bam \
               O=star_gene_exon_tagged.bam \
               ANNOTATIONS_FILE=%s" %(args.REFERENCE_GTF))
##DetectBeadSubstitutionErrors
def DetectBeadSubstitutionErrors():
    os.system("DetectBeadSubstitutionErrors \
               I=star_gene_exon_tagged.bam \
               O=my_clean_subtitution.bam \
               OUTPUT_REPORT=my_clean.substitution_report.txt \
               TMP_DIR=tmp")
##DetectBeadSynthesisErrors
def DetectBeadSynthesisErrors():
    os.system("DetectBeadSynthesisErrors \
               I=my_clean_subtitution.bam \
               O=my_clean.bam \
               REPORT=my_clean.indel_report.txt \
               OUTPUT_STATS=my.synthesis_stats.txt \
               SUMMARY=my.synthesis_stats.summary.txt \
               PRIMER_SEQUENCE=AAGCAGTGGTATCAACGCAGAGTAC \
               TMP_DIR=tmp")

##Cell Selection
def CellSelection():
    os.system("BamTagHistogram \
               I=my_clean.bam \
               O=out_cell_readcounts.txt.gz \
               TAG=XC")
    os.system("Rscript cell_selection.R")


FastqToSamTag()
TagMolecularBarcode()
FilterBam()
TrimStartingSequence()
PolyATrimmer()
SamToFastq()
STAR()
SortSam()
MergeBamAlignment()
TagReadWithGeneExonFunction()
TagReadWithGeneFunction()
DetectBeadSubstitutionErrors()
DetectBeadSynthesisErrors()
CellSelection()

