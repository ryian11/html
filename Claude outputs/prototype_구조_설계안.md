# prototype 을 project_rules.json 기준으로 — 설계안 (코드 수정 전)

아직 코드는 손대지 않았습니다. 아래를 확인해 주시면 그 다음에 구현하겠습니다.

---

## A. 현재 prototype 데이터 흐름 (코드 기준 실측)

```
사용자가 화면 "프로토 단원" 칸에 숫자를 직접 타이핑  (app_page.py: <input id="sl_proto_lesson"> — 텍스트 입력, 목록 없음)
        ↓
recipes/cj_reading.py : proto_lesson(ctx)
    v = str(ctx.get('proto_lesson') or '').strip()
    return int(v) if v.isdigit() else None      ← 숫자가 아니면 무조건 포기
        ↓
recipes/cj_reading.py : proto_ops(ctx)
    ctx.get('proto_ops') 를 사용자가 따로 채웠으면 그걸 쓰고,
    아니면 out_dir(ctx, n) → read_paths.ops(n)
    (n 이 project_rules.json 의 등록된 단원이면 그 ops 경로를 바로 씀 — 이 경로 자체는 문제없음)
        ↓
GET /api/proto?lesson=N
    → cj_reading.py:proto_pages(ctx)
        → proto_scan.pages_in(ops, pattern)   ← ops 폴더를 다시 스캔해서 보여줄 후보를 만듦
                                                 (project_rules.json 에 "이 단원의 프로토 페이지는
                                                  이것" 이라는 기록이 없음 — 매번 폴더를 다시 훑음)
        ↓
사용자가 페이지 체크박스를 고르고 [규칙 분석]
        ↓
POST /api/analyze → runner.analyze → cj_reading.py:analyze(ctx, pages)
    n = proto_lesson(ctx)          ← 여기서 또 int 가 아니면 막힘
    sb = P.storyboard(n) / snd = P.SND
    proto_scan.scan(rid, n, ops, pages, sound_xlsx=snd, sb_xlsx=sb, page_pattern=pat)
        → proto_scan.py:scan_sound(xlsx, lesson)
              want = '%d과' % int(lesson)      ← project_rules.json 도 rules.json 도 안 보고
                                                  시트 이름을 직접 만듦 (project_rules.json 에
                                                  이미 있는 unit.sheet 값은 여기서 쓰이지 않음)
        ↓
rules/cj_reading/proto_L<N>.json 에 결과 저장
        ↓
[승격] → rules/cj_reading/rules.json 에 합침
```

**문제의 핵심**: project_rules.json 에는 "어떤 단원을, 어떤 페이지를 견본으로 쓸지"에 대한 기록이 전혀 없습니다. 매번 (1) 사용자가 번호를 손으로 입력하고, (2) Python 이 그 번호의 폴더를 다시 스캔해서 페이지 후보를 만들고, (3) 시트 이름은 코드가 `%d과` 로 직접 짐작합니다. 말씀하신 "Claude 최초 분석 결과를 JSON 에 기록 → 프로그램은 그걸 읽기만" 원칙에서 이 부분만 벗어나 있습니다.

---

## B. 변경 후 데이터 흐름 (제안)

