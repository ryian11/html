# project_rules.json 구조 설계안 (분석 전용 — 코드 수정 없음)

작성일: 2026-09-22
대상: `_딕테이션_생성기` (CJ 중3 영어 Reading 딕테이션 생성기)
성격: **분석 + 계획만**. 이 문서에 적힌 어떤 것도 아직 코드에 반영되지 않았습니다.
표기: 코드에서 실제로 확인한 내용만 적었습니다. 확인하지 못한 부분은 `<확인 필요>` 로 표시했습니다.

---

## 0. 목표 재확인

```
프로젝트 자료 (스토리보드·녹음대본·각론 PDF·프로토 HTML)
   ↓ Claude가 분석
project_rules.json  (프로젝트 구조 + 프로토에서 뽑은 생성 규칙)
   ↓ 읽음
일반 HTML 생성기 (Python, 프로젝트별 하드코딩 없음)
   ↓ 단원/페이지 선택
HTML 생성
```

3단원이 프로토타입입니다. 3단원에 없는 기능을 억지로 규칙에 채우지 않습니다.
6단원은 새 프로토타입이 아니라 3단원 규칙으로 만들어지는 대상 단원입니다.

---

## 1. 현재 코드 흐름 재추적 (파일 · 함수 단위)

### 1-1. 프로젝트 열기 / 폴더 선택
```
사용자가 [프로젝트 폴더] 선택
  → app.py  /api/settings (POST)          — 고른 root 를 settings.json 에 저장
  → app.py  /api/ls                        — 폴더 한 단계만 보여줌(재귀 없음, 추측 없음)
  → recipes/cj_reading.py  setup(ctx)      — root 로부터 SB_DIR/SND/WORDDIC/CONTENTS/GEN 계산
       ← 이 계산식 자체가 문제의 핵심(1-6절에서 다룸): 폴더명이 코드에 박혀 있음
  → recipes/cj_reading.py  units(ctx)      — project.json + discover() 로 단원 목록 확정
       → project_io.units(rid)             — project.json 읽기 (이미 JSON화된 부분)
       → discover(ctx)                     — SB_DIR/CONTENTS 를 정규식으로 훑어 빈 자리만 채움
       → project_io.put_units(rid, ...)    — 합친 결과를 project.json 에 다시 저장
       → _register(ctx, lst)               — read_paths.UNITS 에 등록(다른 함수들이 여기서 찾음)
```

### 1-2. 프로토 분석 (견본 단원 → 규칙 추출)
```
사용자가 [프로토 단원] 지정 + 견본 쪽 선택 + [프로토 분석]
  → app.py  /api/analyze (POST)
  → recipes/cj_reading.py  analyze(ctx, pages)
       → proto_ops(ctx) / proto_lesson(ctx)        — 견본 ops 폴더 결정
       → proto_scan.scan(rid, lesson, ops, pages, sound_xlsx=P.SND, sb_xlsx=P.storyboard(n))
            scan_page(html)      — data-pop-idx, data-use, css/js, mp4/vtt/mp3 링크 등 정규식 추출
            scan_css(css)        — images/{page}/*.png 이름 틀 추출
            scan_sound(xlsx, n)  — 그 과 시트에서 ID열·글열·ID모양·코너이름 추정
            scan_storyboard(xlsx)— 시트 이름 목록만 확인
       → rules_io.put(...) 로 rules/cj_reading/proto_L<N>.json 에 기록
  화면에는 app.py _proto_info() 가 "이번에 새로 본 것 / rules.json 과 다른 것 / 프로토로는
  알 수 없는 것"을 계산해 카드로 보여줌 (읽기 전용, rules.json 을 건드리지 않음)
```

### 1-3. 규칙 확정 (승격)
```
사용자가 [이 규칙 쓰기]
  → app.py  /api/promote (POST)
  → rules_io.promote(rid, lesson, keys, fresh=False)
       proto_L<N>.json 의 항목을 rules.json 에 key 단위로 합침
       (없던 key 만 추가/갱신, 이번 분석에 없는 예전 key 는 그대로 둠 — 9/21 수정분)
```

### 1-4. 생성 (자료 → data<N>.py → HTML)
```
사용자가 단원 + 쪽 선택 + [생성]
  → app.py  /api/run (POST, steps=['extract','build',...])
  → runner.py  Ctx / 백업 / .pyc 정리 후 recipe 의 각 단계 함수 호출
       extract(ctx, unit)
            → read_import.assemble(unit)      — 대본/스토리보드/각론 PDF/이미지 크기를 data 형태로
              ※ 이 함수는 rules.json 을 전혀 읽지 않음 (grep 으로 확인, 아래 2절)
            → data<N>.py 로 저장
       build(ctx, unit)
            → read_gen.load_rules(rid)        — rules.json 을 읽어 RULES 전역에 올림
            → read_gen.build(unit, out=..., only=ctx.pages)
                 R(key, default) 를 통해 20개 자리에서 규칙값(없으면 코드 기본값) 사용
                 HEAD / ALL_HEAD (긴 하드코딩 템플릿 문자열)에 값 채워 넣음
            → read_gen.missed_rules() 로 이번에 기본값으로 메운 항목을 사용자에게 알림
       measure(ctx, unit) / verify(ctx, unit)  — 이번 요청과 직접 관련 없음(생략)
```

