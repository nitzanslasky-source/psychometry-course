# Fresh-solve: combinatorics, probability, factorials, overlapping_sets, trial_and_error, generality (88 Qs)
All 88 solved; all match the key (one key questionable: 2024_spring_q1_17, see bottom).
Format: id · fastest route · taught?

## combinatorics (24)
2020_autumn_q1_16 · "exactly 2 coloured neighbours" with 4 squares = a 2x2 block; slide it in 4x4: 3x3=9 · NO (one-off, spatial)
2022_autumn_q1_16 · choose 4 of 5 = choose the 1 left out; total 15 odd, so leave out an odd one: 3 · YES t28 "choose who is left out"
2023_autumn_q1_04 · draws=10-3G -> 10,7,4,1; test choices: 10-d divisible by 3 · YES t21 "divisible by 3, eliminate"
2023_autumn_q2_01 · max: against=9 (less than 10) -> 10+3+9=22 · YES t21 min/max
2023_autumn_q2_07 · 3 of 4 = leave out 1: 4 · YES t28
2025_autumn_q1_03 · worst case 3+2+1 (last key still counts as a try) = 6 · YES t28 Q56 (keys/cupboards) + t20 worst luck
2020_spring_q1_01 · extreme: 11 countries 1 each, 19-11=8 · YES t21 "give the others the least"
2020_spring_q1_07 · 15+4-2=17 (inclusion-exclusion) · YES t29 card / t21 Q23
2021_spring_q2_16 · all minus same colour: 49-(8+10)=31 · YES t28 "all minus forbidden"
2023_spring_q1_05 · 3s>=7 -> s=3 · YES t28 multiply + t21 min
2024_spring_q1_05 · ends 5..5 -> 3 orders of 2,7,7; 7..7 -> 3; 2 impossible: 6 · YES t28 (identical items/forced digits)
2024_spring_q1_08 · overlap between 20+15-25=10 and 15 -> 13 · YES t24 Overlap Ranges
2024_spring_q2_17 · "at least": plug choices from the smallest; 26 no, 28 yes (6 left > 5.6) · YES t21 "smallest asked, plug smaller first"
2025_spring_q1_03 · list 28-shekel combos: 40,50,60 -> 70 impossible · YES t21 impossible totals
2025_spring_q1_08 · one vertex's colour fixes all (neighbours alternate) -> 2 · NO (one-off; forced-position idea in t28)
2026_spring_q2_20 · 3 kinds x 3 (none/storey/attic) x 2 (parking) =18 · YES t28 multiply (trap: 2 options for storey instead of 3 -> 12)
2019_winter_q1_14 · pigeonhole n people, n-1 countries · YES t20 pigeonhole
2019_winter_q2_05 · every price multiple of 3 -> total multiple of 3; 52 isn't · YES t21 "constant step / remainder"
2020_winter_q2_06 · C(4,2)=6 · YES t28 pairs table
2022_winter_q1_17 · other 8 prices & 6 colours need >=8 types -> 30-8=22 · YES t21 min/max (hard)
2022_winter_q2_18 · 2^3+2^6=72 · YES t28 repetition + separate cases add
2023_winter_q1_19 · small case: 100 boys make 100 gaps in circle; 101 girls -> one gap has 2 -> 99 · WEAK (t20 "count a small case"); one-off
2024_winter_q2_16 · 1 chocolate forced (2 >21); 2c+g=10, c=1..4 -> 4 · YES t21 list/forced
2025_winter_q1_02 · 5·4/2=10 · YES t28 mutual action

## probability (24)
2020_autumn_q2_17 · tree: 1/2·1/2+1/2·1/4=3/8 · YES t29 tree
2021_autumn_q1_03 · sums 0..3 -> 4 · YES t20 counting range
2022_autumn_q2_15 · only 9:00,10:00 in window -> 2 checks; 2·(1/3)(2/3)=4/9 · YES t29 "exactly k" (trap: 3 checks) 
2023_autumn_q1_14 · 1/2·2/3·…·6/7 cancels -> 1/7 · YES t29 Q20 cancelling
2024_autumn_q1_07 · Sunday 6 places × 6! (or 7!-6!) · YES t28
2024_autumn_q2_14 · first ball free, second different 2/3 · YES t29 "first pick doesn't matter"
2025_autumn_q2_16 · 5/6·1/6 · YES t29 (Q50 similar)
2019_spring_q1_04 · total=avg×count (language, mis-tagged) · YES t25
2019_spring_q2_13 · count ways: 1 vs 2 -> 1/2 · YES t29 dice table
2020_spring_q1_14 · which 2 remain: 1/C(5,2)=1/10 · YES t29 symmetry/t28 left out
2020_spring_q2_05 · total/(n+1) -> (2). Fast: plug y=x -> avg must stay x; only (2) · WEAK: y=x "do-nothing" check not taught as plug-in tip (t25 has the fact)
2020_spring_q2_16 · direct, or plug n=k=0 -> 80; only (2) · WEAK same
2023_spring_q1_17 · 16 outcomes, 3 good · YES
2024_spring_q2_20 · doll free; ball 1/7, whistle 1/7 · YES t29 first pick free
2025_spring_q1_20 · test choice 99 -> 66,66,99 avg 77 (mis-tagged averages) · YES t51 plug answers
2025_spring_q2_16 · 17/18: 3+1 of 216 -> 1/54 · YES
2026_spring_q1_02 · 5/15 · YES
2019_winter_q1_07 · 2 pairs/row ×4 rows ×2 orders=16 · YES t28 order matters (trap 8)
2019_winter_q2_19 · strictly increasing 6 dice forces 1..6: one outcome · YES t28 Q1 idea (trap 1/6!)
2020_winter_q1_18 · 21x=1 · YES t29 p18 style
2022_winter_q1_06 · Y gets 1/4+1/4, X 1/4 -> 2 (figure) · YES tree
2023_winter_q2_02 · (1/2)^n; plug n=1 then n=3 · YES
2024_winter_q1_16 · symmetry 1/3 · YES t29 symmetry ("three players")
2025_winter_q2_14 · symmetry: k chosen of n -> 2/9 · YES t29 Q11 lockers

