from io import StringIO
from Bio import SeqIO
from Bio import AlignIO
import pandas as pd
import os

def qcCvab(best_hitsPep, best_hitsAln):
	if os.stat(best_hitsAln).st_size==0:
		gappyDict = {"id":[], "nonGap":[], "percentGap":[], "alignment":[]}
		gappyDF = pd.DataFrame.from_dict(gappyDict)
		lenDict = {"id":[], "len":[]}
		lenDF = pd.DataFrame.from_dict(lenDict)
		lenGapDF = gappyDF.merge(lenDF)
		lenGapDF["percentTrim"] = (lenGapDF["len"]-lenGapDF["nonGap"])/ lenGapDF["len"]
		return lenGapDF
	else:
		alignment = AlignIO.read(open(best_hitsAln), "fasta")
		gappyDict = {"id":[], "nonGap":[], "percentGap":[], "alignment":[]}
		for record in alignment:
			percentGap = record.seq.count("-")/len(record.seq)
			gappyDict["id"].append(record.id)
			gappyDict["nonGap"].append( len(record.seq) - record.seq.count("-"))
			gappyDict["percentGap"].append(percentGap)
			gappyDict["alignment"].append(str(record.seq))
		gappyDF = pd.DataFrame.from_dict(gappyDict)
		# catalytic triad
		gappyDF["C34"] = gappyDF["alignment"].astype(str).str[34]
		gappyDF["H107"] = gappyDF["alignment"].astype(str).str[107]
		gappyDF["D123"] = gappyDF["alignment"].astype(str).str[123]
		lenDict = {"id":[], "len":[]}
		for record in SeqIO.parse(best_hitsPep, "fasta"):
			lenDict["id"].append(record.id)
			lenDict["len"].append(len(record.seq))
		lenDF = pd.DataFrame.from_dict(lenDict)
		lenGapDF = gappyDF.merge(lenDF)
		lenGapDF["percentTrim"] = (lenGapDF["len"]-lenGapDF["nonGap"])/ lenGapDF["len"]
		return lenGapDF

rule makeblastdb_CvaB:
	input:
		config["outdir"] + "/00_dbs/CvaB.verified.pep"
	output:
		config["outdir"] + "/00_dbs/CvaB.verified.pep.dmnd"
	threads:threads_max
	shell:
		"diamond makedb --in {input} -d {input} -p {threads}"

rule blast_CvaB:
	input:
		verified_component = config["outdir"] + "/00_dbs/CvaB.verified.pep.dmnd",
		input_seqs = config["outdir"] + "/01_orf_homology/CvaB/filtered_nr.fa"
	output:
		config["outdir"] + "/01_orf_homology/CvaB/blast.txt"
	threads:threads_max
	shell:
		"diamond blastp -d {input.verified_component} -q {input.input_seqs}   --evalue 0.001 -k 1 -o {output} -p {threads}"

rule msa_CvaB:
	input:
		config["outdir"] + "/00_dbs/CvaB.verified.pep"
	output:
		config["outdir"] + "/00_dbs/CvaB.verified.aln"
	threads:threads_max
	shell:
		"mafft --thread {threads} --auto {input} > {output}"

rule buildhmm_CvaB:
	input:
		config["outdir"] + "/00_dbs/CvaB.verified.aln"
	output:
		config["outdir"] + "/00_dbs/CvaB.verified.hmm"
	threads:threads_max
	shell:
		"hmmbuild --cpu {threads} {output} {input}"

rule blast_v_hmmer_CvaB:
	input:
		verifiedHMM = config["outdir"] + "/00_dbs/CvaB.verified.hmm",
		input_seqs = config["outdir"] + "/01_orf_homology/CvaB/filtered_nr.fa",
		blastOut = config["outdir"] + "/01_orf_homology/CvaB/blast.txt"
	output:
		config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.csv"
	run:
		blastDF = load_blast(input.blastOut)
		hmmer_hits, hmm_name = run_hmmsearch(input.input_seqs, input.verifiedHMM)
		hmmer_hitsHeaders = [hit.name.decode() for hit in hmmer_hits]
		blastDF["component"] = hmm_name
		blastDF["hmmerHit"] = blastDF["qseqid"].isin(hmmer_hitsHeaders)
		blastDF.to_csv(output[0], index = False)

rule best_Cvab_headers:
	input:
		config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.csv"
	output:
		config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.headers"
	shell:
		"cut -d, -f1 {input} > {output}"

rule best_Cvab_fasta:
	input:
		headers=config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.headers",
		input_seqs = config["outdir"] + "/01_orf_homology/CvaB/filtered_nr.fa"
	output:
		config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.fa"
	threads:threads_max
	shell:
		"seqkit -j {threads} grep -f {input.headers} {input.input_seqs} > {output}"

rule align_with_verifiedCvab:
	input:
		best_CvaB=config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.fa",
		verified_CvaB=config["outdir"] + "/00_dbs/CvaB.verified.aln"
	output:
		config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.with_verified.aln"
	threads:threads_max
	shell:
		"""
		if [ -s {input.best_CvaB} ]; then
			mafft --thread {threads} --inputorder --keeplength --add {input.best_CvaB} --auto {input.verified_CvaB} > {output}
		else
			touch {output}
		fi
		"""

rule filter_CvaB_hits:
	input:
		best_CvaB=config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.fa",
		align_with_verifiedCvab=config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.with_verified.aln",
		nr_filtered_csv=config["outdir"] + "/01_orf_homology/prodigal_out.all.nr_expanded.csv"
	output:
		preQC=config["outdir"] + "/01_orf_homology/CvaB/preQC.csv",
		QC=config["outdir"] + "/01_orf_homology/CvaB/QC.csv"
	threads:threads_max
	run:
		preQC_Cvab = qcCvab(input.best_CvaB, input.align_with_verifiedCvab)
		nr_filteredDF = pd.read_csv(input.nr_filtered_csv)
		nr_filteredDF.merge(preQC_Cvab, left_on="pephash", right_on="id").to_csv(output.preQC)

		lowGapCvaB = preQC_Cvab[preQC_Cvab["percentGap"] <0.1]
		lowTrimCvaB = lowGapCvaB[lowGapCvaB["percentTrim"] <0.1]
		catalyticTriadCvab = lowTrimCvaB[(lowTrimCvaB["C34"] + lowTrimCvaB["H107"] + lowTrimCvaB["D123"]) == "CHD"]
		catalyticTriadCvab.to_csv(output.QC)
