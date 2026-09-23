# prototype 을 project_rules.json 기준으로 — 구현 결과

요청하신 7개 항목 순서대로 보고합니다. 모든 테스트는 실제 `app.py` 서버를 띄워 HTTP로 확인했습니다.

---

## 1. 수정한 파일

| 파일 | 상태 |
|---|---|
| `project_rules_io.py` | 수정 (함수 2개 추가) |
| `recipes/cj_reading.py` | 수정 (함수 4개 수정 + 1개 신규) |
| `proto_scan.py` | 수정 (함수 2개) |
| `app.py` | 수정 (`_recipe_info()` 한 곳) |
| `app_page.py` | 수정 (프로토 단원 UI + 안내 문구) |
| `project_rules.json` | 데이터 추가 (`prototype.units` — 3·6·special_lesson 3개 단원, 실제 이미 분석에 쓰인 페이지 값 그대로) |

건드리지 않은 파일: `read_paths.py`, `read_gen.py`, `read_import.py`(자료 해석 로직), `rules_io.py`, `runner.py`, extract/build 파이프라인 — 말씀하신 범위 제한을 그대로 지켰습니다.

모든 수정 파일은 `_backup/코드/`에 이번 작업 시작 전 시점(`20260922_015655`)으로 백업돼 있습니다.

---

## 2. 수정한 함수 / 3. 변경 이유

| 파일 | 함수 | 무엇을 바꿨는지 | 왜 |
|---|---|---|---|
| `project_rules_io.py` | `proto_units()` (신규) | `project_rules.json["prototype"]["units"]` 를 그대로 돌려줌 | prototype 정보를 읽는 공용 창구가 필요했음 (전에는 아무도 안 부르는 죽은 `prototype()` 함수만 있었음) |
| 〃 | `proto_pages(unit_id)` (신규) | 그 단원 id 의 `pages` 배열만 돌려줌. 없으면 빈 목록 | 화면과 `analyze()` 가 "등록된 페이지만" 쓰도록 하는 단일 창구 |
| `recipes/cj_reading.py` | `proto_lesson(ctx)` | `int(v) if v.isdigit()` 강제 변환을 없앰. 대신 `PR.proto_units()` 의 id 목록에 있는지만 확인하고, 있으면 문자열 그대로 돌려줌 | 숫자 단원만 되던 제약(C-1)을 없애는 핵심 수정. 이제 `UnitA`/`special_lesson`/`Review` 등 어떤 문자열 id 도 그대로 통과함 |
| 〃 | `proto_ops(ctx)` | `out_dir(ctx,n)`→`read_paths.ops(n)` 경유를 그만두고, `read_paths.P.unit(n).get('ops')` 를 바로 읽음 | `read_paths.ops()` 안에는 "값이 없으면 `int(n)` 으로 CJ 식 폴더명을 만드는" 폴백이 있는데, 문자열 id 에서 그 폴백을 타면 예전엔 그대로 죽었음. 이번 prototype 흐름에서는 그 위험한 경로 자체를 안 타도록 우회함(=read_paths.py 는 손대지 않음, cj_reading.py 안에서만 회피) |
| 〃 | `proto_pages(ctx)` | `proto_scan.pages_in()` 폴더 재탐색을 없애고, `PR.proto_pages(id)` 값만 돌려줌 | project_rules.json 에 없는 페이지는 화면에 아예 안 보이게(요청 ③) 하는 핵심 수정 |
| 〃 | `analyze(ctx, pages)` | 이 단원의 시트 이름을 `P.unit(n)['sheet']`(최우선) → 없으면 `rules.json` 의 `sound.sheet`(숫자 단원일 때만 `%d` 적용) 순서로 미리 구해서 `proto_scan.scan(..., sound_sheet=…)` 에 건네줌 | `proto_scan.py` 가 시트 이름을 스스로 추측하지 않도록, project_rules.json 에 있는 값을 실제로 쓰게 만드는 연결 고리 |
| 〃 | `prototype_units(ctx)` (신규) | `PR.proto_units()` 의 id 목록만 돌려줌 | 화면 드롭다운이 쓸 후보 목록 |
| `proto_scan.py` | `scan_sound(xlsx, lesson, sheet=None)` | `'%d과' % int(lesson)` 무조건 실행을 없앰. `sheet` 인자를 받으면 그대로 쓰고, 안 받았을 때만(단독 실행 호환용) 단원 id 가 숫자인지 먼저 확인한 뒤 `%d과` 를 시도. 숫자가 아니면 크래시 대신 "시트 이름을 모릅니다" 오류를 돌려줌 | C-2 문제(`%d과` 하드코딩)의 원인 제거. 원칙 4(추측 대신 오류)를 지킴 |
| 〃 | `scan(...)` | `sound_sheet=None` 매개변수 추가, `scan_sound()` 로 그대로 전달. `sound.sheet` 규칙을 rules.json 에 적을 때 **단원 id 가 숫자일 때만** 적음(문자열 단원엔 항상 맞다고 할 수 없는 값이라 안 적고 notes 로만 설명) | 위 변경을 전달하는 통로 + "모르는 걸 아는 척 적어두지 않는다" 원칙 |
| `app.py` | `_recipe_info(rid)` | 응답에 `protoUnits`(문자열 id 목록) 필드 하나 추가 | 화면이 드롭다운을 그릴 재료 |
| `app_page.py` | `loadRecipe()` | "프로토 단원" 자유 입력 `<input>` 을 `<select id="sl_proto_lesson">` 로 교체(기존 "단원 고르기" `<select>` 와 같은 패턴, `R.protoUnits` 로 옵션을 채움) | 요청하신 "JSON → 드롭다운" 흐름 |
| 〃 | `loadProto()`/`protoChanged()`/`analyze()`/`promote()`/안내 문구 | "적어 주세요/적으면" → "골라 주세요/고르면" 으로 문구만 교체 | 자유 입력이 아니라 드롭다운이 됐으므로 |