### 1-5. 미리보기 / 대조
```
[미리보기] → preview(ctx, unit) → layout_edit.page_files()/common_files() 로
             picked/common/other 세 묶음 반환 (생성 안 함, 읽기만)
[코드와 대조] → rules_io.compare(rid) → rules.json vs code_rules(rid)
             (code_rules 는 HTML 소스 정규식 + read_gen.py/read_import.py 소스코드 정규식으로
              "코드가 실제로 내놓는 값"을 재구성해서 비교 — 이것도 대조용일 뿐 생성에 안 쓰임)
[기준본과 견주기] → regress.py → _기준본/cj_reading/<단원> 과 바이트 단위 비교
```

---

## 2. `rules.json → read_gen` 은 연결, `rules.json → read_import` 은 미연결 — 실측 확인

`read_import.py` 전체에서 `rules_io` / `load_rules` / `RULES` 를 검색하면 **0건**입니다
(grep 실행 결과, 일치 없음). 즉 `read_import.py` 는 `rules.json` 의 존재를 전혀 모릅니다.

반대로 `read_gen.py` 는 `R(key, default)` 가 20곳에서 불리고, `rules.json` 의 항목 32개 중
20개가 실제로 생성에 쓰이는 자리에 대응합니다(6개는 아직 rules.json 에 없어 기본값으로
메워지는 중 — 3절 참고).

`rules.json` 안에는 `sound.*` / `storyboard.sheet.*` 항목 11개가 이미 들어 있지만
(proto_scan.scan() 이 만들어 둠), **어느 것도 read_import.py 가 읽지 않는** 죽은 데이터입니다.
대신 read_import.py 는 같은 정보를 **독립적으로 다시 하드코딩**해 두고 있습니다.

| rules.json 항목 | 실제로 쓰이는 코드 | 관계 |
|---|---|---|
| `sound.sheet` (`"%d과"`) | `read_import.py:92` `P.unit(n).get('sheet') or ('%d과' % int(n))` | rules.json 안 봄. 시트 이름은 사실 project.json(`units[].sheet`)에서 오고, 이 리터럴은 그 fallback일 뿐 |
| `sound.col.id` (2) / `sound.col.text` (1) | `read_import.py:96` `fid, txt = str(r[2] ...), norm(r[1])` | 하드코딩된 인덱스. 값은 우연히 같지만 연결 안 됨 |
| `sound.idPattern` | `read_import.py:90` 모듈 레벨 `IDPAT = re.compile(r'^\d+-(\d{3})-(.+?)-(\d+(?:-\d+)*)$')` | 하드코딩. rules.json 값과 문자열이 같지만(proto_scan 이 이 상수를 읽어 그대로 rules.json 에 적어둔 것이라 같음) read_import 는 여전히 자기 상수를 씀 |
| `sound.mp3` (`sep:'_', case:'lower'`) | `read_import.py:33` `mp3name()` `.replace('-','_').replace(' ','_').lower()` | 하드코딩 |
| `storyboard.sheet.구문 해설` 등 | `read_import.py:119` `openpyxl.load_workbook(...)['구문 해설']` | 시트 이름 리터럴. rules.json 항목은 "이 시트가 있더라"는 기록일 뿐, 실제로 그 이름을 rules.json 에서 읽어 쓰지 않음 |

**결론**: 현재 `read_import.py` 는 자료를 읽는 모든 규칙(시트 이름, 열 위치, ID 정규식,
mp3 이름 규칙)을 code에 하드코딩하고 있고, `proto_scan.py` 가 프로토에서 뽑아 rules.json 에
적어 두는 같은 정보는 **비교용으로만** 쓰입니다(`rules_io.compare()`/`code_rules()`).
사용자가 지난 메시지에서 지적한 문제가 코드 상에서 정확히 이 모양으로 확인됩니다.

---

## 3. `discover()` 의 현재 역할과 앞으로의 역할

### 현재 역할 (실측)
`recipes/cj_reading.py:108-138`

```python
_NUM   = re.compile(r'Lesson\s*0*(\d+)\s*\.xlsx$', re.I)
_NAMED = re.compile(r'_([A-Za-z][A-Za-z ]*Lesson)\s*\.xlsx$', re.I)
```
- `P.SB_DIR` 안의 `.xlsx`/`.xlsm` 파일명을 위 두 정규식으로 훑어 단원 id/이름/시트이름을 추정
- `P.CONTENTS` 안의 `lesson0*(\d+)` 폴더명을 훑어 ops 경로를 추정
- **다른 곳은 보지 않음** (주석에도 명시)

이 결과는 `units(ctx)` 에서 이렇게 쓰입니다:
```python
have = {u['id']: u for u in project_io.units(rid)}   # project.json 이 우선
for uid, e in discover(ctx).items():
    cur = have.setdefault(uid, {...})                 # project.json 에 없는 단원만 새로 추가
    for k in ('storyboard', 'ops'):
        if e.get(k) and not cur.get(k):                # 이미 있는 값은 절대 덮지 않음
            cur[k] = ...
```
즉 **project.json 에 이미 적힌 값은 discover() 가 절대 덮어쓰지 않습니다.** 빈 자리만 채우고,
채운 결과를 다시 project.json 에 저장합니다. 구조상으로는 "JSON이 기준, discover()는 보조"라는
원칙에 이미 상당히 가깝습니다.

