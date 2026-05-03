# Assignment 2 — Notas

## Step 2

### Ex. 1 e 2 — naive hashing com input simples

Inputs: `step_2/input` = `up202509273` · `step_2/input2` = `test`.

- **Ex. 1**: ambos os terminais com `input`. Output: "Found 1 intersecting elements: up202509273". Hashes "my" e "partner" iguais (`478ed603b634`). Screenshot: `screenshots/Screenshot From 2026-04-16 11-46-17.png`.
- **Ex. 2**: `input` vs `input2`. Output: "Found 0 intersecting elements". Hashes diferentes. Screenshot: `screenshots/Screenshot From 2026-04-16 11-51-28.png`.
- Verificação manual: `echo -n up202509273 | sha256sum | cut -c -12` → `478ed603b634` (confirma sha256 truncado a 6 bytes). Screenshot: `screenshots/Screenshot From 2026-04-16 12-04-26.png`.

### Ex. 3 — inspecção dos pacotes naive (verificação dos hashes)

Inputs: `step_2/input` = `up202509273`; `step_2/input2` = `test`.

Hashes esperados (sha256 truncado a 6 bytes):

- `up202509273` → `478ed603b634`
- `test` → `9f86d081884c`

Capturas:

- `step_2/3.1.pcapng` — ambos os terminais com `input`. 35 pacotes, 3 968 bytes. Hash `478ed603b634` aparece 2× (um pacote em cada direção, port 7766) → intersecção encontrada.
- `step_2/3.2.pcapng` — `input` vs `input2`. 30 pacotes, 3 508 bytes. Cada hash aparece 1× em direções opostas → sem intersecção, confirma que só os hashes truncados são trocados.

### Ex. 5 — Naive hashing (-p 0) com AppList1.csv vs AppList2.csv

Intersecção (5 elementos):

- com.whatsapp
- org.meowcat.edxposed.manager
- com.google.android.apps.maps
- com.android.chrome
- com.delaware.empark

Captura (`step_2/5.pcapng`):

- Pacotes: 31
- Total capturado: 4016 bytes (data: 2613 bytes)

### Ex. 6 — Server-aided (-p 1)

Bug do protocolo: as listas têm de ter o mesmo tamanho. AppList2 (34) foi paddada para 36 linhas com 2 emails fake de `emails_alice.txt` (`step_2/AppList{1,2}_padded.csv`).

Intersecção (mesmos 5 elementos do ex. 5) — `step_2/server_aided_intersection.txt`.

Captura (`step_2/6.pcapng`):

- Pacotes: 32
- Total capturado: 4768 bytes (data: 3330 bytes)

### Ex. 8 — Diffie-Hellman PSI (-p 2)

Intersecção (mesmos 5 elementos) — `step_2/dh_intersection.txt`.

Captura (`step_2/8.pcapng`):

- Pacotes: 30
- Total capturado: 7084 bytes (data: 5714 bytes)

### Ex. 9 — OT-based PSI (-p 3)

Intersecção (mesmos 5 elementos) — `step_2/ot_intersection.txt`.

Captura (`step_2/9.pcapng`):

- Pacotes: 36
- Total capturado: 56580 bytes (data: 55006 bytes)

### Ex. 10 — Comparação (segurança vs custo de comunicação)

| Protocolo | Pacotes | Bytes capturados |
|---|---|---|
| Naive hashing (-p 0) | 31 | 4 016 |
| Server-aided (-p 1) | 32 | 4 768 |
| Diffie-Hellman (-p 2) | 30 | 7 084 |
| OT-based (-p 3) | 36 | 56 580 |

## Step 3 — Benchmarks (psi.exe, -b 16)

Script: `step_3/bench.sh` · resultados: `step_3/results.csv` · plots: `step_3/time_vs_n.png`, `step_3/data_vs_n.png`.

Tamanhos testados: 50, 100, 500, 1 000, 5 000, 10 000, 50 000, 100 000.

