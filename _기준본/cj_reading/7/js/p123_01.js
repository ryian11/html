// 미니 단어장 data-use="word"
var wordData = [
  {
    index: 1,
    wordArr: "court",
    wordMp3Arr: "media/mp3/3_123_word_01.mp3",
    wordClassArr: "명",
    wordMeanArr: "(테니스 등의) 코트, 경기장",
    wordExEgArr: "They played tennis on the <b>court</b>.",
    wordExMp3Arr: "media/mp3/court_ex.mp3",
    wordExKoArr: "그들은 코트에서 테니스를 쳤다."
  },
  {
    index: 2,
    wordArr: "ant",
    wordMp3Arr: "media/mp3/3_123_word_02.mp3",
    wordClassArr: "명",
    wordMeanArr: "개미",
    wordExEgArr: "A group of <b>ants</b> is walking in a line.",
    wordExMp3Arr: "media/mp3/ant_ex.mp3",
    wordExKoArr: "한 무리의 개미들이 줄을 지어 걷고 있다."
  },
  {
    index: 3,
    wordArr: "deep",
    wordMp3Arr: "media/mp3/3_123_word_03.mp3",
    wordClassArr: "부",
    wordMeanArr: "깊게",
    wordExEgArr: "He dived <b>deep</b> into the ocean.",
    wordExMp3Arr: "media/mp3/deep_ex.mp3",
    wordExKoArr: "그는 바다 속 깊게 잠수했다.",

    wordClassArr2: "형",
    wordMeanArr2: "깊은"
  },
  {
    index: 4,
    wordArr: "golden",
    wordMp3Arr: "media/mp3/3_123_word_04.mp3",
    wordClassArr: "형",
    wordMeanArr: "금빛의, 금의",
    wordExEgArr: "He has <b>golden</b> hair and bright blue eyes.",
    wordExMp3Arr: "media/mp3/golden_ex.mp3",
    wordExKoArr: "그는 금빛 머리카락과 밝은 파란색 눈을 가졌다."
  },
  {
    index: 5,
    wordArr: "fit into",
    wordMp3Arr: "media/mp3/3_123_word_05.mp3",
    wordClassArr: "",
    wordMeanArr: "~에 꼭 들어맞다",
    wordExEgArr: "The key <b>fits into</b> the lock perfectly.",
    wordExMp3Arr: "media/mp3/fit_into_ex.mp3",
    wordExKoArr: "열쇠가 자물쇠에 꼭 들어맞는다."
  },
  {
    index: 6,
    wordArr: "million",
    wordMp3Arr: "media/mp3/3_123_word_06.mp3",
    wordClassArr: "명",
    wordMeanArr: "100만",
    wordExEgArr: "Over a <b>million</b> people visited the museum last year.",
    wordExMp3Arr: "media/mp3/million_ex.mp3",
    wordExKoArr: "작년에 100만 명이 넘는 사람들이 그 박물관을 방문했다."
  },
  {
    index: 7,
    wordArr: "final",
    wordMp3Arr: "media/mp3/3_123_word_07.mp3",
    wordClassArr: "형",
    wordMeanArr: "마지막의, 최종의",
    wordExEgArr: "I'm reading the <b>final</b> page of this book.",
    wordExMp3Arr: "media/mp3/final_ex.mp3",
    wordExKoArr: "나는 이 책의 마지막 페이지를 읽고 있다."
  },
  {
    index: 8,
    wordArr: "unfold",
    wordMp3Arr: "media/mp3/3_123_word_08.mp3",
    wordClassArr: "동",
    wordMeanArr: "펼치다",
    wordExEgArr: "He <b>unfolds</b> the map on the table.",
    wordExMp3Arr: "media/mp3/unfold_ex.mp3",
    wordExKoArr: "그는 탁자 위에 지도를 펼친다."
  },
  {
    index: 9,
    wordArr: "piece by piece",
    wordMp3Arr: "media/mp3/3_123_word_09.mp3",
    wordClassArr: "",
    wordMeanArr: "조금씩, 천천히",
    wordExEgArr: "They solved the puzzle <b>piece by piece</b>.",
    wordExMp3Arr: "media/mp3/piece_by_piece_ex.mp3",
    wordExKoArr: "그들은 조금씩 퍼즐을 풀었다."
  },
  {
    index: 10,
    wordArr: "bloom",
    wordMp3Arr: "media/mp3/3_123_word_10.mp3",
    wordClassArr: "동",
    wordMeanArr: "(꽃이) 피다",
    wordExEgArr: "The roses <b>bloom</b> along the fence.",
    wordExMp3Arr: "media/mp3/bloom_ex.mp3",
    wordExKoArr: "장미가 울타리를 따라 핀다."
  },
]

// 구문 해설 data-use="syntax"
var syntaxData = [
  {
    index: 1,
    syntaxArr: "It’s as wide as a tennis court and as tall as a three- story building.",
    syntaxMp3Arr: "media/mp3/3_123_read_03.mp3",
    syntaxCmtArr: "<span class='cursiveB'>「</span>as+형용사/부사의 원급+as ~<span class='cursiveB'>」</span>는 ‘~만큼 …한/하게’라는 의미의 동급 비교 구문이다. 두 구문 모두 It’s와 연결되어 망원경의 크기를 비교해 주고 있다.",
  },
  {
    index: 2,
    syntaxArr: "If a person stood next to the telescope, the person would look like a tiny ant.",
    syntaxMp3Arr: "media/mp3/3_123_read_04.mp3",
    syntaxCmtArr: "현재와 반대되는 상황을 가정하는 가정법 과거는 <span class='cursiveB'>「</span>If+주어+동사의 과거형 ~, 주어+조동사의 과거형(would, could might 등)+동사원형 ….<span class='cursiveB'>」</span>의 형태로 쓴다.",
  },
  {
    index: 3,
    syntaxArr: "The JWST was folded twelve times so that it could fit into a space rocket.",
    syntaxMp3Arr: "media/mp3/3_123_read_08.mp3",
    syntaxCmtArr: "so that은 ‘~하기 위해, ~할 수 있도록’이라는 의미로 뒤에 <span class='cursiveB'>「</span>주어+동사 ~<span class='cursiveB'>」</span>의 절이 오며 앞에 나온 주절의 목적을 표현한다.",
  },
  {
    index: 4,
    syntaxArr: "After the JWST was launched, it spent about a month traveling to its final location.",
    syntaxMp3Arr: "media/mp3/3_123_read_10.mp3",
    syntaxCmtArr: "주절의 it은 앞에 나온 JWST를 가리킨다. spent는 spend의 과거형이고 <span class='cursiveB'>「</span>spend+목적어(시간)+-ing<span class='cursiveB'>」</span>는 ‘~하는 데 …의 시간을 보내다’라는 의미이다. its는 it의 소유격이다.",
  },
]