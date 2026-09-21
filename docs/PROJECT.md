# HTML Generator — 프로젝트 설명서

> 이 문서가 **기준 문서**다. 작업을 시작할 때 이것부터 읽는다.
> 규칙은 `RULES.md`, 진행 기록은 `PROGRESS.md`, 문제는 `ISSUES.md` 에 있다.
> 같은 내용을 두 문서에 적지 않는다.
>
> 작성 근거: 2026-09-20 코드 전수 조사. 추측 없이 실제 코드만 적었다.

---

## 1. 목적

교재(전자저작물)의 Reading 본문 페이지 HTML/CSS/JS 를 원고에서 자동으로 만든다.

### 확정된 설계 원칙

1. 이 프로그램은 **모든 프로젝트에 하나의 공통 HTML 규칙을 강제로 적용하는 프로그램이 아니다.**
2. 각 프로젝트는 자신의 **프로토 HTML** 을 가지고 있으며, 그 프로토 HTML에서 필요한 생성 규칙을 분석하여 사용한다.
3. **Claude 는 프로토타입을 분석하고 규칙을 추출하는 역할**을 하며, 반복적인 HTML 생성은 프로그램이 담당한다.
4. 기존에 만들어져 있는 **과거 HTML 을 무조건 똑같이 재현하는 것이 최종 목적은 아니다.**

### 최종적으로 만들려는 흐름 (확정)

프로젝트별 구조와 규칙을 Python이 매번 추측하는 것이 아니라, **Claude가 프로젝트를 최초 1회 분석하여 프로젝트별 구조·경로·규칙을 JSON으로 만들고, 일반 생성기는 그 JSON을 읽어 반복 생성**한다.

```
[프로젝트 자료 전체]
        ↓
[Claude 최초 분석]
        ↓
project_rules.json
  ├─ 프로젝트 기본 정보
  ├─ 모든 자료 경로
  ├─ 단원 목록 / 단원별 경로
  ├─ prototype 단원 / 페이지
  ├─ 페이지 구조 / 순서 / 타입
  ├─ 자료 ↔ 페이지 연결 관계
  └─ HTML / CSS / JS / popup / 예외 규칙
        ↓
[일반 HTML 생성기]
  ├─ 프로젝트 폴더 선택
  ├─ project_rules.json 선택
  ├─ prototype 단원 선택
  ├─ 생성할 단원 선택
  ├─ 페이지 선택
  └─ HTML 생성
```

**핵심 원칙:** 프로젝트별 지식은 Claude의 최초 분석 결과인 JSON에 기록한다. 일반 생성기는 JSON에 없는 프로젝트 구조를 임의로 추측하지 않는다.

### 현재 구현이 설계와 다른 점

| 항목 | 설계 의도 | 현재 구현 |
|---|---|---|
| 자료 위치 | 프로젝트마다 다른 폴더 구조를 받아들임 | `recipes/cj_reading.py setup()` 이 **CJ 프로젝트의 한글 폴더 이름을 코드에 박아** 기본 경로를 만든다. UI 선택 칸(`script_xlsx`·`storyboard_dir`·`guide_dir`·`contents_dir`)으로 덮어쓸 수 있다 |
| 규칙 출처 | 전부 프로토에서 | **19항목만** `rules.json` 에서 읽는다. 나머지 HTML 뼈대·본문 마크업·팝업 내부 구조는 `read_gen.py` 의 템플릿 문자열에 그대로 있다 |
| 자료 읽기 규칙 | 프로토/설정에서 | `read_import.py` 의 시트 이름·mp3 ID 규칙은 **코드 고정** (rules.json 에 항목은 있으나 읽지 않는다) |
| 쪽 이름 | 프로젝트마다 다름 | `p\d{3}_\d{2}` 를 **정규식으로 여러 곳에 박아** 두었다 |
| 프로토 | 프로젝트마다 지정 | 지금은 3단원. `settings.json` 의 `proto_lesson` 으로 지정. **최종적으로는 Claude 분석 JSON에 기록** |

---

## 1-1. 프로젝트 JSON의 역할 (새 기준)

현재 `project.json`은 단원 등록과 일부 설정을 담고 있지만, **최종 목표의 프로젝트 지도 전체를 담당하는 파일은 아니다.** 앞으로는 Claude 최초 분석 결과를 별도의 프로젝트 분석 JSON(가칭 `project_rules.json`)으로 관리하는 방향을 기준으로 한다.