**이번에 의도적으로 안 건드린 것** (범위 제한 그대로 준수): `read_paths.py` 의 `storyboard()`/`ops()`/`guide_pdf()` 폴백, `rules.json` 구조 전체, `extract`/`build` 파이프라인, `read_import.py` 의 자료 해석 로직.

---

## 4. 실제 데이터 흐름 (수정 후, 코드로 확인)

```
project_rules.json["prototype"]["units"]
  = [{"id":"3","pages":["p050_02"]},
     {"id":"6","pages":["p104_01","p104_02","p105_01","p106_01","p107_01"]},
     {"id":"special_lesson","pages":["p152_03"]}]      ← Claude 가 이미 분석에 쓰인 흔적
                                                           (rules/cj_reading/proto_L3.json,
                                                           proto_L6.json) 을 보고 그대로 옮김
        ↓
GET /api/recipe/cj_reading
  → cj_reading.py:prototype_units(ctx) → project_rules_io.proto_units() 의 id 만 뽑음
  → 응답에 "protoUnits": ["3","6","special_lesson"]
        ↓
화면 로딩(loadRecipe) — <select id="sl_proto_lesson"> 을 만들고
  단원 이름표는 기존 unitLabels 를 재사용해서 보여줌 (3단원/6단원/Special Lesson)
        ↓
사용자가 드롭다운에서 고름 (예: special_lesson)
        ↓
GET /api/proto?lesson=special_lesson
  → cj_reading.py:proto_pages(ctx)
      → proto_lesson(ctx) 가 'special_lesson' 이 project_rules.json 후보에 있는지 확인 → 통과
      → project_rules_io.proto_pages('special_lesson') → ['p152_03']  (폴더 재탐색 없음)
        ↓
화면 체크박스에 p152_03 하나만 나옴 (폴더에 실제로 있는 p153_01~p157_01 은 안 보임)
        ↓
[규칙 분석] → POST /api/analyze
  → analyze(ctx, ['p152_03'])
      → proto_ops(ctx) → read_paths.P.unit('special_lesson')['ops'] 를 바로 읽음
      → sheet = P.unit('special_lesson')['sheet']  → 'SL' (project_rules.json 에 이미 있던 값)
      → proto_scan.scan(..., sound_sheet='SL')
          → scan_sound(xlsx, 'special_lesson', sheet='SL') → 'SL' 시트를 그대로 열어 읽음
        ↓
rules/cj_reading/proto_Lspecial_lesson.json 저장 (26개 항목, sound.idPattern 등 정상 추출)
```

---

## 5. 기존 기능 테스트 결과

모두 실제 서버를 띄워 HTTP 로 확인했습니다.

