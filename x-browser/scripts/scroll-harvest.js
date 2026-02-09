(async()=>{
  const collected = new Map();
  function harvest() {
    for (const a of document.querySelectorAll("article")) {
      const time = a.querySelector("time");
      if (!time) continue;
      const link = time.closest("a")?.href || "";
      if (collected.has(link)) continue;
      const un = a.querySelector('[data-testid="User-Name"]')?.innerText?.split("\n") || [];
      const tt = a.querySelector('[data-testid="tweetText"]')?.innerText || "";
      collected.set(link, {
        author: un[0] || "",
        handle: un[1] || "",
        date: (time.getAttribute("datetime")||"").split("T")[0],
        text: tt.substring(0, 280),
        url: link
      });
    }
  }
  harvest();
  for (let i = 0; i < 10; i++) {
    window.scrollBy(0, 2000);
    await new Promise(r => setTimeout(r, 600));
    harvest();
  }
  return JSON.stringify({total: collected.size, tweets: [...collected.values()]}, null, 2);
})()
