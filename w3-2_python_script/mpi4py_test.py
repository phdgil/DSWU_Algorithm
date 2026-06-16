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
print (my_files)
print ('*'*50)