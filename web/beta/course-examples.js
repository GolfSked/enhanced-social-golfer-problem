// Illustrative course labels, rather than claims about actual clubs or bookings.
(() => {
  const examples = {
    en: ['8 November · Moruya', '9 November · Narooma', '10 November · Catalina', '11 November · Moruya'],
    ko: ['11월 8일 · 서울 골프장', '11월 9일 · 부산 골프장', '11월 10일 · 제주 골프장', '11월 11일 · 서울 골프장'],
    ja: ['11月8日 · 東京ゴルフ場', '11月9日 · 横浜ゴルフ場', '11月10日 · 箱根ゴルフ場', '11月11日 · 東京ゴルフ場'],
    sv: ['8 november · Stockholms golfbana', '9 november · Uppsalas golfbana', '10 november · Göteborgs golfbana', '11 november · Stockholms golfbana']
  };
  const notes = {
    en: 'Illustrative course names and tee times; these are examples, not bookings.',
    ko: '골프장 이름과 티타임은 사용 예시이며 실제 예약이 아닙니다.',
    ja: 'ゴルフ場名とティータイムは入力例です。実際の予約ではありません。',
    sv: 'Bannamn och starttider är exempel, inga bokningar.'
  };
  const picker = document.querySelector('#site-language');
  const code = document.querySelector('.sharing pre code');
  const link = document.querySelector('.sharing a[href*="round="]');
  if (!picker || !code || !link) return;
  const note = document.createElement('p');
  note.className = 'quiet';
  link.closest('p').after(note);
  function update() {
    const lang = picker.value;
    const courses = examples[lang] || examples.en;
    const times = ['11:35', '10:00', '11:26', '11:00'];
    const query = new URLSearchParams({lang});
    courses.forEach((course, i) => query.append('round', `${course}|${times[i]}`));
    link.href = 'four-round-schedule-explorer.html?' + query;
    code.textContent = `?round=${courses[0]}|${times[0]}&round=${courses[1]}|${times[1]}`;
    note.textContent = notes[lang] || notes.en;
  }
  picker.addEventListener('change', update);
  update();
})();