| Protocolo | n | tempo (s) | sent (MB) | recv (MB) | total (MB) |
|---|---:|---:|---:|---:|---:|
| Naive (0) | 50 | 0.0 | 0.0 | 0.0 | 0.0 |
| Naive (0) | 100 | 0.0 | 0.0 | 0.0 | 0.0 |
| Naive (0) | 500 | 0.0 | 0.0 | 0.0 | 0.0 |
| Naive (0) | 1 000 | 0.0 | 0.0 | 0.0 | 0.0 |
| Naive (0) | 5 000 | 0.0 | 0.0 | 0.0 | 0.0 |
| Naive (0) | 10 000 | 0.0 | 0.1 | 0.1 | 0.2 |
| Naive (0) | 50 000 | 0.1 | 0.4 | 0.4 | 0.8 |
| Naive (0) | 100 000 | 0.3 | 1.0 | 1.0 | 2.0 |
| DH (2) | 50 | 0.0 | 0.0 | 0.0 | 0.0 |
| DH (2) | 100 | 0.0 | 0.0 | 0.0 | 0.0 |
| DH (2) | 500 | 0.2 | 0.0 | 0.0 | 0.0 |
| DH (2) | 1 000 | 0.4 | 0.0 | 0.1 | 0.1 |
| DH (2) | 5 000 | 2.1 | 0.2 | 0.3 | 0.5 |
| DH (2) | 10 000 | 4.3 | 0.4 | 0.7 | 1.1 |
| DH (2) | 50 000 | 22.2 | 1.8 | 3.3 | 5.1 |
| DH (2) | 100 000 | 44.6 | 3.5 | 6.6 | 10.1 |
| OT (3) | 50 | 0.2 | 0.0 | 0.0 | 0.0 |
| OT (3) | 100 | 0.2 | 0.0 | 0.0 | 0.0 |
| OT (3) | 500 | 0.2 | 0.1 | 0.0 | 0.1 |
| OT (3) | 1 000 | 0.2 | 0.1 | 0.0 | 0.1 |
| OT (3) | 5 000 | 0.2 | 0.4 | 0.1 | 0.5 |
| OT (3) | 10 000 | 0.2 | 0.8 | 0.3 | 1.1 |
| OT (3) | 50 000 | 0.3 | 3.7 | 1.3 | 5.0 |
| OT (3) | 100 000 | 0.4 | 7.3 | 2.9 | 10.2 |

Observações rápidas:
- **Naive**: mais rápido e menos comunicação, mas inseguro.
- **DH**: pouca comunicação mas tempo cresce muito (exponenciações por elemento → ~45 s para 100k).
- **OT**: tempo quase constante (overhead inicial dominante), mas mais dados trocados — escala bem em CPU.

## Step 4 — PSI sobre Liked Songs do Spotify (Artur vs Tiago)

Caso de uso real com partner: cada lado exporta as suas Liked Songs do Spotify (`step_4/Liked_Songs_Artur.csv`, `step_4/Liked_Songs_Tiago.csv`) e queremos descobrir as músicas em comum sem revelar o resto da biblioteca.

`step_4/extract_tracks.py` extrai o ID de 22 chars do `Track URI` (`spotify:track:<id>`), um por linha. As listas têm tamanhos diferentes (Artur: 579, Tiago: 601) e o protocolo exige n igual nos dois lados (mesmo bug do step 2 ex 6), por isso a Artur foi paddada para 601 com 22 IDs fake aleatórios prefixados com `FAKE`.

Protocolo: **OT-based (-p 3)** com `demo.exe -f`, consistente com o critério do step 3 para n na ordem das centenas/milhares.

Comandos:

```bash
python3 extract_tracks.py --in Liked_Songs_Artur.csv --out artur_ids.txt --pad-to 601
python3 extract_tracks.py --in Liked_Songs_Tiago.csv --out tiago_ids.txt --pad-to 601
# terminal 1: ./demo.exe -r 0 -p 3 -f artur_ids.txt
# terminal 2: ./demo.exe -r 1 -p 3 -f tiago_ids.txt
```

Resultado (`step_4/result_spotify.txt`): **2 elementos intersectados**, validados contra `comm -12` em plaintext (`step_4/plaintext_intersection.txt`):

- `4nKRZAONxGgcKCMin730Ai` — *33 Max Verstappen* (Carte Blanq; Nils Van Zandt; Maxx Power)
- `63T7DJ1AFDD6Bn8VzG6JE8` — *Paint It, Black* (The Rolling Stones)

Privacidade: cada parte só aprende as 2 músicas em comum; as restantes ~577 e ~599 ficam privadas. Os IDs `FAKE...` do padding nunca colidem com IDs base62 reais.
