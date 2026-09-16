() => [...document.querySelectorAll('.tabContent')].map(t => {
  const box = t.querySelector('.scrollBox');
  const br = box.getBoundingClientRect();
  const o = box.scrollTop - br.top;
  const paras = [...t.querySelectorAll('.Paragraph')];
  const boxes = [...t.querySelectorAll('.scriptBox')];
  const hasSpk = t.querySelectorAll('.Speaker').length > 0;
  return {
    scrollH: box.scrollHeight, boxH: box.clientHeight, hasSpk: hasSpk,
    items: [...t.querySelectorAll('.scriptTarget')].map(el => {
      const rs = [...el.getClientRects()];
      let top = Math.min(...rs.map(r => r.top));
      let bot = Math.max(...rs.map(r => r.bottom));
      el.querySelectorAll('.inputBox').forEach(ib => {
        const r2 = ib.getBoundingClientRect();
        top = Math.min(top, r2.top);
        bot = Math.max(bot, r2.bottom);
      });
      let pi = 0; paras.forEach((p, k) => { if (p.contains(el)) pi = k; });
      let bi = 0; boxes.forEach((p, k) => { if (p.contains(el)) bi = k; });
      return { top: Math.round(top + o), bot: Math.round(bot + o), para: pi, box: bi };
    })
  };
})
