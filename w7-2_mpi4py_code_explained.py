from mpi4py import MPI
import pandas as pd
import glob
import time

pesticides = pd.read_csv("PubChem_Agrochemical.csv")
zinc_files = sorted(glob.glob("./zinc_db/A*.txt"))
#linear search
pesticides_smi = pesticides['smiles'].to_list()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
DONE = -1
pesticides_hash = set(pesticides_smi)

if rank == 0:
    start_time = time.time()
    print(f"[마스터] 총 파일 {len(zinc_files)}개, 워커 {size-1}명으로 시작")
    print("=" * 60)

    task_queue = list(range(len(zinc_files)))
    finished = 0
    total_count = 0

    while finished < size - 1:
        status = MPI.Status()
        count = comm.recv(source=MPI.ANY_SOURCE, tag=0, status=status)
        worker = status.Get_source()

        if count:
            total_count += count
            print(f"[마스터] 워커 {worker} → 결과 수신: {count}개 일치 (누적: {total_count})")

        if task_queue:
            file_idx = task_queue.pop(0)
            comm.send(file_idx, dest=worker, tag=1)
            print(f"[마스터] 워커 {worker} ← 작업 배정: {zinc_files[file_idx]}")
        else:
            comm.send(DONE, dest=worker, tag=1)
            finished += 1
            print(f"[마스터] 워커 {worker} ← 종료 신호 전송 ({finished}/{size-1} 완료)")

    print("=" * 60)
    print(f"[마스터] 농약 일치 개수: {total_count}")
    print(f"[마스터] 계산 시간: {time.time() - start_time:.2f}초")

else:
    comm.send(0, dest=0, tag=0)

    while True:
        file_idx = comm.recv(source=0, tag=1)
        if file_idx == DONE:
            print(f"  [워커 {rank}] 종료 신호 수신, 퇴근!")
            break

        fname = zinc_files[file_idx]
        print(f"  [워커 {rank}] {fname} 처리 시작...")
        df = pd.read_csv(fname, sep='\t', usecols=['smiles'])
        count = sum(1 for s in df['smiles'] if s in pesticides_hash)
        print(f"  [워커 {rank}] {fname} 완료 → {count}개 일치")

        comm.send(count, dest=0, tag=0)