### 문제
`discover()` 가 보조 역할을 하는 **방식 자체**(정규식 두 개, 폴더명 패턴 하나)가
CJ 프로젝트의 명명 관례(`Lesson N.xlsx`, `lessonNN` 폴더, `...Lesson.xlsx` 로 끝나는 특수단원)에
완전히 못박혀 있습니다. 다른 교재가 다른 파일명 규칙을 쓰면:
- `discover()` 는 아무것도 찾지 못하고 조용히 빈 dict `{}` 를 돌려줍니다.
- `units(ctx)` 는 `project.json` 이 이미 있으면 문제없이 그걸 쓰지만, **첫 프로젝트**라면
  단원이 하나도 안 잡히고, 화면에는 "왜 안 잡히는지" 이유가 나오지 않습니다.
  (프로젝트 지침 4번 "추측하지 않는다 — 없으면 오류/경고/누락 표시" 에 어긋남: 지금은
  침묵하는 실패입니다.)

### 앞으로의 역할 제안
| 구분 | 현재 | 제안 |
|---|---|---|
| 단원 목록의 기준 | project.json (사실상 이미 JSON 우선) | 그대로 유지 |
| 새 프로젝트 최초 채움 | discover() 의 하드코딩 정규식 | project_rules.json 에 **Claude가 분석해서 적어 둔 패턴 문자열**을 discover() 가 읽어서 매칭 (정규식 자체를 코드에서 빼냄) |
| project.json 에 이미 있는 값 | 절대 안 덮음 (유지) | 그대로 유지 |
| 패턴이 하나도 안 맞을 때 | 조용히 빈 목록 | 화면에 "이 패턴으로는 단원을 찾지 못했습니다 — project_rules.json 을 확인하거나 직접 추가하세요" 경고 표시 |
| 진단/검증 용도 | 없음 | project_rules.json 에 적힌 경로가 실제로 있는지 확인하는 별도 "검증" 버튼으로 분리 가능(프로젝트 지침 9번과 일치) |

`proto_scan.py:pages_in()` 의 `^(p\d{3}_\d{2})\.html$` 도 같은 성격의 문제입니다 —
프로토 ops 폴더에서 "고를 수 있는 견본 쪽" 목록을 만들 때 쓰는데, 이 페이지 이름 규칙 역시
CJ 전용이라 project_rules.json 으로 옮길 후보입니다.

---

## 4. 하드코딩 인벤토리 (요청하신 전 항목)

범례: **J** = JSON(주로 project.json)에 이미 있음 · **C** = 아직 Python 코드에 리터럴로 박혀 있음 · **X** = 미사용/불명

| 항목 | 현재 코드 위치 | 현재 역할 | 프로젝트별 정보? | JSON 이동 필요? |
|---|---|---|---|---|
| `ROOT` | `read_paths.py:5`, `settings.json` | 프로젝트 루트 절대경로 | 예 | 이미 JSON(settings.json)에 있음 — project_rules.json 으로 통합 가능 |
| `SB_DIR` | `read_paths.py:15` (기본값) + `cj_reading.py:47-48`(root 기준 재계산) | 스토리보드 폴더 경로 | 예 — 폴더명 `01_스토리보드/전자저작물 추가 원고_20260716_아이스캔디 전달` 자체가 이 프로젝트 전용 | **필요 (C)** |
| `SB_NAME` | `read_paths.py:16` | 단원별 스토리보드 파일명 틀(`%d` 자리) | 예 — 이 파일명 전체가 이 프로젝트 전용 | **필요 (C)** — 단, 실사용은 project.json 의 `units[].storyboard` 가 우선이라 fallback 전용 |
| `SND` | `read_paths.py:17` + `cj_reading.py:49-50` | 녹음 대본 엑셀 경로(교재명 포함) | 예 | **필요 (C)** |
| `WORDDIC` | `read_paths.py:18` + `cj_reading.py:51` | 단어사전 폴더 틀 | 예 | 필요하나 `<확인 필요>` — grep 상 이 두 대입 지점 외에 **읽는 코드가 없음**(미사용 가능성, 확인 필요) |
| `CONTENTS` | `read_paths.py:19-20` + `cj_reading.py:52-53` | 산출 폴더(교재명까지 포함한 깊은 경로) | 예 | **필요 (C)** — 가장 깊고 프로젝트 종속적인 경로 |
| `GEN` | `read_paths.py:21` + `cj_reading.py:54` | 생성기 프로그램 자신의 설치 위치 | 성격이 다름 — "자료"가 아니라 "생성기 자기 위치" | 이동은 가능하나, project_rules.json(자료 성격) 보다는 로컬 설정(설치 위치) 쪽이 더 맞을 수 있음 — 판단 필요 |
| `UNITS` (dict) | `read_paths.py:26`, `cj_reading.py:_register()` | 단원별 이름/시트/경로 등록부 | 예 | **이미 J** — project.json 에서 채워짐. 유일하게 완성된 사례 |
| 단원 번호 규칙 (`Lesson\s*0*(\d+)\.xlsx`) | `cj_reading.py:100` `_NUM` | 최초 단원 자동 발견 | 예 — CJ 파일명 관례 | **필요 (C)** |
| Special Lesson류 이름 규칙 (`_([A-Za-z][A-Za-z ]*Lesson)\.xlsx`) | `cj_reading.py:101` `_NAMED` | "…Lesson.xlsx" 형태의 특수 단원 자동 발견 | 예 | **필요 (C)** |
| contents 폴더명 규칙 (`^lesson0*(\d+)$`) | `cj_reading.py:134` | ops 폴더 자동 발견 | 예 | **필요 (C)** |
| 페이지 파일명 규칙 (`^p\d{3}_\d{2}\.html$`) | `proto_scan.py:30 pages_in()` | 프로토 견본 쪽 목록 만들기 | 예 — "p001_01" 형태는 CJ 관례 | **필요 (C)** — 사용자가 이미 지적한 항목 |
| 녹음 대본 시트 이름 (`%d과`) | project.json(`units[].sheet`, **J**) / `read_import.py:92` fallback(**C**) / `proto_scan.py:89` 별도 하드코딩(**C**) | 시트 선택 | 예 | 3곳 중 1곳만 J, 2곳 정리 필요 (동일 규칙이 세 군데 따로 박혀 있음) |
| `sound.col.id`/`sound.col.text` | rules.json 에 값 있음(**J**, 미연결) / `read_import.py:96` 하드코딩(**C**, 실사용) | 대본 열 위치 | 예 | **연결 필요** — 이미 J 로 뽑아놨지만 안 읽음 |
| `sound.idPattern` | rules.json(**J**, 미연결) / `read_import.py:90` `IDPAT`(**C**, 실사용) | 대본 ID 모양 검증 | 예 | **연결 필요** |
| `sound.mp3`(case/sep) | rules.json(**J**, 미연결) / `read_import.py:33` `mp3name()`(**C**, 실사용) | mp3 파일명 규칙 | 예 | **연결 필요** |
| `storyboard.sheet.*` | rules.json(**J**, 존재확인용) / `read_import.py:119` 등 시트 이름 리터럴(**C**) | 스토리보드 시트에서 데이터 읽기 | 예 | **일부 확인 필요** — 시트 이름 리터럴이 코드 여러 곳에 있는지 전수 확인 못함(`<확인 필요>`) |
| 각론 PDF 파일명 규칙 (`*각론%d*.pdf`) | `read_paths.py:81,84` | 지도서 PDF 찾기 | 예 — "각론"이라는 용어 자체가 이 교재 시리즈 전용 | **필요 (C)** |
| 이미지 폴더명 (`images`) | `read_import.py:231,250`, `read_gen.py:imgdir()` | 배경/제목 이미지 위치 | 애매 — `ops/images/<page>/...` 구조 중 `images` 라는 폴더명만 리터럴, 나머지는 이미 `P.ops(n)`(J) 기반 | 우선순위 낮음, 필요시 이동 |
| CJ 전용 popup/skeleton 규칙 (`popup.btn.*`, `skeleton.body.*`, `assets.*`) | rules.json(**J**, 연결됨) / `read_gen.py` `CSS_DEF`/`JS_DEF`/`SPEED_DEF` 등 코드 기본값(**C**, 이중화) | 팝업 번호·CSS/JS 목록·이미지 이름 틀 | 예 | **이미 대부분 연결됨** — read_gen.py 가 R() 로 읽음. 코드 기본값은 안전장치로 남아 있음(의도된 이중화, 문제라기보다 다음 단계에서 "기본값 없이 오류내기"로 갈지 여부만 결정하면 됨) |
| Lesson 1~8 고정, Special Lesson 항상 존재 | 코드에 숫자로 박혀 있지 않음 — project.json 에 실제 단원 8+1개가 나열되어 있을 뿐 | 없음(이미 안전) | 해당 없음 | **이동 불필요** — 이미 project.json 이 기준이라 코드에는 "8개"라는 가정이 없음(확인됨) |

