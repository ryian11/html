# -*- coding: utf-8 -*-
"""Reading 본문 페이지 한 번에 만들기.

  python read_run.py 6              백업 → 생성 → 측정 → 재생성 → 검증
  python read_run.py 6 --no-measure  측정 건너뛰기 (있는 값 그대로 다시 생성)
  python read_run.py 6 --show        브라우저 창 띄워서 측정

lesson<NN>/ops 에 직접 씁니다. 덮어쓰기 전에 _backup/<날짜시각>/ 에 원본을 옮겨 둡니다.
"""
import os, sys, time, shutil
import read_paths as P
import read_gen, read_verify


def backup(n):
    ops = P.ops(n)
    read_gen.load_lesson(n)
    targets = []
    for page in read_gen.ORDER:
        targets += [page + '.html', 'css/%s.css' % page, 'js/%s.js' % page,
                    'popup/%s_kor1.html' % page]
    targets.append(read_gen.intro_page() + '.html')
    targets.append('popup/%s.html' % read_gen.all_popup())
    tp = read_gen.think_page()
    if tp:
        targets.append('popup/%s_think_ans1.html' % tp)

    exist = [t for t in targets if os.path.isfile(os.path.join(ops, t))]
    if not exist:
        print('[backup] 기존 파일 없음 — 건너뜀')
        return None
    dst = os.path.join(ops, '_backup', time.strftime('%Y%m%d_%H%M%S'))
    for t in exist:
        d = os.path.join(dst, t)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(ops, t), d)
    print('[backup] %d개 → %s' % (len(exist), dst))
    return dst


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    do_measure = '--no-measure' not in sys.argv
    show = '--show' in sys.argv

    print('=' * 60)
    print(' lesson%02d Reading 본문 페이지' % n)
    print(' 원고 :', P.storyboard(n))
    print(' 산출 :', P.ops(n))
    print('=' * 60)

    backup(n)

    print('\n[1/4] 생성')
    read_gen.build(n)

    if do_measure:
        print('\n[2/4] 측정')
        try:
            import read_measure
            read_measure.measure(n, headless=not show)
        except ImportError as e:
            print('  건너뜀 — playwright 가 없습니다 (%s)' % e)
            print('  설치:  pip install playwright && playwright install chromium')
            do_measure = False

        if do_measure:
            print('\n[3/4] 측정값 넣어 다시 생성')
            import importlib
            for m in ('scrolls%d' % n, 'krlayout%d' % n, 'popscroll%d' % n):
                if m in sys.modules:
                    importlib.reload(sys.modules[m])
            read_gen.build(n)
    else:
        print('\n[2-3/4] 측정 건너뜀')

    print('\n[4/4] 검증')
    good = read_verify.verify(n)

    print('\n' + '=' * 60)
    if good:
        print(' 끝. 실기에서 한 번 열어 배경 그림과 글 위치를 봐 주세요.')
        print(' 문단 위치가 안 맞으면 data%d.py 의 CSS_LAYOUT 만 고치고 다시 돌리면 됩니다.' % n)
    else:
        print(' 위 !! 항목을 확인하세요.')
    print('=' * 60)
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