### JSON에 반드시 포함해야 하는 프로젝트별 정보

- 프로젝트 root
- 스토리보드 파일/폴더 경로
- 녹음/사운드 Excel 경로
- 각 Excel의 실제 sheet 이름
- 지도서/PDF 경로
- 이미지/오디오 경로
- contents/산출 경로
- 단원 목록과 단원별 실제 경로
- 단원별 자료 연결 정보
- prototype 단원과 prototype 페이지 경로
- 페이지 목록, 순서, 타입, 파일명
- 페이지와 storyboard/Excel/audio/image의 연결 관계
- HTML/CSS/JS/popup 구조
- 프로젝트별 예외와 특수 단원 규칙

### 일반 생성기의 원칙

- JSON에 기록된 경로를 그대로 사용한다.
- `Lesson 01`, `lesson01`, `p001_01` 같은 현재 프로젝트의 형식을 새로운 프로젝트의 공통 규칙으로 가정하지 않는다.
- JSON에 없는 값을 코드가 조용히 추측하지 않는다.
- 필요한 정보가 없으면 누락/오류로 알려준다.
- 파일 존재 여부 확인은 가능하지만, **프로젝트 구조를 결정하는 주체는 JSON**이다.

---

## 2. 폴더·파일 구조

```
<프로젝트 폴더>/                       ← settings.json 의 root
├─ 01_스토리보드/<원고 폴더>/           단원별 xlsx (스토리보드)
├─ 02_사운드/<녹음 대본>.xlsx           단원 시트 = 문장·mp3 이름·단어·퀴즈
├─ 03_PDF/.../각론<N>.pdf               지도서 (한글 해석 원천)
├─ 00_개발물/EBOOK/.../contents/        산출 폴더
│   └─ lesson06/ops/                    ← 단원 하나의 산출물 + images/ + include/
└─ _딕테이션_생성기/                     ← 프로그램 본체
   ├─ HTML생성기.vbs                     실행기
   ├─ app.py · app_page.py               화면(로컬 웹서버 127.0.0.1:8765)
   ├─ runner.py                          껍데기 — 레시피를 불러 4단계를 돈다
   ├─ recipes/cj_reading.py              레시피 — 이 교재의 절차
   ├─ read_paths.py                      경로·단원 등록부·쪽번호 정규화
   ├─ project_io.py / project.json       단원 목록 (사람이 고칠 수 있음)
   ├─ proto_scan.py / rules_io.py        프로토 분석 · 규칙 파일 살림
   ├─ rules/cj_reading/                  proto_L<N>.json · rules.json
   ├─ read_import.py                     ① 추출 — 원고 → data<N>.py
   ├─ read_gen.py                        ② 생성 — data<N>.py → HTML/CSS/JS
   ├─ read_measure.py                    ③ 측정 — Playwright 로 잰 값
   ├─ read_verify.py                     ④ 검증
   ├─ layout_io.py / layout_edit.py      지면 구조(layout<N>.json) 읽기·화면 편집
   ├─ regress.py / _기준본/               회귀 검사
   ├─ 단원자료/                           data<N>.py · layout<N>.json · 잰 값
   ├─ _backup/                           산출물·layout·잰값 백업
   ├─ docs/                              ← 이 문서들
   └─ 문서/                               과거 작업 기록 (PROGRESS.md 17장 참고)
```

---

## 3. 전체 데이터 흐름 (실제 코드 기준)