```
Claude 최초 분석
    → 이미 분석에 쓰인 흔적(rules/cj_reading/proto_L3.json, proto_L6.json)과
      단원 등록부를 보고, "프로토로 쓸 만한 단원과 그 견본 페이지"를 확인
    → project_rules.json["prototype"]["units"] 에 기록
        ↓
GET /api/recipe/cj_reading
    → cj_reading.py 가 project_rules.json["prototype"]["units"] 를 읽어
      { id, pages } 목록을 내려줌 (이름표는 기존 units[] 의 unitLabels 를 그대로 재사용)
        ↓
화면 "프로토 단원" 칸 — 지금의 자유 입력란을 <select> 드롭다운으로 교체
    (기존 "단원 고르기" <select> 와 똑같은 방식, 새 UI 부품을 만들 필요 없음)
        ↓
사용자가 드롭다운에서 단원을 고름  (문자열 id — 3이든 special_lesson 이든 UnitA 든 그대로 통과)
        ↓
cj_reading.py : proto_pages(ctx)
    → project_rules.json["prototype"]["units"][그 id]["pages"] 를 1차 후보로 보여줌
    → proto_scan.pages_in(ops) 는 "폴더에 실제로 그 파일이 있는지 확인 + 후보에 없는
      새 파일이 있는지 참고 표시"하는 보조 역할로 내려감 (discover() 와 같은 원칙)
        ↓
[규칙 분석] → analyze(ctx, pages)
    → sheet 이름을 project_rules.json["units"][id]["sheet"] (없으면 rules.json 의
      sound.sheet) 에서 가져와 proto_scan.scan() 에 그대로 건네줌
    → proto_scan.py 는 이제 시트 이름을 스스로 만들지 않고 건네받은 값을 그대로 씀
        ↓
(이후는 지금과 동일 — rules/cj_reading/proto_L<N>.json 저장 → 승격)
```

---

## C. 최종 JSON 예시 (지금 CJ 프로젝트 실제 값 기준)

`rules/cj_reading/proto_L3.json`, `proto_L6.json` 을 직접 열어서 실제로 분석에 쓰인 페이지를 확인했습니다 — 지어낸 값이 아닙니다.

```json
{
  "schema": 1,
  "project": { "...": "기존과 동일, 생략" },
  "paths": { "...": "기존과 동일, 생략" },
  "patterns": { "...": "기존과 동일, 생략" },
  "units": [
    { "id": "1", "name": "1단원", "...": "기존과 동일" },
    { "id": "3", "name": "3단원", "...": "기존과 동일" },
    { "id": "6", "name": "6단원", "...": "기존과 동일" },
    "... (기존 units 배열, 그대로)"
  ],
  "prototype": {
    "units": [
      { "id": "3", "pages": ["p050_02"] },
      { "id": "6", "pages": ["p104_01", "p104_02", "p105_01", "p106_01", "p107_01"] }
    ]
  }
}
```

**일부러 이렇게 얇게 설계한 이유** (말씀하신 "규칙/구조"와 "원본 위치"를 구분하라는 원칙에 따른 것):

| 후보로 검토했던 필드 | 넣지 않기로 한 이유 |
|---|---|
| `unit_name` (프로토 항목에 이름 중복) | 이미 최상위 `units[].name` 에 있음. `id` 로만 연결하면 이름이 바뀌어도 한 곳만 고치면 됨(중복 데이터가 둘로 갈라져 어긋나는 사고를 막음) |
| 단원별 `storyboard`/`ops` 경로 (프로토 항목에 경로 중복) | 이미 최상위 `units[].ops` 에 있음. 같은 이유로 중복하지 않음 |
| 페이지별 `file` (전체 파일 경로) | `ops 경로 + pageId + ".html"` 로 완전히 계산되는 값이라(지금 코드가 실제로 그렇게 찾음), 따로 저장하면 나중에 ops 가 바뀌었을 때 둘이 어긋날 수 있음 |
| 페이지별 `order` (순서 번호) | 배열 안에서의 나열 순서 자체가 이미 순서를 의미함. 별도 숫자를 또 관리하면 배열 순서와 order 값이 어긋날 수 있음 |
| 페이지별 `type`("vocabulary" 등) | **proto_scan.py 가 이미 HTML 을 읽어서 그 쪽이 본문(body)인지 들머리(intro)인지 스스로 알아냅니다**(`scan_page()` 의 `kind` — 방금 proto_L6.json 에서 `info.pageKinds`: `intro: ["p104_01"]`, 나머지는 body 로 실제로 기록된 걸 확인했습니다). 이미 코드가 정확히 아는 사실을 JSON 에도 따로 적으면, 나중에 HTML 은 바뀌었는데 JSON 은 안 바뀌는 "둘이 다른 말을 하는" 상황이 생길 수 있습니다. 그래서 **type 은 넣지 않는 것을 제안**합니다. (다른 recipe 가 나중에 스스로 판별 못 하는 종류의 "type" 이 필요해지면, 그때 그 recipe 안에서 선택적 필드로 추가하면 됩니다 — 지금 당장 스키마에 넣어 둘 필요는 없어 보입니다)

