# =============================================================
# 분자 DP 병렬화 — mpi4py 마스터-워커 패턴
#
# ▼ 실행 모드 두 가지 ▼
#
#   1) 로컬 PC 테스트 (KISTI 제출 전 동작 확인용)
#      - 아래 TEST_MODE = True 로 두고
#      - 터미널에서:  mpirun -np 4 python w10-1_molecule_dp_kisti.py
#      - 수 초 내 완료. 출력 형식과 마스터-워커 통신 동작을 먼저 검증.
#
#   2) KISTI 본 실행
#      - TEST_MODE = False 로 바꾸고
#      - 작업 스케줄러에 제출 (자세한 절차는 4주차 KISTI 강의 참고):
#         mpirun -np 32 python w10-1_molecule_dp_kisti.py
#
# 전략 (7주차 마스터-워커 패턴):
#   - 마스터(rank 0): 현재 frontier의 이웃 후보를 모아 워커들에게 분배
#   - 워커(rank 1+):  자기 몫의 분자 점수 계산 후 마스터에게 반환
#   - 마스터: 결과를 모아 최고 갱신, top-N(beam)을 다음 frontier로 선정
#   - K번 반복
# =============================================================

from mpi4py import MPI
from rdkit import Chem, RDLogger
from rdkit.Chem import QED, Crippen
import time

RDLogger.DisableLog('rdApp.*')


# ---- 점수 함수 (지난 시간과 동일) ----
def score(smi):
    """분자 점수: QED는 높이고 logP는 낮춘다"""
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return -1e9                          # 유효하지 않은 분자는 매우 낮은 점수
    logp = Crippen.MolLogP(mol)
    if logp > 5:
        logp = 5                             # logP 상한
    return QED.qed(mol) - 0.5 * logp


def neighbors(smi):
    """치환 + 원자 추가까지 — KISTI 스케일에서는 탐색 공간을 크게 잡는다"""
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return []
    result = []
    # 1) 원자 치환 (C/N/O)
    for i in range(mol.GetNumAtoms()):
        for atom_num in [6, 7, 8]:
            rw = Chem.RWMol(mol)
            rw.GetAtomWithIdx(i).SetAtomicNum(atom_num)
            try:
                Chem.SanitizeMol(rw)
                result.append(Chem.MolToSmiles(rw))
            except:
                pass
    # 2) 원자 추가 (각 원자에 C/N/O 하나씩 단일 결합)
    for i in range(mol.GetNumAtoms()):
        for atom_num in [6, 7, 8]:
            rw = Chem.RWMol(mol)
            new_idx = rw.AddAtom(Chem.Atom(atom_num))
            rw.AddBond(i, new_idx, Chem.BondType.SINGLE)
            try:
                Chem.SanitizeMol(rw)
                result.append(Chem.MolToSmiles(rw))
            except:
                pass
    return result


# ---- MPI 설정 ----
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ---- 하이퍼파라미터 ----
# ┌─────────────────────────────────────────────────────────┐
# │  ★ 로컬 테스트 vs KISTI 본 실행을 여기서 한 줄로 전환     │
# │     True  → PC 빠른 테스트  (mpirun -np 4 권장)          │
# │     False → KISTI 본 실행   (mpirun -np 32 권장)        │
# └─────────────────────────────────────────────────────────┘
TEST_MODE = True

START_SMI = 'CC(C)Cc1ccc(cc1)C(C)C(=O)O'    # 이부프로펜

if TEST_MODE:
    K = 2          # 가볍게: 깊이 2 (수 초 내 완료)
    BEAM = 10      # top-N도 작게
else:
    K = 4          # KISTI 스케일: 깊이 4 (~분 단위) 
    BEAM = 50      # top-50

DONE = None        # 종료 신호 (수정 X)


if rank == 0:
    # ============================================================
    # 마스터 프로세스
    # ============================================================
    print(f'[마스터] 워커 {size-1}명, 시작 분자: {START_SMI}')
    print(f'[마스터] K={K}, BEAM={BEAM}')
    print('=' * 60)

    t_start = time.time()

    frontier = [START_SMI]                   # 현재 깊이의 분자 집합
    visited = set(frontier)                  # 이미 방문한 분자 (재계산 방지 — DP의 캐싱 역할)
    best = (score(START_SMI), START_SMI)     # 지금까지의 최적

    for depth in range(K):
        # ------ 1) 모든 이웃 후보 모으기 ------
        candidates = []
        for smi in frontier:
            candidates.extend(neighbors(smi))
        # 중복 제거 + 이미 본 분자 제외 (← 여기서 DP의 "겹치는 부분 문제" 캐싱)
        candidates = [s for s in set(candidates) if s not in visited]
        visited.update(candidates)

        print(f'[마스터] 깊이 {depth+1}: 평가할 후보 {len(candidates)}개')

        if not candidates:
            print('[마스터] 더 평가할 분자가 없음. 조기 종료.')
            break

        # ------ 2) 워커 수만큼 균등 분배 ------
        n_workers = size - 1
        chunks = [candidates[i::n_workers] for i in range(n_workers)]
        for w in range(1, size):
            comm.send(chunks[w-1], dest=w, tag=1)

        # ------ 3) 각 워커의 결과 수신 ------
        scored = []
        for w in range(1, size):
            chunk_result = comm.recv(source=w, tag=2)
            scored.extend(chunk_result)

        # ------ 4) 최고 갱신 ------
        for s, m in scored:
            if s > best[0]:
                best = (s, m)
                print(f'  [마스터] 새 최적: 점수 {round(s, 3)}, {m}')

        # ------ 5) 다음 frontier (top-N beam) ------
        scored.sort(key=lambda x: -x[0])
        frontier = [m for _, m in scored[:BEAM]]

    # ------ 종료 신호: 모든 워커에게 None 전송 ------
    for w in range(1, size):
        comm.send(DONE, dest=w, tag=1)

    print('=' * 60)
    print(f'[마스터] 최적 점수 : {round(best[0], 3)}')
    print(f'[마스터] 최적 분자 : {best[1]}')
    print(f'[마스터] 누적 방문 : {len(visited)}개')
    print(f'[마스터] 총 시간   : {time.time() - t_start:.2f}초')

else:
    # ============================================================
    # 워커 프로세스
    # ============================================================
    while True:
        chunk = comm.recv(source=0, tag=1)
        if chunk is DONE:
            print(f'  [워커 {rank}] 종료 신호 수신. 퇴근!')
            break

        # 자기 몫의 분자에 대해 점수 계산
        scored = [(score(s), s) for s in chunk]
        comm.send(scored, dest=0, tag=2)