```
[1] 자료 경로
    입력 : UI ① 자료 칸 → POST /api/settings → settings.json
    처리 : recipes/cj_reading.py setup(ctx)
           root 로 SB_DIR·SND·WORDDIC·CONTENTS·GEN 을 한글 이름으로 조립
           선택 칸(script_xlsx·storyboard_dir·guide_dir·contents_dir)이 있으면 덮어씀
           check(ctx) 가 SND 파일 / SB_DIR / CONTENTS 존재를 확인
    출력 : read_paths 모듈 전역(P.ROOT·P.SB_DIR·P.SND·P.CONTENTS…)

[2] 단원 찾기
    입력 : P.SB_DIR 의 xlsx, P.CONTENTS 의 하위 폴더
    처리 : cj_reading.discover() → units() → _register()
    출력 : project.json 의 units[] , read_paths.UNITS 등록부
    연결 : UI ③ 단원 칸 (GET /api/recipe/<id>)

[3] 프로토 분석  ※ 생성과 별개. 결과는 rules/ 에만 쌓인다
    입력 : 프로토 단원의 ops 폴더(HTML·CSS), 녹음 대본, 스토리보드
    처리 : cj_reading.analyze() → proto_scan.scan()
    출력 : rules/cj_reading/proto_L<N>.json
    승격 : rules_io.promote() → rules/cj_reading/rules.json

[4] ① 추출 (extract)
    입력 : 녹음 대본 <시트>, 스토리보드(구문 해설·미니 단어장·지시문), 각론 PDF,
           ops/images/<쪽>/*.png, 단원자료/layout<N>.json
    처리 : read_import.assemble() → apply_layout() → apply_kr()/apply_guide_kr()
           → clear_joins() → render()
    출력 : 단원자료/data<N>.py
    연결 : ② 생성이 이 파일을 import 한다

[5] ② 생성 (build)
    입력 : 단원자료/data<N>.py, 잰 값(scrolls/krlayout/popscroll<N>.py),
           스토리보드(구문 해설·미니 단어장 시트), rules/cj_reading/rules.json
    처리 : cj_reading.build() → read_gen.load_rules() → read_gen.build(only=고른 쪽)
    출력 : <ops>/p*.html · css/*.css · js/*.js · popup/*.html
    연결 : 미리보기가 이 폴더를 읽는다

[6] ③ 측정 (measure)
    입력 : 실기 ops 폴더의 HTML (P.ops(n)) — 임시 폴더가 아니라 늘 실기
    처리 : read_measure.measure(n, gen_dir=단원자료) — Playwright 로 실제 렌더
    출력 : 단원자료/scrolls<N>.py · krlayout<N>.py · popscroll<N>.py
    연결 : 다음 ② 생성이 이 값을 HTML 에 주입한다 (그래서 보통 생성→측정→생성)

[7] ④ 검증 (verify)
    입력 : 산출 폴더 + 원고
    처리 : read_verify.verify() — 파일 형식 / 문장 수 / 해석 글자 / mp3·이미지 존재 / scrollTop
    출력 : 화면 기록 (파일은 안 만든다)

[8] 미리보기
    입력 : **산출 폴더 전체** (고른 쪽과 무관)
    처리 : cj_reading.preview() = glob(ops/p*.html) + glob(ops/popup/*.html)
    출력 : 파일 목록 → /files/<레시피>/<단원>/ops/<상대경로> 로 iframe 서빙
```

---

## 4. 주요 구성요소와 역할

| 파일 | 역할 | 프로젝트 종속? |
|---|---|---|
| `app.py` / `app_page.py` | 로컬 화면. 일감(job) 관리, 정적 서빙 | 공통 |
| `runner.py` | 레시피 로더, `Ctx`, 4단계 실행, 백업/되돌리기, `.pyc` 청소 | 공통 |
| `recipes/cj_reading.py` | 이 교재의 절차. 경로 조립·단원 찾기·4단계 구현 | **종속** |
| `read_paths.py` | 경로 상수, 단원 등록부(`UNITS`), `pgkey()` | **종속** (상수) |
| `project_io.py` / `project.json` | 단원 목록 저장소 | 공통 |
| `proto_scan.py` | 프로토 HTML/CSS/엑셀에서 규칙 뽑기 | 대체로 공통 (쪽 이름 정규식만 종속) |
| `rules_io.py` | proto_L\<N\>.json ↔ rules.json ↔ 코드 값 대조 | 공통 |
| `read_import.py` | 원고 → `data<N>.py` | **종속** (시트 이름·ID 규칙) |
| `read_gen.py` | `data<N>.py` → HTML/CSS/JS | 반반 (뼈대는 템플릿 고정, 19항목은 rules.json) |
| `read_measure.py` | 실제 브라우저로 재기 | 대체로 공통 |
| `read_verify.py` | 산출물 점검 | **종속** (검사 항목이 이 교재 기준) |
| `layout_io.py` / `layout_edit.py` | 지면 구조 파일 읽기 / 화면 편집 | 공통 구조 + 종속 항목 |
| `regress.py` | 기준본과 바이트 대조 | 공통 |

