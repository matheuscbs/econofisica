# Lab 01 — Leitura dos resultados

Parâmetros: \(S_0=100\), \(\mu=0{,}08\), \(\sigma=0{,}02\), \(T=1\), `nsteps=252`, `seed=42`.

## Teoria

| Quantidade | Valor |
|------------|------:|
| \(m = \ln S_0 + (\mu-\tfrac12\sigma^2)T\) | 4.68497 |
| \(v = \sigma^2 T\) | 0.00040 (std 0.02) |
| \(\mathbb{E}[S_T] = S_0 e^{\mu T}\) | **108.329** |
| \(\mathrm{Var}(S_T)\) | **4.695** |

Com \(\sigma=0{,}02\) o túnel é estreito: quase toda a massa de \(S_T\) fica perto de ~108. A pdf em \(s=108\) domina; em 80 ou 120 é praticamente zero — coerente com vol baixa.

## Monte Carlo (subamostras aninhadas)

| N | mean empírica | \|err mean\| | var empírica | \|err var\| |
|--:|-------------:|-------------:|-------------:|-----------:|
| 1 000 | 108.329 | 0.0006 | 4.701 | 0.006 |
| 10 000 | 108.348 | 0.019 | 4.697 | 0.002 |
| 100 000 | 108.332 | 0.003 | 4.716 | 0.021 |

### Como ler

1. **A média já está correta na ordem de centavos** mesmo com N=1 000 — o estimador de média sob GBM é estável com vol baixa.
2. **Erros não caem de forma monótona a cada linha** (sorte amostral). A lei útil é \(\mathrm{erro}\sim 1/\sqrt{N}\) *em tendência*; por isso a cena Manim plota vários N e a reta \(1/\sqrt{N}\).
3. **Variância amostral (`ddof=1`) converge mais devagar** que a média — segundo momento precisa de mais amostras.
4. **Histograma vs pdf**: com N=100 000 a forma log-normal fica nítida; com N=1 000 ainda “pixelada”.

## Figuras estáticas

Geradas por `run_lab.py --plot` em `outputs/lab-m01-gbm-monte-carlo/` (gitignored):

- `gbm_paths.png` — envelope das trajetórias  
- `gbm_ST_density.png` — histograma + pdf  
- `gbm_mc_convergence.png` — erro vs N  

## Animações Manim

Ver `manim/README.md`. Use \(\sigma=0{,}20\) nas cenas de path para o túnel ficar visível; a convergência MC usa \(\sigma=0{,}02\) do lab.