## generality (20)
2021_autumn_q1_19 · look at B: only ONE road enters B -> cut it: 1 (figure) · NO specific (one-off; "look at the target end")
2021_autumn_q2_04 · 0.5·(1+2+4+8+16)=15.5 · YES t21 doubling sums
2022_autumn_q1_18 · extreme: one pile 15 forces others >=13 -> 54>50 · YES t21
2022_autumn_q2_10 · each sentence t+2t+2t=5t -> 300/5=60 · YES reading (trap 3t ->100, choice 1)
2019_spring_q1_15 · plug x=0 -> difference must be 0: only (3) · WEAK (t23 tip says "not 0")
2019_spring_q2_06 · 210t=840 or test choices · YES
2019_spring_q2_15 · geometric sum: 1 + (just under 1) -> between 1 and 2 · YES-ish t21/t8 (estimate)
2020_spring_q2_07 · net 4 moves -> diff changes by 8: |5-8|=3; or plug numbers · YES t1 "difference stays" / plug in
2021_spring_q1_11 · chain: butter->cans->sacks 700 · YES t22
2021_spring_q2_10 · per game: 2 (tie) to 4 (win) points ×50 · YES t21 min/max (per-unit)
2023_spring_q2_02 · 1/x+1/(2x)+1/(2x)=2/x=1 · YES
2023_spring_q2_10 · test choices: P=5 -> 6 wins ✓ · YES t51
2024_spring_q1_14 · 1+1/2+1/4+1/8 · YES
2024_spring_q1_17 · plug y=1: x^2=3+2√2 not integer -> (4). BUT y=0 breaks (4) — key questionable · YES t20
2024_spring_q2_03 · plug E=4,S=0 / E=6,S=2 · YES t20
2019_winter_q1_03 · P/2-P/3=P/6=150k, or test 900k · YES
2019_winter_q1_20 · 80-min cycle timeline; 10:00 is 60–90 min into cycle -> never at B · YES t21 cycles
2020_winter_q2_01 · 33/3=11 · YES (sum split evenly)
2022_winter_q1_19 · plug n=2,k=1 -> a: only (1) · YES t23/t51 plug numbers
2024_winter_q1_09 · 7n-2=8(n-1) -> 6, or test choices · YES

## factorials (12)
2020_autumn_q1_04 · 720=6! by sight · YES t28 card
2021_autumn_q2_05 · run of neighbours = x alone -> y=x-1 · YES
2022_autumn_q1_17 · 42=6·7 -> a=5 · YES t28 "run of neighbours"
2025_autumn_q1_17 · plug k=2: 8 -> only (2); or pair each factor with a 2 · YES t28 plug n=2
2021_spring_q1_05 · n vs n(n-1) vs n^2 · YES
2025_spring_q1_14 · 120=5!, (5!/6!)^2=1/36 · YES
2026_spring_q2_18 · =(n+1)(n-1)=n^2-1 -> 35 · YES (run of neighbours) 
2019_winter_q2_16 · primes in 8!; faster: 2^7 takes all 2s -> x odd -> 35 only odd choice · YES (primes in n!); parity shortcut one-off
2020_winter_q1_19 · take out 15!: 17·16·15!/(17·15!)=16 · YES t28 card
2022_winter_q2_07 · plug x=2 · YES
2024_winter_q2_17 · 8!(1+90)/2 · YES t28 card
2025_winter_q1_07 · 121!=121·120! -> x=11 · YES

## overlapping_sets (6)
2020_autumn_q1_11 · put all 100 children in classes (both) -> adults need only 20 soccer: 200-20=180 · YES t24 (hard; trap: treat classes as separate people -> 140/100)
2023_autumn_q2_20 · all-three <= pair overlap 10; can be 0 · YES t24 Three Groups
2024_autumn_q1_19 · count absences: 1+1+2=4 = number of lectures -> 0 · YES t24 Three Groups
2019_spring_q2_04 · 45+60-100=5, max 45 · YES t24
2020_winter_q1_14 · hidden total = 24 h: min 11+15-24=2 · WEAK (hidden total not warned)
2024_winter_q2_02 · union 10+20-5=25 -> 15 · YES t24

## trial_and_error (2)
2020_spring_q2_11 · 300·330≈99,000 -> 100,000 · YES t51 estimate
2021_spring_q1_04 · cheapest per litre is 1.5 L (4/L): 2×6=12 (table) · YES t21/t52 (unit price)
