// 미니 단어장 data-use="word"
var wordData = [
  {
    index: 1,
    wordArr: "path",
    wordMp3Arr: "media/mp3/3_143_word_01.mp3",
    wordClassArr: "명",
    wordMeanArr: "길",
    wordExEgArr: "There was a narrow <b>path</b> between the trees.",
    wordExMp3Arr: "media/mp3/path_ex.mp3",
    wordExKoArr: "나무들 사이에 좁은 길이 있었다."
  },
  {
    index: 2,
    wordArr: "deliver",
    wordMp3Arr: "media/mp3/3_143_word_02.mp3",
    wordClassArr: "동",
    wordMeanArr: "배달하다",
    wordExEgArr: "The man is <b>delivering</b> a package to the house.",
    wordExMp3Arr: "media/mp3/deliver_ex.mp3",
    wordExKoArr: "그 남자는 집에 택배를 배달하고 있다."
  },
  {
    index: 3,
    wordArr: "take on",
    wordMp3Arr: "media/mp3/3_143_word_03.mp3",
    wordClassArr: "",
    wordMeanArr: "(일 등을) 맡다",
    wordExEgArr: "She decided to <b>take on</b> the new project.",
    wordExMp3Arr: "media/mp3/take_on_ex.mp3",
    wordExKoArr: "그녀는 새로운 프로젝트를 맡기로 결심했다."
  },
  {
    index: 4,
    wordArr: "hint",
    wordMp3Arr: "media/mp3/3_143_word_04.mp3",
    wordClassArr: "명",
    wordMeanArr: "힌트, 암시",
    wordExEgArr: "She gave me a <b>hint</b> about the party.",
    wordExMp3Arr: "media/mp3/hint_ex.mp3",
    wordExKoArr: "그녀는 나에게 파티에 대한 힌트를 줬다."
  },
]

// 구문 해설 data-use="syntax"
var syntaxData = [
  {
    index: 1,
    syntaxArr: "A healthcare worker whose name was Hannah began using the bike.",
    syntaxMp3Arr: "media/mp3/3_143_read_01.mp3",
    syntaxCmtArr: "소유격 관계대명사 whose가 선행사 A healthcare worker와 whose 뒤의 명사 name을 연결해준다. using은 began의 목적어로 쓰인 동명사이다.",
  },
  {
    index: 2,
    syntaxArr: "She rode Big Red along small paths where cars couldn’t go, delivering medicines and bringing patients to the clinic.",
    syntaxMp3Arr: "media/mp3/3_143_read_02.mp3",
    syntaxCmtArr: "관계부사 where가 이끄는 절이 선행사 small paths를 수식한다. delivering ~과 bringing ~은 분사구문으로, rode와 동시에 일어난 동작을 나타낸다.",
  },
  {
    index: 3,
    syntaxArr: "She whispered “Thank you,” wondering where its journey had first begun.",
    syntaxMp3Arr: "media/mp3/3_143_read_05.mp3",
    syntaxCmtArr: "wondering ~은 동시 상황을 나타내는 분사구문이고, wondering 뒤에 <span class='cursiveB'>「</span>의문사+주어+동사<span class='cursiveB'>」</span> 어순의 간접의문문이 왔다. had begun은 <span class='cursiveB'>「</span>had+과거분사<span class='cursiveB'>」</span> 형태의 과거완료 시제로, 여정이 시작된 시점이 궁금해했던 시점보다 더 이전임을 보여준다.",
  },
  {
    index: 4,
    syntaxArr: "There was no hint that a girl had once ridden it to the market or that a boy had ridden it around a small town.",
    syntaxMp3Arr: "media/mp3/3_143_read_07.mp3",
    syntaxCmtArr: "<span class='cursiveB'>「</span>There was no+단수 명사 ~.<span class='cursiveB'>」</span>는 ‘~가 없었다.’라는 의미이다. or로 병렬 연결된 that절은 hint와 동격을 나타낸다. 각 that절의 had (once) ridden은 과거완료 시제이다.",
  },
]