남기는 건 정말로 "Claude 가 확인한, 코드가 계산으로 못 알아내는 사실" 두 가지뿐입니다 — **어느 단원을 프로토로 쓸지, 그 단원의 어느 페이지가 견본인지.**

---

## D. 수정 대상 파일

| 파일 | 함수 | 현재 역할 | 변경 이유 | 변경 방향 |
|---|---|---|---|---|
| `project_rules_io.py` | (신규) `proto_units()` | 없음 — `prototype()` 이 있지만 아무도 안 부름(죽은 코드) | prototype.units 를 읽는 공용 함수가 필요 | `d.get('prototype',{}).get('units') or []` 를 돌려주는 짧은 함수. 기존 `prototype()` 은 이 함수로 대체하거나 그대로 두고 안 씀 |
| `recipes/cj_reading.py` | `proto_lesson(ctx)` | 문자열을 int 로 강제 변환, 숫자 아니면 None | C-1 문제의 원인. prototype 후보가 이제 project_rules.json 에 있으므로 int 변환이 필요 없어짐 | int 캐스팅을 없애고, `ctx.get('proto_lesson')` 값을 그대로 문자열 id 로 씀. `PR.proto_units()` 의 id 목록에 있는지만 확인 |
| 〃 | `proto_ops(ctx)` | `out_dir(ctx, n)` → `read_paths.ops(n)` 경유(문제 없었음, 그대로 둬도 됨) | 이미 등록된 단원의 ops 를 바로 찾는 구조라 큰 변경 불필요 | 문자열 id 를 그대로 받도록만 확인 (실질적 로직 변경 최소) |
| 〃 | `proto_pages(ctx)` | 매번 `proto_scan.pages_in(ops)` 로 폴더를 다시 스캔해 후보를 만듦 | project_rules.json 의 기록을 1차로, 폴더 스캔은 보조로 바꿔야 함 | `PR.proto_units()` 에서 그 id 의 `pages` 를 1차로 쓰고, `pages_in()` 결과와 견줘 "후보에 없는 새 파일"이 있으면 notes 로만 알려줌(발견은 하되 강제로 추가하지 않음 — discover() 와 같은 원칙) |
| 〃 | `analyze(ctx, pages)` | `P.SND` 만 건네고 시트 이름은 proto_scan 내부가 결정 | C-2 문제 해결에 필요 | 이 단원의 sheet 이름(`unit dict['sheet']` 또는 rules.json 의 `sound.sheet`)을 미리 구해서 `proto_scan.scan(..., sound_sheet=sheet)` 처럼 건네줌 |
| 〃 | (신규) `prototype_units(ctx)` | 없음 | 화면 드롭다운에 넘겨줄 "프로토 후보 단원" 목록이 필요 | `PR.proto_units()` 의 id 목록을 돌려줌 (이름표는 기존 `unit_labels(ctx)` 그대로 재사용) |
| `proto_scan.py` | `scan_sound(xlsx, lesson)` | 내부에서 `'%d과' % int(lesson)` 로 시트 이름을 직접 만듦 | C-2 의 원인 그 자체 | `lesson` 대신(또는 추가로) `sheet` 인자를 받아, 있으면 그 값을 그대로 쓰고 없을 때만 `'%d과' % lesson` 기본값으로 (기존 단독 실행 `python proto_scan.py cj_reading 6 ...` 호환 유지) |
| 〃 | `scan(rid, lesson, ops, pages, ..., page_pattern=None)` | 시그니처에 시트 이름을 받을 자리가 없음 | 위 변경을 전달하려면 필요 | `sound_sheet=None` 매개변수 추가, `scan_sound()` 로 그대로 넘김 |
| `app.py` | `_recipe_info(rid)` | `units`/`unitLabels` 만 내려줌 | 화면이 프로토 드롭다운을 그리려면 후보 id 목록이 필요 | 응답에 `protoUnits`(id 목록) 필드 하나 추가 — 이름표는 기존 `unitLabels` 재사용하면 되므로 새 이름표 목록은 안 만들어도 됨 |
| 〃 | `_proto_info(rid, lesson)` | `lesson` 을 그대로 문자열로 다룸(이미 int 변환 없음 — 여기는 문제 없었음) | 큰 변경 불필요 | 그대로 둠 |
| `app_page.py` | `#pslots` 렌더링(252번째 줄) | `proto_lesson` 을 텍스트 `<input>` 으로 그림 | 자유 입력 → 드롭다운으로 바꿔야 함(말씀하신 목표) | 이미 있는 `#unit` `<select>` 만드는 코드(254~256번째 줄)와 똑같은 패턴으로, `R.protoUnits` 를 옵션으로 하는 `<select id="sl_proto_lesson">` 를 새로 그림. 그 아래 `onchange`/`protoChanged()` 연결은 기존 코드 재사용 |

