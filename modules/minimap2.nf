process MINIMAP2 {

    tag {"${seq.baseName}"}

    publishDir "${params.outdir}/${params.prefix}/${task.process.replaceAll(":","_")}", pattern: "*.sorted.bam", mode: 'copy'

    cpus 8

    input:
        tuple(path(seq),path(ref))

    output:
        path("*.sorted.bam"), emit: bam
        path("*.bai"), emit: index

    script:
      """
      minimap2 -t ${task.cpus} -ax asm5 -a ${ref} ${seq} | \
      samtools sort -o ${seq.baseName}.sorted.bam
      samtools index -b -@ ${task.cpus} ${seq.baseName}.sorted.bam ${seq.baseName}.sorted.bam.bai
      """
}