---

## 5. 프로토 HTML 과 규칙 분석의 관계

- **프로토 단원** = 이 생성기가 만들지 **않은** 원래 납품 HTML. 현재 3단원.
  (6·7·8단원은 이 생성기가 만든 결과라 견본으로 쓰면 배울 것이 없다 — 순환)
- `proto_scan.scan()` 이 프로토 쪽의 `*.html` 과 `css/*.css`, 그리고 녹음 대본·스토리보드를 읽어
  `proto_L<N>.json` 에 항목을 적는다. `source` 로 어디서 봤는지 남긴다
  (`html` / `css` / `xlsx` / `none`).
- `rules_io.promote()` 가 고른 항목을 `rules.json` 으로 옮긴다.
- `rules_io.compare()` / `report()` 가 `rules.json` 과 **지금 코드가 내놓는 값**을 견준다.
  코드 쪽 값은 `_기준본` 을 프로토와 같은 잣대로 다시 읽어 만든다(`code_rules()`).

## 6. rules.json 의 역할

- 위치: `rules/cj_reading/rules.json`
- **읽는 곳은 `read_gen.load_rules(rid)` 단 한 곳**, 부르는 곳은 `recipes/cj_reading.py build()` 한 줄.
- `read_gen.R(key, default)` 가 값을 꺼내고, **없으면 코드에 있는 기본값**을 쓴다.
  → `rules.json` 을 지워도 결과가 달라지지 않는다.
- 값 안의 `{page}` · `{lesson}` 은 `read_gen._fill()` 이 채운다.
- 실제로 쓰이는 항목과 아직 안 쓰이는 항목의 구분은 `RULES.md` 에 있다.

## 7. 데이터와 생성기의 관계

`data<N>.py` 가 **단원 데이터의 전부**다. `read_gen` 은 이 파일 + 잰 값 + 스토리보드 두 시트만 본다.

```
data<N>.py :  PAGES(쪽별 원고·제목·퀴즈·think·mission) · ORDER · IMG · WORDBTN
              · CSS_LAYOUT · READSMART
잰 값      :  scrolls<N>.py(SCROLLS) · krlayout<N>.py(KR) · popscroll<N>.py(KOR1·ALL)
layout<N>.json : 문단 나눔(paras) · 라벨 · 말하는 이 · 지면 글자(text) · css · kr(해석)
```

`layout<N>.json` 은 **1~6단원에는 없다.** 7·8·Special Lesson 만 있고, 그 안의 `kr` 이 지금 이 세 단원 해석의 원천이다.

---

## 8. UI 의 실제 작업 흐름

화면은 왼쪽 세로 한 줄이다.

```
① 자료      root + 선택 칸 4개 → [자료 경로 저장]   (+ 접이식: 단원별 자료 = 시트·지도서 PDF)
② 프로토    프로토 단원 / 프로토 ops → [견본 쪽 불러오기] [프로토 분석] [승격] [코드와 대조]
③ 단원      체크박스 (project.json 의 units)
④ 쪽        체크박스 (비우면 단원 전체) + [전체 선택] [전체 해제]
⑤ 단계      추출 / 생성 / 측정 / 검증 체크박스 → [생성]
되돌리기    백업 고르기 → [이 백업으로 되돌리기]
회귀 검사   [기준본과 견주기] [지금 결과를 기준본으로]
오른쪽      [미리보기] | [설정] 탭 + 파일 목록 + iframe + 기록창
```

기능별 A/B/C 분류와 근거는 이 문서 9장에, 각 단추가 실제로 하는 일은 `RULES.md` 가 아니라 아래 9장 표에 있다.

---

## 9. 기능 분류 (A: 사용자용 / B: 개발·검증용 / C: 현재 목적상 불필요)