---

## 5. CJ 전용 패턴을 일반 규칙으로 만들지 않는다 — 재확인

이번 조사에서 확인한 바로는, 코드에 "Lesson 은 무조건 1~8이다" 류의 **개수 하드코딩**은
없습니다(단원 목록은 project.json 이 기준). 문제는 개수가 아니라 **명명 패턴**입니다:

- `Lesson N.xlsx`, `lessonNN` 폴더, `p001_01` 페이지 이름, `%d과` 시트 이름, `*각론N*.pdf` —
  이런 "이름 짓는 방식"이 정규식으로 코드에 박혀 있습니다.
- 다른 프로젝트는 `Unit_3.xlsx`, `page-03-a.html`, `Chapter 3` 시트처럼 완전히 다른 규칙을
  쓸 수 있습니다. 이 문서의 4절 표에서 "필요(C)" 로 표시한 항목들이 정확히 이 위험군입니다.
- 다만 **한 가지는 이미 잘 되어 있습니다**: project.json 에 한 번 기록된 값(`units[].storyboard`,
  `units[].ops`, `units[].sheet`)은 discover() 의 정규식과 무관하게 그대로 쓰입니다.
  즉 "패턴이 안 맞아도 project.json 에 직접 적어 넣으면 동작은 한다"는 우회로는 이미 있습니다.
  다만 그 project.json 을 처음 채우는 방법이 지금은 "코드의 정규식에 우연히 맞기를 기다리거나,
  사람이 손으로 적는 것" 뿐이고, "Claude가 프로젝트를 분석해서 적어 준다"는 경로가 없습니다.

---

## 6. 지우면 안 되는 기존 기능 — 점검 결과

요청하신 목록을 하나씩 코드에서 확인했습니다. 이번 조사에서 삭제되거나 손상된 것은 없습니다
(이 작업은 분석만 했고 코드를 건드리지 않았습니다).

