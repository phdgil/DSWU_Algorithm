import pandas as pd
import glob
import time

#linear search: 아래 코드를 수정해서 zinc db로부터 pesticide를 찾아낼 수 있는 코드 작성.
#A*.txt로 코드를 테스트 한 후, 아래 코드를 mpi4py로 실행할 수 있도록 변경.

# 농약 로드
pesticides = pd.read_csv("pesticides.csv")['smiles'].tolist()

# ZINC 1900개 파일 순회
zinc_files = sorted(glob.glob("./zinc_data/*.csv"))
found = []
start = time.time()

for i, f in enumerate(zinc_files):
    zinc = pd.read_csv(f)
    for smi in zinc['smiles']:
        if smi in pesticides:
            found.append(smi)

    print(f"[{i+1}/{len(zinc_files)}] 발견: {len(found)}개 | {time.time()-start:.1f}초")

# 결과 저장
pd.DataFrame({'smiles': found}).to_csv("found_results.csv", index=False)
print(f"완료! 총 {len(found)}개 발견")