| 기능 | 코드 | 분류 | 근거 |
|---|---|---|---|
| ① 자료 경로 + 저장 | `POST /api/settings` → `settings.json` → `setup()` | **A** | 이것 없이는 아무것도 못 찾는다 |
| ① 단원별 자료(시트·지도서 PDF) | `POST /api/project` → `project.json` | **A** | 교재마다 다른 값. 파일을 직접 안 고치게 하는 칸 |
| ② 견본 쪽 불러오기 | `GET /api/proto` → `proto_pages()` | **B** | 분석 대상 쪽을 고르는 보조 |
| ② 프로토 분석 | `POST /api/analyze` → `proto_scan.scan()` | **B**(→장차 A) | 지금은 `rules/` 에만 쌓임. 설계상으로는 A 가 되어야 함 |
| ② 승격 | `POST /api/promote` → `rules_io.promote()` | **B**(→장차 A) | 위와 같음 |
| ② 코드와 대조 | `GET /api/compare` → `rules_io.report()` | **B** | 규칙과 코드가 어긋나는지 보는 개발용 |
| ③ 단원 | `GET /api/recipe/<id>` → `units()` | **A** | |
| ④ 쪽 | `GET /api/pages` → `read_gen.ORDER` | **A** | |
| ⑤ 단계(추출/생성/측정/검증) | `runner.STEPS` | **A** | 다만 사용자가 매번 고를 값은 아님 |
| [생성] | `POST /api/run` | **A** | |
| 미리보기 | `preview()` + `/files/...` | **A** | |
| 설정 탭(지면 다듬기) | `GET·POST /api/layout` → `layout_edit` | **B** | 손으로 해석·문단을 넣는 임시 수단. `guide_stream` 이 넓어지면 줄어듦 |
| 이 쪽만/전체 재생성 | `POST /api/regen` → `layout_edit.regen()` | **B** | ⑤ [생성] 과 기능이 겹친다 |
| 되돌리기 | `POST /api/restore` → `runner.restore()` | **A** | 덮어쓴 산출물을 되살리는 안전망 |
| 기준본과 견주기 | `POST /api/regress` mode=check | **B** | 개발 중 회귀 확인 전용 |
| 지금 결과를 기준본으로 | `POST /api/regress` mode=save | **B** | 개발자만 |
| 끝내기 | `POST /api/quit` | **A** | |

`C` 로 분류할 기능은 현재 **없다.** 겹치는 것(재생성 ↔ 생성)은 있으나 동작이 달라(안전망 되돌리기 포함) 단순 중복은 아니다.

---

## 10. 프로젝트 종속 / 공통 구분

### 이 프로젝트에만 맞는 부분 (다른 교재에서 깨진다)

| 무엇 | 코드 위치 |
|---|---|
| `01_스토리보드/전자저작물 추가 원고_20260716_아이스캔디 전달` | `recipes/cj_reading.py:47`, `read_paths.py:15` |
| `02_사운드/중3(소영순) 전자저작물 녹음 대본_최종_20260806 아이스캔디 전달.xlsx` | `recipes/cj_reading.py:49`, `read_paths.py:17` |
| `00_개발물/EBOOK/중학교 영어 3_소영순/app/resource/contents` | `recipes/cj_reading.py:52`, `read_paths.py:19` |
| `02_사운드/단어사전/lesson%02d` (**정의만 되고 아무도 안 씀**) | `read_paths.py:18` |
| 스토리보드 파일명 `… Lesson %d.xlsx` | `read_paths.py:16 SB_NAME`, `cj_reading.py:100 _NUM` |
| 산출 폴더 이름 `lesson%02d` | `read_paths.py:ops()`, `cj_reading.py:134` |
| 쪽 이름 `p\d{3}_\d{2}` | `proto_scan.py:28·74`, `read_import.page_key()`, `layout_edit.py` |
| 녹음 대본 mp3 ID `^\d+-(\d{3})-(.+?)-(\d+…)$` | `read_import.py:85 IDPAT` |
| 시트 이름 `<N>과` / `구문 해설` / `미니 단어장` / `Dictation` | `read_import.py` 여러 곳, `read_gen.py:133` |
| 지도서 파일명 `*각론<N>*.pdf` | `read_paths.guide_pdf()` |
| 각론 지면 좌표 상수(`GUIDE_MID=341` 등) | `read_import.py` GUIDE_* |
| 팝업 번호·클래스 이름(`korBtn`·`questionBtn`…) | `read_gen.py` 템플릿 — **일부는 rules.json 으로 뺐다** |
| 검증 항목(단어장·구문 번호·해석 팝업) | `read_verify.py` |

### 다른 프로젝트에도 쓸 수 있게 만든 부분

