// 미니 단어장 data-use="word"
var wordData = [
  {
    index: 1,
    wordArr: "healthcare",
    wordMp3Arr: "media/mp3/3_142_word_01.mp3",
    wordClassArr: "명",
    wordMeanArr: "보건 의료",
    wordExEgArr: "Doctors and nurses work in <b>healthcare</b>.",
    wordExMp3Arr: "media/mp3/healthcare_ex.mp3",
    wordExKoArr: "의사와 간호사는 보건 의료 분야에서 일한다."
  },
  {
    index: 2,
    wordArr: "clinic",
    wordMp3Arr: "media/mp3/3_142_word_02.mp3",
    wordClassArr: "명",
    wordMeanArr: "병원, 진료소",
    wordExEgArr: "The <b>clinic</b> is next to the park.",
    wordExMp3Arr: "media/mp3/clinic_ex.mp3",
    wordExKoArr: "병원은 공원 옆에 있다."
  },
  {
    index: 3,
    wordArr: "offer",
    wordMp3Arr: "media/mp3/3_142_word_03.mp3",
    wordClassArr: "동",
    wordMeanArr: "제공하다, 제안하다",
    wordExEgArr: "She <b>offered</b> her seat to an old man.",
    wordExMp3Arr: "media/mp3/offer_ex.mp3",
    wordExKoArr: "그녀는 노인에게 자리를 제공하였다."
  },
  {
    index: 4,
    wordArr: "pat",
    wordMp3Arr: "media/mp3/3_142_word_04.mp3",
    wordClassArr: "동",
    wordMeanArr: "토닥거리다, 쓰다듬다",
    wordExEgArr: "She <b>patted</b> the cat on the head.",
    wordExMp3Arr: "media/mp3/pat_ex.mp3",
    wordExKoArr: "그녀는 고양이의 머리를 토닥거렸다."
  },
  {
    index: 5,
    wordArr: "ambulance",
    wordMp3Arr: "media/mp3/3_142_word_05.mp3",
    wordClassArr: "명",
    wordMeanArr: "구급차",
    wordExEgArr: "The <b>ambulance</b> rushed to the hospital.",
    wordExMp3Arr: "media/mp3/ambulance_ex.mp3",
    wordExKoArr: "구급차가 병원으로 급히 달려갔다."
  },
  {
    index: 6,
    wordArr: "trailer",
    wordMp3Arr: "media/mp3/3_142_word_06.mp3",
    wordClassArr: "명",
    wordMeanArr: "트레일러(자전거, 자동차 등에 연결하여 짐이나 사람을 나르는 차량)",
    wordExEgArr: "The truck was pulling a large <b>trailer</b> full of boxes.",
    wordExMp3Arr: "media/mp3/trailer_ex.mp3",
    wordExKoArr: "트럭이 상자들로 가득 찬 큰 트레일러를 끌고 있었다."
  },
  {
    index: 7,
    wordArr: "stretcher",
    wordMp3Arr: "media/mp3/3_142_word_07.mp3",
    wordClassArr: "명",
    wordMeanArr: "(환자를 나르는) 들것",
    wordExEgArr: "Two men carried the patient on a <b>stretcher</b>.",
    wordExMp3Arr: "media/mp3/stretcher_ex.mp3",
    wordExKoArr: "두 남자가 들것으로 환자를 옮겼다."
  },
  {
    index: 8,
    wordArr: "safety belt",
    wordMp3Arr: "media/mp3/3_142_word_08.mp3",
    wordClassArr: "명",
    wordMeanArr: "안전벨트",
    wordExEgArr: "Always wear your <b>safety belt</b> in the car.",
    wordExMp3Arr: "media/mp3/safety_belt_ex.mp3",
    wordExKoArr: "차 안에서는 항상 안전벨트를 착용하세요."
  },
  {
    index: 9,
    wordArr: "patient",
    wordMp3Arr: "media/mp3/3_142_word_09.mp3",
    wordClassArr: "명",
    wordMeanArr: "환자",
    wordExEgArr: "The doctor is checking on the <b>patient</b>.",
    wordExMp3Arr: "media/mp3/patient_ex.mp3",
    wordExKoArr: "의사가 환자의 상태를 확인하고 있다."
  },
]

// 구문 해설 data-use="syntax"
var syntaxData = [
  {
    index: 1,
    syntaxArr: "She knew what to do.",
    syntaxMp3Arr: "media/mp3/3_142_read_04.mp3",
    syntaxCmtArr: "what to do는 <span class='cursiveB'>「</span>의문사+to부정사<span class='cursiveB'>」</span> 형태의 명사구로 knew의 목적어 역할을 하며, ‘무엇을 해야 할지’라는 의미를 나타낸다.",
  },
  {
    index: 2,
    syntaxArr: "That afternoon, she offered 5 Big Red to the clinic and felt proud that it would continue helping others.",
    syntaxMp3Arr: "media/mp3/XXX.mp3",
    syntaxCmtArr: "과거형 동사 offered와 felt는 and로 병렬 연결되어 있다. helping은 동사 continue는 목적어로 쓰인 동명사이다.",
  },
  {
    index: 3,
    syntaxArr: "At the clinic, the bike was turned into an ambulance by adding a trailer.",
    syntaxMp3Arr: "media/mp3/3_142_read_07.mp3",
    syntaxCmtArr: "was turned into는 ‘~(으)로 변형되었다’라는 의미의 수동태 표현이다. by는 ‘~함으로써’라는 의미로 쓰인 전치사이다.",
  },
]