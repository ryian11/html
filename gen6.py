# -*- coding: utf-8 -*-
"""(구버전) 엔진은 read_gen.py 로 옮겼습니다.

  python read_run.py 6     생성 → 측정 → 재생성 → 검증 (권장)
  python read_gen.py 6     생성만
"""
import sys
import read_gen

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print('※ gen6.py 는 read_gen.py 로 대체되었습니다. read_run.py 를 쓰세요.\n')
    read_gen.build(n)