| 기능 | 현재 담당 코드 | 상태 |
|---|---|---|
| 프로토 분석 | `proto_scan.scan()` | 있음, 4-2절에서 재확인 |
| 페이지 선택 | `ctx.pages`, `read_gen.build(..., only=...)` | 있음 |
| HTML 생성 | `read_gen.build()` | 있음 |
| Preview | `recipes/cj_reading.py:preview()` (9/21 3단계 수정분, picked/common/other) | 있음 |
| popup | `read_gen.py` popup 관련 R() 20곳 | 있음 |
| CSS/JS | `skeleton.body.css/js`, `CSS_DEF`/`JS_DEF` | 있음 |
| Special Lesson | `project.json` 의 `special_lesson` 항목(`kr: "guide"` 처리 포함) | 있음 — 단, ops 폴더 파일 유실 버그는 별건으로 미해결 상태(이번 조사 대상 아님) |
| recipe 구조 | `runner.py` + `recipes/cj_reading.py` 단일 recipe | 있음 |
| rules.json | `rules_io.py` | 있음, merge 방식으로 9/21 개선됨 |
| backup | `runner.py` 백업/복원, `_backup_measured()` | 있음 |
| settings | `settings.json`, `/api/settings` | 있음 |
| recipe 구조 | (위와 중복 표기, 생략) | — |
| 기준본과 견주기(regress) | `regress.py` | 있음 — 알려진 데이터 손상 위험(Issue #5)은 그대로 미해결, 이번 조사에서 손대지 않음 |

---

## 7. UI 기능 15개 ↔ 코드 매핑

| UI 기능 | 화면(app_page.py) | 서버 API(app.py) | 실제 로직 |
|---|---|---|---|
| 1. 프로젝트 폴더 선택 | 폴더 선택창 → `/api/ls` 로 한 단계씩 탐색(재귀 없음) | `/api/ls`, `/api/settings`(POST) | `_ls()` — 추측 없이 보이는 대로만 |
| 2. 프로토 단원 선택 | `proto_lesson` 입력 → `protoChanged()` | `/api/proto` | `recipes.py:proto_lesson(ctx)` |
| 3. 견본 쪽 불러오기 | 자동 로드(9/21 2단계) | `/api/proto` | `proto_pages(ctx)` → `proto_scan.pages_in(ops)` |
| 4. 프로토 분석 | `[프로토 분석]` 버튼 | `/api/analyze`(POST) | `analyze(ctx, pages)` → `proto_scan.scan()` → `proto_L<N>.json` |
| 5. 승격(이 규칙 쓰기) | `[이 규칙 쓰기]`(9/21 promote() 수정) | `/api/promote`(POST) | `rules_io.promote()` — key merge |
| 6. 코드와 대조 | 분석결과 카드(newKeys/diffKeys) + 별도 대조 | `/api/compare` | `rules_io.compare()`/`code_rules()` |
| 7. 단원 선택 | 드롭다운(9/21 4단계 `pickedUnits()`) + "여러 단원" 체크박스 | `/api/project` | `units(ctx)` |
| 8. 페이지 목록 표시 | `showFiles()`에서 picked/common/other 3묶음 | `/api/pages` | `pages(ctx, unit)` → `read_gen.ORDER` |
| 9. 페이지 선택 | 체크박스 → `ctx.pages` | `/api/run`(POST) | `only=ctx.pages` 로 `read_gen.build()` 에 전달 |
| 10. HTML 생성 | `[생성]` | `/api/run`(POST, steps) | `runner.py` → `extract/build/measure/verify` |
| 11. Preview | iframe, `/files/...` 로 서빙 | `/api/pages`(preview 포함), `/files/*` | `preview(ctx, unit)` → `layout_edit.*` |
| 12. Settings | 개발자 도구 토글(9/21 1단계) | `/api/settings` | `settings.json` |
| 13. 되돌리기 | `[되돌리기]`(백업 복원) | `/api/restore` | `runner.py` 백업 폴더에서 복원 |
| 14. 기준본과 견주기 | 대조 버튼 | `/api/regress` | `regress.py:rebuild()`/`check()` |
| 15. 지금 결과를 기준본으로 | 기준본 저장 버튼 | `/api/regress`(save 모드로 추정) | `regress.py` — 세부 흐름 `<확인 필요>`(이번엔 안 읽음) |

**이전에 헷갈려하셨던 부분 다시 설명**
- **스토리보드가 폴더 선택만 해도 자동으로 뜨는 이유**: `setup(ctx)` 가 root 를 받자마자
  `P.SB_DIR` 을 계산해 버리기 때문입니다(코드에 박힌 하위 폴더명으로). 폴더를 고른 순간
  이미 "스토리보드 폴더 위치"가 정해져 있어서, 그 안의 파일 목록을 바로 보여줄 수 있는 것입니다.
  — 이게 정확히 4절에서 지적한 "SB_DIR 하드코딩"이 만들어내는 편의이자 동시에 위험입니다.
- **드롭다운 데이터 출처**: `units(ctx)` 가 돌려주는 목록이며, 이건 project.json(신뢰 기준)과
  discover() 결과(보조)를 합친 것입니다.
- **페이지 목록 출처**: 코드가 자료를 스캔해서 만드는 게 아니라, 이미 `extract()` 로 뽑아 둔
  `data<N>.py` 안의 `ORDER` 를 읽는 것입니다(`pages(ctx, unit)`). 그래서 [단원 준비]로 먼저
  추출을 해야 페이지 목록이 나옵니다.
- **선택한 페이지가 생성 함수까지 가는 경로**: 화면 체크박스 → `ctx.pages`(러너가 만드는
  컨텍스트 객체의 속성) → `build(ctx, unit)` 안에서 `only=getattr(ctx, 'pages', None)` 로
  `read_gen.build()` 에 그대로 넘어갑니다.
- **선택 안 한 페이지가 예전엔 왜 미리보기에 나왔는지**: 9/21 3단계 전에는 `preview()` 가
  폴더 안의 html 을 통째로 돌려줬기 때문입니다. 지금은 `layout_edit.page_files()` 로
  "선택한 쪽에 실제로 딸린 파일"만 골라내고, 나머지는 `common`(단원 공통) 또는 `other`
  (생성기가 안 만드는 파일, 예: `_dic1.html`) 로 분리합니다.
- **각 대조/기준본 기능이 실제로 하는 일**: "코드와 대조"는 rules.json 값과, 지금 코드가
  실제로 만들어내는 값을 비교만 합니다(고치지 않음). "기준본과 견주기"는 지금 생성 결과를
  과거에 저장해 둔 정답(`_기준본/`)과 바이트 단위로 비교합니다. 둘 다 **읽기 전용 검증**이고
  rules.json 이나 생성 결과를 바꾸지 않습니다.

---

## 8. 목표 최종 UI 흐름 (7단계)

요청하신 순서를 현재 코드 기준으로 다시 표현하면:

1. 프로젝트 폴더 선택 — `/api/ls`, `/api/settings`
2. **(신규)** Claude가 만든 `project_rules.json` 선택/불러오기 — 지금은 없는 단계.
   지금은 `setup(ctx)` 가 root 만 받고 나머지 경로를 코드로 계산합니다. 이 단계가 생기면
   `setup(ctx)` 는 `project_rules.json` 을 읽어 경로/패턴을 채우는 방식으로 바뀌어야 합니다.
3. 파싱된 프로젝트/단원/프로토/페이지 정보 표시 — 지금의 `_proto_info()` + `units(ctx)` +
   `pages(ctx, unit)` 를 하나의 요약 화면으로 합치는 것에 해당
4. 프로토 선택 — 지금의 (2)(3) 단계와 동일
5. 대상 단원 선택 — 지금의 (7) 단계와 동일
6. 대상 페이지 선택 — 지금의 (9) 단계와 동일
7. 생성 — 지금의 (10) 단계와 동일

**즉, 4~7단계는 이미 있는 기능을 순서만 재배치하면 되고, 2단계(project_rules.json 불러오기)가
유일하게 새로 만들어야 하는 UI/로직**입니다.

---

## 9. `rules.json` 의 현재 역할 분리 실태

| 역할 | 해당 항목 | 비고 |
|---|---|---|
| 실제 생성에 사용 | `popup.*`, `skeleton.*`, `assets.*` (20개 키) | `read_gen.py` R() 로 읽음 |
| 비교에만 사용 | `sound.*`, `storyboard.sheet.*` (11개 키) | `read_import.py` 는 안 읽음. `rules_io.compare()`만 봄 |
| 적어 둔 사실(규칙 아님) | `info.pageKinds` | `compare()` 도 건너뜀 |
| 프로토로는 알 수 없어 코드값 유지 | `measure.safeBody/safePop/gapKr` | `source: "none"`, 항상 코드 기본값 |
| 아직 rules.json 에 없어 코드 기본값 사용 중 | `popup.btn.thinkAboutBtn`, `popup.btn.exAnswerBtn`, `popup.thinkabout`, `popup.quiz.last`, `popup.btn.missionClearBtn`, `popup.missionclear` (6개) | 3단원 견본 쪽(현재 1쪽만 승격됨: `p050_02`)에 Think-About/마지막쪽 예외가 없어서 못 뽑은 것 — 프로토 원칙상 "3단원에 없으면 안 채워도 됨"에 해당 |

### `project_rules.json` / `rules/<recipe>/rules.json` 분업 제안 (코드 근거 기반)

지금 코드에는 이미 **두 층**이 있습니다 — project.json(경로/단원 목록) vs rules.json(생성 규칙).
`project_rules.json` 은 이 두 층을 하나의 파일로 합치되, 성격이 다른 정보를 구역으로 나누는
것이 제안입니다:

```
project_rules.json
  ├─ project / paths      ← 지금 settings.json + read_paths.py 하드코딩을 대체
  ├─ units                ← 지금 project.json 을 대체(또는 흡수)
  ├─ patterns             ← 지금 discover()/proto_scan.pages_in() 의 정규식을 대체 (신규)
  └─ prototype            ← 지금 rules/<recipe>/rules.json 의 생성 규칙을 가리키거나 포함

rules/<recipe>/rules.json  ← 유지: 프로토에서 뽑은 "생성 규칙 값" 자체(팝업 번호, CSS 목록 등)는
                              지금처럼 recipe 전용 파일에 남기는 편이 자연스러움
                              (recipe 마다 이 파일의 내용 모양이 완전히 다를 수 있으므로)
```

이렇게 나누는 근거: `project_rules.json` 에 들어갈 정보(경로, 단원 목록, 명명 패턴)는
**recipe 와 무관하게** UI가 프로젝트를 여는 시점에 필요하고, `rules/<recipe>/rules.json` 의
정보(팝업 번호 등)는 **recipe 의 생성 로직**이 알아야 하는 것이라 이미 recipe 별 폴더 구조
(`rules/cj_reading/`)를 갖추고 있기 때문입니다. 다만 이 분업이 맞는지는 recipe 가 하나뿐인
지금 상태로는 완전히 검증되지 않으므로 `<확인 필요>` 로 남겨 둡니다 — recipe 가 두 개 이상
생길 때(다른 교재) 진짜로 갈라지는지 봐야 합니다.

---

## 10. 문제 우선순위 (A~E)

**A. 반드시 구조를 바꿔야 하는 문제**
- A1. `read_import.py` 가 `rules.json`(`sound.*`)을 안 읽음 — 사용자가 이번에 콕 집은 문제
- A2. `SB_DIR`/`SND`/`CONTENTS`/`WORDDIC`/각론 PDF 경로가 `setup()`/`read_paths.py` 에
  폴더명 리터럴로 박혀 있음 — project_rules.json 의 "자료 위치" 구역이 대체해야 할 핵심

**B. 지금 구조에서도 유지 가능**
- B1. `popup.*`/`skeleton.*`/`assets.*` → `read_gen.py` 연결 — 이미 잘 됨, 그대로 유지
- B2. project.json 기반 단원 등록부 — 이미 JSON 우선 구조, 그대로 유지
- B3. `rules_io.promote()` 의 key-merge 방식(9/21 수정) — 그대로 유지

**C. 나중에 개선해도 됨**
- C1. `discover()` 의 정규식을 project_rules.json 의 patterns 구역으로 이동 (지금도
  project.json 이 있으면 정상 동작하므로 급하지 않음)
- C2. `proto_scan.pages_in()` 의 페이지 이름 정규식 이동
- C3. `GEN`(생성기 자기 위치)을 JSON 으로 옮길지 여부 — 성격이 달라 후순위
- C4. `HEAD`/`ALL_HEAD` 하드코딩 템플릿을 프로토 유래 골격으로 대체 — 범위가 크고 위험도 높음

**D. 기존 기능을 깨뜨릴 가능성이 높은 부분**
- D1. `read_import.py` 를 rules.json 에 연결하면서 **기본값 fallback 을 어떻게 유지할지**가
  관건 — 지금 `read_gen.py` 의 `R(key, default)` 패턴처럼 "없으면 기존 코드값" 방식을
  그대로 따르지 않으면, rules.json 에 아직 없는 6개 팝업 키처럼 read_import 쪽도 결측이
  생길 때 조용히 다른 값을 쓸 위험이 있음
- D2. `HEAD`/`ALL_HEAD` 교체(C4) — 현재 모든 생성 결과가 이 템플릿에서 나오므로 손대면
  8단원 회귀 전체가 흔들릴 수 있음

**E. 새 프로젝트 테스트가 필요한 부분**
- E1. project_rules.json 의 patterns 구역이 실제로 "다른 명명 규칙"에서도 동작하는지는
  이 프로젝트(CJ) 안에서는 검증 불가 — 다른 교재 프로젝트가 있어야 확인 가능
- E2. recipe 가 2개 이상일 때 project_rules.json / rules/<recipe>/rules.json 분업이
  맞는지(9절 참고)

---

## 11. 단계별 변경 계획 (코드 아님 — 계획만)

작은 단위로 나눴습니다. 각 단계는 이전 단계가 승인·완료된 뒤에만 진행합니다.

### 0단계 — project_rules.json 스키마 확정 (코드 변경 없음)
- 수정 대상: 없음(문서만)
- 변경 내용: 이 문서 12절의 스키마를 사용자가 확인/수정
- 테스트 방법: 해당 없음

### 1단계 — `read_import.py` ↔ `rules.json` 연결 (A1, 가장 작고 사용자가 이미 요청한 부분)
- 수정 대상 파일/함수: `read_import.py` 의 `sound()`(대본 열 위치·ID 정규식·시트 이름),
  `mp3name()`(mp3 규칙), `syntax_sentences()`(구문 해설 시트 이름)
- 변경 내용: `read_gen.py` 의 `load_rules()`/`R()` 과 같은 패턴을 `read_import.py` 에도 도입.
  즉 하드코딩된 `IDPAT`, `r[1]`/`r[2]`, `'구문 해설'` 등을 `R('sound.idPattern', IDPAT.pattern)`
  식으로 바꾸되 **기본값은 지금 코드값 그대로** 둬서 결과가 안 바뀌게 함(read_gen.py 의
  1순위 작업과 동일한 안전장치)
- 무엇을 JSON으로 옮기는가: `sound.col.id/col.text/idPattern/mp3/sheet`, `storyboard.sheet.*`
  (이미 rules.json 에 값은 있음 — "옮기기"가 아니라 "연결하기")
- 기존 기능 영향: 없어야 함(기본값 fallback 원칙 유지 시). rules.json 값이 코드 기본값과
  현재 동일하므로(3단원 분석 결과) 8단원 등 다른 단원 추출 결과도 그대로여야 함
- 테스트 방법: 8단원(회귀 기준 있음) `extract()` 재실행 → `data8.py` 바이트 비교,
  `missed_rules()` 와 같은 방식으로 "read_import 쪽 결측 규칙" 로그 추가해 확인

### 2단계 — project_rules.json 의 "자료 위치" 구역으로 경로 하드코딩 이동 (A2)
- 수정 대상: `recipes/cj_reading.py:setup()`, `read_paths.py` 상단 상수들
- 변경 내용: `setup(ctx)` 가 폴더명을 스스로 조립하는 대신 `project_rules.json.paths.*` 를
  그대로 읽어 `P.SB_DIR` 등에 대입. 파일이 없거나 값이 없으면 지금처럼 UI 슬롯(`script_xlsx` 등)
  으로 덮어쓸 수 있는 기존 동작은 유지
- 무엇을 JSON으로 옮기는가: `SB_DIR`, `SND`, `WORDDIC`, `CONTENTS`, 각론 PDF 패턴
- 기존 기능 영향: `check(ctx)` 의 경로 존재 검사, UI 슬롯 오버라이드 로직에 영향 — 신중히 확인 필요
- 테스트 방법: project_rules.json 없이 실행 시 지금과 동일한 기본 경로가 나오는지(하위호환),
  있을 때 그 값이 우선하는지 두 경우 모두 확인

### 3단계 — `discover()`/`proto_scan.pages_in()` 패턴을 project_rules.json 의 "patterns" 구역으로
- 수정 대상: `recipes/cj_reading.py:_NUM/_NAMED/discover()`, `proto_scan.py:pages_in()`
- 변경 내용: 정규식 리터럴을 project_rules.json 에서 읽어오게 변경, 패턴이 없으면
  "찾지 못했습니다" 경고를 명시적으로 냄(지금의 침묵 실패 제거)
- 기존 기능 영향: project.json 이 이미 채워진 지금 프로젝트는 영향 적음(discover 는 보조라서).
  다만 최초 탐색 로직이 바뀌므로 새 프로젝트 시나리오로 반드시 확인
- 테스트 방법: 지금 project.json 을 지운 상태로 재탐색했을 때 같은 9개 단원이 다시 잡히는지

### 4단계 이후 (C3, C4 등)
- 범위가 크고(특히 HEAD/ALL_HEAD) 위험도가 높아(D2), 1~3단계 완료 후 별도로 계획

---

## 12. `project_rules.json` 스키마 초안

```json
{
  "schema": 1,
  "project": {
    "name": "<확인 필요 — project.json 의 'name' 필드가 '2026_cj_midd3_eng' 로 실측됨>",
    "root": "E:\\00_works\\2026\\2026_cj_midd3_eng"
  },
  "paths": {
    "storyboardDir": "01_스토리보드/전자저작물 추가 원고_20260716_아이스캔디 전달",
    "soundXlsx": "02_사운드/중3(소영순) 전자저작물 녹음 대본_최종_20260806 아이스캔디 전달.xlsx",
    "wordDicDir": "02_사운드/단어사전/lesson{unit:02d}",
    "contentsDir": "00_개발물/EBOOK/중학교 영어 3_소영순/app/resource/contents",
    "guideDir": "<확인 필요 — 현재 GUIDE_DIR 은 None, glob 패턴만 있음>",
    "genDir": "_딕테이션_생성기"
  },
  "patterns": {
    "storyboardFilename": "Lesson\\s*0*(\\d+)\\s*\\.xlsx$",
    "specialUnitFilename": "_([A-Za-z][A-Za-z ]*Lesson)\\s*\\.xlsx$",
    "contentsFolder": "^lesson0*(\\d+)$",
    "pageFilename": "^(p\\d{3}_\\d{2})\\.html$",
    "guidePdf": "*각론{unit}*.pdf",
    "soundSheet": "{unit}과"
  },
  "units": [
    {"id": "1", "name": "1단원",
     "storyboard": "01_스토리보드/.../Lesson 1.xlsx",
     "ops": "00_개발물/.../lesson01/ops", "sheet": "1과"},
    "... (2~8단원 동일 구조, project.json 실측값 그대로) ...",
    {"id": "special_lesson", "name": "Special Lesson",
     "storyboard": "01_스토리보드/.../Special Lesson.xlsx",
     "ops": "00_개발물/.../special_lesson/ops",
     "sheet": "SL",
     "guide": "03_PDF/3학년 지도서 각론 pdf/B1 (324-331) 각론9 중등영어지도서3년_ok.pdf",
     "kr": "guide"}
  ],
  "prototype": {
    "lesson": "3",
    "analyzedPages": ["p050_02"],
    "note": "3단원 1쪽만 승격됨. Think-About/마지막쪽 예외 등 6개 키는 아직 없음(정상 — 프로토에 없는 건 안 채워도 됨)",
    "rulesFile": "rules/cj_reading/rules.json"
  }
}
```

**확인 필요 표시 사유**
- `project.name`: project.json 최상위에 `"name": "2026_cj_midd3_eng"` 로 실제 존재함을 확인했으나,
  이 값이 사람이 의미부여한 "프로젝트 이름"인지 `os.path.basename(root)` 자동 생성값인지는
  코드상 후자로 확인됨(`project_io.put_units(rid, lst, name=os.path.basename(root))`) —
  즉 project_rules.json 에서는 "자동 생성값"이라고 명시하는 편이 정직함
- `guideDir`: 코드상 기본값은 `None`이고, 슬롯으로 채울 수 있으나 지금 settings.json 에는
  채워진 값이 없어 실제 운영값을 확인하지 못함

---

## 13. 요약과 다음 결정 필요 사항

1. **A1(read_import ↔ rules.json 연결)**: 가장 작고, 사용자가 이미 명시적으로 요청한 범위와
   정확히 일치합니다. 다음 단계로 바로 진행 가능한 후보입니다.
2. **A2(경로 하드코딩 이동)**: project_rules.json 스키마(12절)가 확정되어야 시작할 수 있습니다.
3. project_rules.json 과 rules/<recipe>/rules.json 을 별개 파일로 유지하는 안(9절)에
   동의하시는지 확인이 필요합니다 — 하나로 합칠 수도 있지만, 지금 코드 구조(recipe 별
   rules 폴더)와 제일 자연스럽게 맞는 쪽은 "분리 유지"입니다.
4. `GEN`(생성기 자기 위치, 4절)을 project_rules.json 에 넣을지, 지금처럼 로컬 계산으로
   둘지 — 의미가 달라(자료 위치가 아니라 프로그램 설치 위치) 판단이 필요합니다.

이 문서 전체는 분석과 계획이며, **코드는 전혀 수정하지 않았습니다.** 어느 단계부터
진행할지, 12절 스키마에 고칠 부분이 있는지 알려주시면 그 범위만 승인받은 대로 진행하겠습니다.
