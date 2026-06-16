# DSWU Algorithm

덕성여자대학교 알고리즘 강의 자료 저장소입니다. Python 기반 알고리즘 실습에서 시작해 pandas, ZINC 데이터 다운로드, 분할 정복, Big-O 표기법, MPI 병렬 처리, 정렬/탐색/그래프 알고리즘, 분자 데이터 기반 greedy/dynamic programming 응용, SMARTS와 fingerprint 유사도 분석까지 다룹니다.

## 강의 흐름 요약

이 저장소는 알고리즘의 기본 개념을 실습 중심으로 학습하고, 후반부에는 화합물/농약 후보 분석 문제에 알고리즘을 적용하는 자료로 구성되어 있습니다.

- 1주차: 알고리즘 개요와 기본 사고 방식
- 2주차: pandas 기초와 ZINC 데이터베이스 다운로드 자동화
- 3주차: 분할 정복, pseudo code, Big-O notation, mpi4py 병렬 처리
- 4주차: 정렬 알고리즘과 KISTI 실습 자료
- 6주차: 탐색 알고리즘
- 7주차: 그래프 알고리즘과 MPI 코드 해설
- 9주차: 분자 데이터에 대한 greedy algorithm 응용
- 10주차: dynamic programming과 농약 구조 점수화
- 11주차: SMARTS 패턴, pesticide 구조 탐색, fingerprint/Tanimoto similarity
- 기말: 알고리즘 기말고사 템플릿

## 파일 구성

