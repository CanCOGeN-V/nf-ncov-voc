#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

// import modules


include { DOWNLOAD_VIRALAI_MULTIFASTA                    } from '../../modules/local/viralai_multifasta'
include { DOWNLOAD_VIRALAI_METADATA                      } from '../../modules/local/viralai_metadata'
include { DOWNLOADPANGOALIAS                             } from '../../modules/local/downloadPangoalias'
include { PROCESS_VIRALAI_METADATA                       } from '../../modules/local/processViralai_metadata' 
include { XZ_DECOMPRESS                                  } from '../../modules/nf-core/xz/decompress/main'

workflow VIRALAI {
    

    main:
        
        DOWNLOAD_VIRALAI_METADATA()
        meta = DOWNLOAD_VIRALAI_METADATA.out.csv
       
        DOWNLOAD_VIRALAI_MULTIFASTA()
        seq=DOWNLOAD_VIRALAI_MULTIFASTA.out.xz
        
        seq
            .map { fasta ->
            tuple( [[id:"viralai_seq"], fasta] )
            }
            .set{sequences}
        
        XZ_DECOMPRESS(sequences)
        seq=XZ_DECOMPRESS.out.file
        

        DOWNLOADPANGOALIAS()
        alias=DOWNLOADPANGOALIAS.out.json

        meta
            .map { csv ->
            tuple( [[id:"viralai_meta"], csv] )
            }
            .set{metadata} 

        PROCESS_VIRALAI_METADATA(metadata, alias)
        meta = PROCESS_VIRALAI_METADATA.out.gz
        
    emit:
        meta
        seq
}
