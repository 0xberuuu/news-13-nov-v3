# The World in One Day — Friday 13 November 2026 (V3)

A make.fun `news-image-01` entry: one 1024x1024 image summing up the world's
news of Friday 13 November 2026.

## Concept

A numbered world atlas, not a newspaper front page. A world map carries 26
numbered pins at the places the news happened; a three-column index below the
map tells each story in one headline and one short factual line, keyed to the
same numbers. A lead banner carries the day's biggest story (the FAA
nationwide ground stop), and a legend cell counts the stories by region.

## How it is built

- `render.py` draws the whole image with PIL: hand-drawn simplified continent
  outlines, numbered pins (with leader lines where pins would overlap), and
  all text rendered crisply. Every story in it was verified against reporting
  published on 13 November 2026 (Reuters, AP, BLS, FAA, IAEA, IEA,
  Al Jazeera, Microsoft, Downdetector).
- `entry.png` is the rendered image (1024x1024, under 1 MiB).
- `main.py` (standard library only) copies `entry.png` to the output
  directory, so the entry runs with no network and produces identical bytes
  on every run.

## Stories (26)

1. FAA grounds all US flights (telecom outage) · 2. US producer prices jump
   (+0.3% m/m, +6.5% y/y) · 3. Nvidia chief quits · 4. Senate leadership
   fight · 5. Brooklyn collapse toll 8 · 6. Democrat wins Kansas · 7. $1.2bn
   crypto seizure · 8. Measles ruling awaited · 9. Pope Leo in Peru ·
   10. Europe joins Ukraine talks · 11. Storm Charles hits Portugal ·
   12. England beat Croatia · 13. US officer named in UK spy probe ·
   14. France pushes Russia sanctions · 15. Sudan army takes stronghold ·
   16. Sudan-Ethiopia expulsions · 17. China drills ring Taiwan · 18. IAEA
   loses sight of Iran site · 19. Four tankers hit in Hormuz · 20.
   Turkey-Qatar defence pact · 21. Gaza hospital strike kills 6 · 22. Yen
   slides past 160 · 23. IEA sees oil surplus · 24. Microsoft 365 goes down ·
   25. Chip curbs row (Megaspeed) · 26. Australia rout England.
