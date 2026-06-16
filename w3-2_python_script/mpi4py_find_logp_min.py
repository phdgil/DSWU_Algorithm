from mpi4py import MPI
import pandas as pd
import glob

# 1. comm (Communicator, 통신 도구함)
# - 모든 프로세스가 모여 있는 '채팅방' 또는 '전화망'이라고 생각하면 됩니다.
# - MPI.COMM_WORLD는 현재 실행된 모든 일꾼(Process)이 포함된 기본 통신 그룹입니다.
# - 이 객체를 통해 "데이터를 보내라(send)", "받아라(recv)", "합쳐라(reduce)" 같은 명령을 내립니다.
comm = MPI.COMM_WORLD

# 2. rank (Rank, 내 번호/신분증)
# - 전체 채팅방에서 '나'에게 부여된 고유한 ID 번호입니다.
# - 0번부터 (size - 1)번까지 부여됩니다.
# - "if rank == 0:" 처럼 특정 번호에게만 특별한 임무(결과 취합, 파일 출력 등)를 맡길 때 사용합니다.
rank = comm.Get_rank()

# 3. size (Size, 전체 인원수)
# - 터미널에서 'mpirun -np 6'이라고 쳤을 때의 '6'에 해당하는 전체 일꾼 수입니다.
# - 데이터를 몇 등분으로 나눌지 결정할 때 분모(Step) 역할을 합니다.
# - 모든 프로세스는 똑같은 size 값을 공유합니다.
size = comm.Get_size()

print(f"안녕하세요! 저는 {size}명 중 {rank}번 일꾼입니다.")

# 2. 일 나누기 (2,000개 파일을 사람 수대로 쪼개기)
all_files = sorted(glob.glob('./zinc_db/*.txt'))
my_files = all_files[rank::size] 

# 3. 각자 자기 일 하기 (자기 할당량에서 최솟값 찾기)
local_results = []
for f in my_files:
    df = pd.read_csv(f, sep='\t', usecols=['smiles', 'logp'])
    
    min_logp = df['logp'].min()
    min_smi = df.loc[df['logp']==min_logp, 'smiles']
    min_dict = {'smiles':', '.join(min_smi.to_list()),'logp':min_logp}

    local_results.append(min_dict) # 각 파일의 1등만 보관

# 4. 결과 취합 (내 결과물 뭉치기)
my_best = pd.DataFrame(local_results)

# 5. 최종 보고 (모든 일꾼의 결과를 Rank 0에게 전달)
all_reports = comm.gather(my_best, root=0)

# 6. 정답 발표 (Rank 0만 수행)
if rank == 0:
    # gather의 결과는 리스트이므로 하나로 합칩니다
    final_df = pd.concat(all_reports, ignore_index=True)
    
    # 전체 중 가장 낮은 logp 찾기
    lowest_idx = final_df['logp'].idxmin()
    best_match = final_df.loc[lowest_idx]
    
    print("\n" + "="*30)
    print("      --- 최종 분석 결과 ---")
    print(f"SMILES: {best_match['smiles']}")
    print(f"Lowest LogP: {best_match['logp']}")
    print("="*30)