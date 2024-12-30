#!/bin/bash
#SBATCH --job-name=mpi_p2p_bloqueante
#SBATCH --partition=hype
#SBATCH --nodes=2
#SBATCH --ntasks=40
#SBATCH --time=1:30:00
#SBATCH --output=%x_%j.out
#SBATCH --error=erros/%x_%j.err


MACHINEFILE="nodes.$SLURM_JOB_ID"
srun -l hostname | sort -n | awk '{print $2}' > $MACHINEFILE


perf stat -e task-clock,cycles,instructions \
mpirun -np $SLURM_NTASKS \
       -machinefile $MACHINEFILE \
       --mca btl ^openib \
       --mca btl_tcp_if_include eno2 \
       --bind-to none -np $SLURM_NTASKS \
       ./mpi_p2p_bloqueante 2048  &>> bloquante_2048_40_2.out
sacct -j $SLURM_JOB_ID --format=JobID,JobName,CPUTime,MaxRSS,AveRSS,Elapsed