| 무엇 | 코드 위치 |
|---|---|
| 레시피 구조(`SLOTS`·`setup`·`units`·4단계·`outputs`·`preview`) | `runner.py` + `recipes/` |
| 단원 등록부를 코드가 아니라 파일로 | `project_io.py` / `project.json` / `read_paths.UNITS` |
| 프로토 분석 → 규칙 파일 | `proto_scan.py` / `rules_io.py` |
| 규칙을 생성에 쓰는 자리 | `read_gen.load_rules()` / `R()` / `_fill()` |
| 쪽 고르기(`only`) | `read_gen.build(only=…)` / `Ctx.pages` |
| 백업·되돌리기·백업 정리 | `runner.backup/restore/prune_*` |
| 회귀 검사 | `regress.py` |
| 묵은 `.pyc` 청소 | `runner.purge_pyc/refresh_modules` |
| 쪽 번호 정규화 | `read_paths.pgkey()` |

---

## 11. 작업 흐름

### 현재 실제 흐름 (코드 기준)

```
1. HTML생성기.vbs 실행 → 127.0.0.1:8765
2. ① 자료: 프로젝트 폴더 지정 → [자료 경로 저장]
   (필요하면 접이식 '단원별 자료' 에서 시트 이름·지도서 PDF 지정)
3. ③ 단원 하나 체크
4. ⑤ 단계 = 추출·생성·측정·검증 → [생성]        ← 첫 회는 쪽 목록이 없으므로 단원 전체
5. ④ 쪽 목록이 생김 → 고칠 쪽만 체크 → [생성] 다시
6. 오른쪽 [미리보기] 로 확인 (※ 고른 쪽과 무관하게 전체가 나온다 — ISSUES #1)
7. 해석·문단이 비면 [설정] 탭에서 손으로 채우고 [이 쪽만 재생성]
8. (개발자) [기준본과 견주기] 로 회귀 확인
```

프로토(②)는 **이 흐름에 들어 있지 않다.** 지금은 생성에 19항목만 영향을 준다.

### 최종 목표 흐름 (확정)

```
1. 프로젝트 폴더 선택
2. Claude가 최초 분석해 만든 프로젝트 JSON 선택
3. JSON에 기록된 prototype 단원 선택
4. JSON에 기록된 prototype 페이지 확인/분석
5. JSON에 기록된 생성 대상 단원 선택
6. (선택) 생성할 페이지 선택
7. [생성]
8. 미리보기 — 선택한 페이지 중심으로 표시
```

※ 현재의 `[프로토 분석] → rules.json → 생성` 흐름은 이 최종 구조로 가는 중간 단계다. `rules.json`에 항목을 계속 추가하는 것만으로 끝내지 않고, **프로젝트 경로/단원/페이지/자료 연결까지 포함한 프로젝트 JSON으로 확장**하는 것이 목표다.

없애거나 합쳐야 할 것:
- **[승격]** 을 [프로토 분석] 에 합친다 (분석 후 바로 rules.json).
- **[이 쪽만 재생성]·[단원 전체 재생성]** 을 ⑤ [생성] 으로 합친다.
- **⑤ 단계 체크박스**를 숨긴다 (추출→생성→측정→생성→검증이 정해진 순서).
- **[설정] 탭**은 규칙 자동화가 끝나는 만큼 줄어든다.
- **[코드와 대조]·회귀 검사 2개**는 개발자 화면으로 접는다.

---

## 12. 아직 확정되지 않은 것

- Claude 분석 JSON과 기존 `project.json`/`rules.json`의 최종 역할 분담을 어떻게 할 것인가.
- `read_gen` 의 HTML 뼈대(본문 마크업·팝업 내부 구조)를 프로젝트 JSON/규칙 데이터로 어디까지 옮길 것인가.
- `read_import` 의 자료 읽기 규칙(시트 이름·ID 패턴·열 번호)을 프로젝트 JSON/규칙 데이터로 옮길 것인가.
  (`rules.json` 에 항목은 있으나 `read_import` 는 읽지 않는다)
- 쪽 이름 규칙(`p\d{3}_\d{2}`)을 어떻게 일반화할 것인가.
- 프로토에서 못 뽑는 3항목(측정 여백)을 어디에 둘 것인가.
- 1~6단원을 이 생성기로 다시 만들 것인가 → **만들지 않기로 했다**(2026-09-17 결정).