| 파일/폴더 | 형식 | 내용 |
| --- | --- | --- |
| [`W1-1 Algorithm.pdf`](<W1-1 Algorithm.pdf>) | PDF | 알고리즘 강의 도입 자료입니다. 알고리즘의 기본 개념과 수업 전체의 출발점을 정리합니다. |
| [`W1-1 Algorithm.pptx`](<W1-1 Algorithm.pptx>) | PPTX | 1주차 알고리즘 개요 발표 자료입니다. |
| [`W2-1 pandas basic.pdf`](<W2-1 pandas basic.pdf>) | PDF | pandas 기초 문법과 데이터 처리 흐름을 설명하는 강의 자료입니다. |
| [`W2-1 pandas basic.pptx`](<W2-1 pandas basic.pptx>) | PPTX | pandas 기본 사용법 발표 자료입니다. |
| [`w2-2_download_zinc.ipynb`](<w2-2_download_zinc.ipynb>) | Notebook | ZINC DB 다운로드 자동화 실습 노트북입니다. 파일 읽기, 리스트, 반복문을 활용합니다. |
| [`w2_2_download_zinc_colab.ipynb`](<w2_2_download_zinc_colab.ipynb>) | Notebook | Google Colab 환경에서 ZINC DB 다운로드 실습을 수행하는 노트북입니다. |
| [`ZINC-downloader-2D-txt.uri`](<ZINC-downloader-2D-txt.uri>) | URI | ZINC 2D text 데이터 다운로드에 사용하는 URI 목록입니다. |
| [`w3-1 divide_and_conquer.pptx`](<w3-1 divide_and_conquer.pptx>) | PPTX | 분할 정복 알고리즘 강의 자료입니다. |
| [`w3-1_divide_and_conquer.ipynb`](<w3-1_divide_and_conquer.ipynb>) | Notebook | 분할 정복 개념과 관련 퀴즈를 포함한 실습 노트북입니다. |
| [`w3-1_divide_and_conquer-student.ipynb`](<w3-1_divide_and_conquer-student.ipynb>) | Notebook | 학생 실습용 분할 정복 노트북입니다. 일부 코드를 직접 채우는 형태입니다. |
| [`w3-2 pseudo_code_BigO_notation_mpi4py.pdf`](<w3-2 pseudo_code_BigO_notation_mpi4py.pdf>) | PDF | pseudo code, Big-O notation, mpi4py 병렬 처리 개념을 설명하는 자료입니다. |
| [`w3-2 pseudo_code_BigO_notation_mpi4py.pptx`](<w3-2 pseudo_code_BigO_notation_mpi4py.pptx>) | PPTX | 3주차 pseudo code, Big-O, mpi4py 발표 자료입니다. |
| [`w3-2_python_script/`](<w3-2_python_script/>) | Folder | mpi4py 실습용 Python 스크립트 폴더입니다. |
| [`w3-2_python_script/mpi4py_test.py`](<w3-2_python_script/mpi4py_test.py>) | Python | mpi4py 기본 동작과 병렬 실행을 확인하는 테스트 스크립트입니다. |
| [`w3-2_python_script/mpi4py_find_logp_min.py`](<w3-2_python_script/mpi4py_find_logp_min.py>) | Python | pandas와 mpi4py를 사용해 분자 데이터에서 logP 최솟값을 찾는 병렬 처리 예제입니다. |
| [`w4-1_sorting.ipynb`](<w4-1_sorting.ipynb>) | Notebook | 정렬 알고리즘 실습 노트북입니다. |
| [`w4-1_sorting-student.ipynb`](<w4-1_sorting-student.ipynb>) | Notebook | 학생 실습용 정렬 알고리즘 노트북입니다. |
| [`w4-2_sorting_kisti.pdf`](<w4-2_sorting_kisti.pdf>) | PDF | KISTI 환경 또는 관련 실습을 포함한 정렬 알고리즘 자료입니다. |
| [`w4-2_sorting_kisti.pptx`](<w4-2_sorting_kisti.pptx>) | PPTX | KISTI 연계 정렬 알고리즘 발표 자료입니다. |
| [`w6-2_search_algorithm.ipynb`](<w6-2_search_algorithm.ipynb>) | Notebook | 탐색 알고리즘 실습 노트북입니다. |
| [`w6-2_search_algorithm.py`](<w6-2_search_algorithm.py>) | Python | pandas, glob, time을 활용한 탐색 알고리즘 Python 예제입니다. |
| [`w7-2_graph_algorithm.ipynb`](<w7-2_graph_algorithm.ipynb>) | Notebook | adjacency matrix, distance matrix 등 그래프 기반 알고리즘 개념을 다루는 노트북입니다. |
| [`w7-2_mpi4py_code_explained.py`](<w7-2_mpi4py_code_explained.py>) | Python | mpi4py 기반 병렬 처리 코드를 설명하는 Python 스크립트입니다. |
| [`w9-1_molecule_greedy.ipynb`](<w9-1_molecule_greedy.ipynb>) | Notebook | 분자 데이터 문제에 greedy algorithm을 적용하는 실습 노트북입니다. |
| [`w9-1_molecule_greedy_additional_description.ipynb`](<w9-1_molecule_greedy_additional_description.ipynb>) | Notebook | greedy algorithm 분자 응용에 대한 추가 설명 자료입니다. |
| [`w10-1_molecule_dp.ipynb`](<w10-1_molecule_dp.ipynb>) | Notebook | 분자 데이터 문제에 dynamic programming을 적용하는 실습 노트북입니다. |
| [`w10-1_molecule_dp_kisti.py`](<w10-1_molecule_dp_kisti.py>) | Python | mpi4py와 RDKit을 활용해 QED, logP 등 분자 특성을 계산하는 KISTI용 Python 스크립트입니다. |
| [`w10-2_agrochemical_score.ipynb`](<w10-2_agrochemical_score.ipynb>) | Notebook | 농약 구조 분포 분석과 agrochemical score 계산 실습 노트북입니다. |
| [`w11-1_smarts_pesticide.ipynb`](<w11-1_smarts_pesticide.ipynb>) | Notebook | SMARTS 패턴을 활용해 pesticide 관련 구조를 탐색하는 실습 노트북입니다. |
| [`w11-1_smarts_pesticide_lecture.pptx`](<w11-1_smarts_pesticide_lecture.pptx>) | PPTX | SMARTS와 pesticide 구조 분석 강의 발표 자료입니다. |
| [`w11-2_fingerprint_tanimoto.ipynb`](<w11-2_fingerprint_tanimoto.ipynb>) | Notebook | molecular fingerprint와 Tanimoto similarity 기반 유사도 분석 실습 노트북입니다. |
| [`algorithm_final_exam_template.ipynb`](<algorithm_final_exam_template.ipynb>) | Notebook | 알고리즘 기말고사 템플릿 노트북입니다. |

## 실행 환경

기본 실습은 Jupyter Notebook 또는 Google Colab에서 실행할 수 있습니다. 일부 고급 실습은 다음 Python 패키지를 사용합니다.

- `pandas`
- `mpi4py`
- `rdkit`

MPI 예제는 로컬 또는 클러스터 환경에서 `mpiexec`/`mpirun`으로 실행합니다. 예:

```bash
mpiexec -n 4 python w3-2_python_script/mpi4py_test.py
```

PDF와 PPTX 파일은 강의용 읽기 자료이며, notebook 파일은 수업 중 실습과 과제/시험 템플릿으로 사용할 수 있습니다.
