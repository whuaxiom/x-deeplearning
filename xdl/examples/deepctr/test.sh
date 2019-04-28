#!/bin/sh

program=$1
zk="zfs://localhost:2181/mm"

nohup python ${program} --task_name=scheduler --zk_addr=${zk} --ps_num=2 --ps_cpu_cores=10 --ps_memory_m=4000 --ckpt_dir=./checkpoint > scheduler.log 2>&1 &
nohup python ${program} --task_name=ps --task_index=0 --zk_addr=${zk} --ckpt_dir=./checkpoint > ps0.log 2>&1 &
nohup python ${program} --task_name=ps --task_index=1 --zk_addr=${zk} --ckpt_dir=./checkpoint > ps1.log 2>&1 &
nohup python ${program} --task_name=worker --task_index=0 --task_num=2 --zk_addr=${zk} --ckpt_dir=./checkpoint > worker0.log 2>&1 &
nohup python ${program} --task_name=worker --task_index=1 --task_num=2 --zk_addr=${zk} --ckpt_dir=./checkpoint > worker1.log 2>&1 &