**이번에는 손대지 않는 것** (말씀하신 6번 제약 그대로 지킴):
- `read_paths.py` 의 storyboard()/ops()/guide_pdf() 폴백 — 이번 prototype 구조와 직접 충돌하지 않으므로 그대로 둠
- rules.json 구조·`R()`/`load_rules()` 패턴 — 그대로 둠
- extract/build 파이프라인 — 전혀 안 건드림
- CJ fallback(LEGACY_PATHS 등) 전체 제거 — 안 함

---

## E. 기존 기능 영향

| 기능 | 영향 |
|---|---|
| **prototype 분석** | 흐름만 "번호 직접 입력" → "드롭다운 선택"으로 바뀝니다. 분석 로직(`scan_page`/`scan_css`/`scan_sound`/`scan_storyboard`) 자체는 그대로라 결과물(생성 규칙)은 동일합니다. 지금 CJ 프로젝트(3·6단원, 숫자 id)는 동작이 바뀌지 않고, 문자 id 밖에 없는 새 프로젝트에서 비로소 이 기능이 쓸 수 있게 됩니다 |
| **페이지 선택** | 체크박스 UI 자체는 그대로입니다. 다만 "기본으로 체크되어 보이는 후보"가 폴더 전체 스캔에서 project_rules.json 기록으로 바뀝니다 — 폴더에는 있지만 JSON 후보에 없는 페이지는 "참고" 취급으로 빠질 수 있는데, 이 UX 디테일(안내 문구를 어떻게 보여줄지)은 구현 전에 한 번 더 확인받고 싶습니다 |
| **HTML 생성(extract/build)** | 전혀 무관 — prototype 은 애초에 "본 생성과 따로 도는" 기능이라는 원칙(`PROTO = True` 주석)이 그대로 유지됩니다. extract/build 코드는 이번 변경에서 한 줄도 안 건드립니다 |
| **preview** | 무관 — 생성 결과물을 보여주는 기능이라 이번 변경과 관계없습니다 |
| **popup / CSS / JS** | 무관 — `proto_scan.py` 가 팝업 번호·파일이름 틀을 뽑는 로직(`scan_page`/`scan_css`) 자체는 안 건드리므로, 뽑히는 규칙의 내용은 지금과 동일합니다 |
| **rules.json 승격(promote)** | 무관 — `rules_io.promote()` 는 이번 변경과 완전히 분리되어 있습니다 |

---

확인해 주실 부분을 정리하면:
1. **C 의 JSON 구조**(unit_name/file/order/type 을 안 넣고, id + pages 만 남기는 방향)에 동의하시는지
2. **D 표의 파일별 변경 방향**이 맞는지, 빠진 게 있는지
3. **E 의 "폴더에는 있는데 JSON 후보에는 없는 페이지" 처리 방식**(참고로만 보여줄지, 아예 안 보여줄지)

여기까지 확인해 주시면 코드 수정에 들어가겠습니다.