| 테스트 | 결과 |
|---|---|
| `GET /api/recipe/cj_reading` → `protoUnits` | `["3","6","special_lesson"]` — 정상 |
| `GET /api/proto?lesson=3` | `pages: ["p050_02"]` — JSON 그대로, 폴더 재탐색 아님 |
| `GET /api/proto?lesson=6` | `pages`: 등록된 5개만 — 정상 |
| `GET /api/proto?lesson=special_lesson`(문자열 id) | `pages: ["p152_03"]`, `ops` 경로 정상 해석 — 크래시 없음 |
| `GET /api/proto?lesson=1`(prototype.units 에 없는 단원) | `pages: []` — 화면에서 숨겨짐 확인 |
| `POST /api/analyze` (special_lesson, 문자열 id로 실제 분석) | 정상 완료, 26항목, `sound.idPattern`/`sound.col.id` 등 정상 추출. 로그에 "sound.sheet 템플릿은 단원 id 가 숫자가 아니라 적어 두지 않았습니다" 정상 출력 |
| 숫자 단원(3, 6) 재분석 후 `proto_L3.json`/`proto_L6.json` 대조 | 시각(`made`) 차이와 `lesson` 필드의 `6`→`"6"`(정수→문자열) 표기 차이, `ops` 경로 표기(테스트가 리눅스 샌드박스에서 도는 탓에 실제 윈도 경로와 다르게 잡힘 — 오늘 앞서 발견한 것과 같은 종류의 테스트 환경 문제, 실제 윈도에서는 재현 안 됨) 외에는 **완전히 동일**. 뽑힌 규칙 항목(팝업 번호·이름 틀·음원 정보 등) 자체는 한 글자도 안 바뀜 |
| `POST /api/run` — 7·8단원 extract+build | 정상 완료, 기준본(`_기준본/cj_reading/7·8`)과 **바이트 단위로 완전히 동일** — extract/build 파이프라인은 이번 변경의 영향을 전혀 안 받음 |
| `GET /api/project` | 정상 (9개 단원) — 단원 편집 화면 그대로 동작 |

**정직하게 남겨두는 차이점 하나**: `proto_L<N>.json` 안의 `proto.lesson` 값이 이제 `6`(정수)이 아니라 `"6"`(문자열)으로 저장됩니다. `proto_lesson()`이 더는 int 로 바꾸지 않기 때문에 생기는, 의도된 부수 효과입니다. 이 값은 화면 표시(`분석 결과 — 6단원`)와 `promote()`/`compare()` 어디에서도 정수 연산에 쓰이지 않는다는 것을 코드로 확인했고, 실제로 `/api/promote`/`/api/compare` 도 정상 동작함을 확인했습니다.

---

## 6. 새 구조에서 문자열 단원 ID가 가능한지

**예, 실제로 확인했습니다.** `special_lesson`(숫자가 아닌 id)을 `project_rules.json["prototype"]["units"]` 에 등록하고,

- 드롭다운 후보 목록에 정상적으로 나타남
- `GET /api/proto?lesson=special_lesson` 이 정상적으로 ops 경로와 페이지 목록을 돌려줌
- `POST /api/analyze` 로 실제 분석을 끝까지 실행해 `proto_Lspecial_lesson.json` 을 성공적으로 만듦(음원 엑셀의 `SL` 시트를 정확히 찾아 읽음)

까지 전부 성공했습니다. `1`, `UnitA`, `Review` 같은 다른 어떤 문자열도 project_rules.json 의 `prototype.units` 에 등록되어 있고 `units[]` 에도 그 id 가 등록돼 있으면 똑같이 동작합니다.

---

## 7. prototype JSON에 없는 페이지가 실제로 UI에서 숨겨지는지

**예, 확인했습니다.** `special_lesson`의 실제 ops 폴더에는 `p152_03, p153_01, p154_01, p155_01, p156_01, p157_01` 6개 페이지가 있지만, `project_rules.json` 에는 `p152_03` 하나만 등록해 두었고 `GET /api/proto?lesson=special_lesson` 은 정확히 `["p152_03"]` 하나만 돌려줬습니다 — 나머지 5개는 폴더에 실제로 존재함에도 화면에 나타나지 않습니다.

또한 `1`단원처럼 `prototype.units` 자체에 등록돼 있지 않은 단원은 드롭다운에도 안 나오고, 혹시 URL 로 직접 요청해도(`lesson=1`) `pages: []` 로 막히는 것까지 확인했습니다 — 말씀하신 "개발자 모드가 아닌 일반 화면에서는 폴더 스캔 결과를 보여주지 않는다"는 기준을 그대로 만족합니다.

---

지금 상태는 CJ 프로젝트에서 지금까지 쓰던 3·6단원과 새로 확인한 special_lesson 세 개만 프로토 후보로 등록돼 있습니다. 다른 단원도 프로토로 쓰고 싶으시면 `project_rules.json`의 `prototype.units`에 `{id, pages}`만 추가해 주시면 됩니다 — 화면 드롭다운에는 등록해 둔 것만 나타납니다.
