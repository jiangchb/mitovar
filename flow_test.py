#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/12 14:50
# @Author  : Runsheng     
# @File    : flow_test.py

from flow import flow_bait
from assembler import spades_wrapper
import os
from flow import flow_pre_fastq
from flow import flow_chain_sra_scaf
from bait import *
from collections import OrderedDict
from anno import flow_exon


def test1():
    # just test the reads from previous combines, treat them as single
    # and do one round of spades assembler
    work_dir_root="/home/zhaolab1/data/mitosra/dna/wkdir"
    #dir_list=['281687', '1561998', '1729975', '1094327', '1094328', '31234',
    #         '1094335', '497829', '1094320', '1094321', '1094326', '135651', '860376']
    dir_list=['860376']
    ref_file = "/home/zhaolab1/data/mitosra/dna/ref/celcbr.fa"
    for spe in dir_list:
        work_dir_spe_root=os.path.join(work_dir_root, spe)
        os.chdir(work_dir_spe_root)
        fq_dict={"all":["/home/zhaolab1/data/mitosra/dna/wkdir/{}/all.fastq".format(spe)]}
        fq_out_dict=flow_bait(0, work_dir=work_dir_spe_root, fq_dict=fq_dict, ref_file=ref_file)

        work_dir_round="/home/zhaolab1/data/mitosra/dna/wkdir/{}/round0".format(spe)
        os.chdir(work_dir_round)
        spades_wrapper(fq_name_dict=fq_out_dict, core=32, outdir="spades_out_onlyas")


def test_pre_fastq():
    """
    using 31243, remani genome to get the fastq
    :return:
    """
    sralist=['SRR1056292', 'SRR1056294', 'SRR1056295', 'SRR1056293', 'SRR275642']
    work_dir_root="/home/zhaolab1/data/mitosra/dna/wkdir/31234"

    flow_pre_fastq(sralist, work_dir_root)


def test_as_one():
    spe="31234"
    work_dir_spe_root="/home/zhaolab1/data/mitosra/dna/wkdir/31234"
    ref_file = "/home/zhaolab1/data/mitosra/dna/ref/celcbr.fa"

    #fq_dict = get_fq_dict("/home/zhaolab1/data/mitosra/dna/wkdir/31234/fastq")
    #print(fq_dict)

    #fq_out_dict=flow_bait(0, work_dir=work_dir_spe_root, fq_dict=fq_dict, ref_file=ref_file)
    fq_out_dict=get_fq_dict("/home/zhaolab1/data/mitosra/dna/wkdir/31234/round0")
    print(fq_out_dict)
    work_dir_round="/home/zhaolab1/data/mitosra/dna/wkdir/{}/round0".format(spe)
    os.chdir(work_dir_round)
    spades_wrapper(fq_name_dict=fq_out_dict, core=32, outdir="spades_out_onlyas")


def test_half():
    dict_half=OrderedDict([
                 ('1729975', ['ERR1055244.sra']),
                 ('1094331',
                  ['ERR1059219.sra',
                   'ERR1059222.sra',
                   'ERR1059220.sra',
                   'ERR1059221.sra']),
                 ('281681',
                  ['ERR1059191.sra', 'ERR1059192.sra', 'ERR1059193.sra'])])
    sra_dir = "/home/zhaolab1/data/mitosra/sra/mitodna"
    work_dir_root="/home/zhaolab1/data/mitosra/dna/wkdir"
    ref_file = "/home/zhaolab1/data/mitosra/dna/ref/celcbr.fa"

    for spe, sra_list in dict_half.iteritems():
        print(flow_chain_sra_scaf(spe, sra_list, ref_file, work_dir_root, sra_dir, core=16))

def test_round1():
    pass


def flow_round0_all():
    from glob import glob
    import os
    wkdir="/home/zhaolab1/data/mitosra/dna/anno/exon"
    os.chdir(wkdir)
    target="./ref/celmt_p.fasta"
    query_list=glob("*.fasta")


    for query in query_list:
        print query
        flow_exon(query, target)


if __name__=="__main__":
    pass
    # note 86 should have another round to finish