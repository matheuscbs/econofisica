"""
Animações Manim — Lab 01 GBM + Monte Carlo (@mosscardoso / econofisica)

Render (na raiz do repo, com .venv ativo):

  manim -pqh modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/manim/scenes.py GBMPathsScene
  manim -pqh .../scenes.py DensityConvergenceScene
  manim -pqh .../scenes.py MonteCarloConvergenceScene
  manim -pqh .../scenes.py Lab01Full  # sequência completa

Qualidade: -ql (rápido) | -qm | -qh (1080p)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import *

# --- path do pacote econofisica ---
_ROOT = Path(__file__).resolve().parents[5]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from econofisica.gbm import (  # noqa: E402
    gbm_ST_moments,
    gbm_ln_params,
    lognormal_pdf,
    simulate_gbm_paths,
)

# Parâmetros do lab (mesmos do run_lab.py)
S0, MU, SIGMA, T, NSTEPS = 100.0, 0.08, 0.02, 1.0, 252
SEED = 42
# Para visual do túnel mais legível nas animações de path, usamos também σ_wide
SIGMA_WIDE = 0.20

BG = "#0f1419"
ACCENT = "#3d9cf0"
ACCENT2 = "#f0a03d"
ACCENT3 = "#e85d5d"
MUTED = "#8b9bb4"
WHITE = "#e8eef7"


def _setup_dark(scene: Scene) -> None:
    scene.camera.background_color = BG


class GBMPathsScene(Scene):
    """Trajetórias GBM crescendo no tempo + envelope teórico."""

    def construct(self):
        _setup_dark(self)
        title = Text("Lab 01 · GBM — trajetórias", font_size=32, color=WHITE)
        subtitle = Text(
            f"S₀={S0:.0f}  μ={MU}  σ={SIGMA_WIDE}  T={T}  N=40 paths",
            font_size=18,
            color=MUTED,
        )
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)

        N_show = 40
        paths = simulate_gbm_paths(
            S0, MU, SIGMA_WIDE, T, NSTEPS, N_show, seed=SEED
        )
        t = np.linspace(0.0, T, NSTEPS + 1)
        m, v = gbm_ln_params(S0, MU, SIGMA_WIDE, T)
        # envelope no espaço do preço: exp(m(t) ± z sqrt(v(t)))
        # m(t), v(t) escalam linearmente com t
        z = 2.0
        mean_line = S0 * np.exp(MU * t)  # E[S_t]
        # approx envelope via log-mean ± z σ√t
        log_m = np.log(S0) + (MU - 0.5 * SIGMA_WIDE**2) * t
        log_s = SIGMA_WIDE * np.sqrt(t)
        upper = np.exp(log_m + z * log_s)
        lower = np.exp(log_m - z * log_s)

        axes = Axes(
            x_range=[0, T, 0.25],
            y_range=[60, 160, 20],
            x_length=10.5,
            y_length=5.2,
            axis_config={"color": MUTED, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.35)
        x_lab = axes.get_x_axis_label(Text("t", font_size=20, color=MUTED))
        y_lab = axes.get_y_axis_label(Text("S_t", font_size=20, color=MUTED))

        path_curves = VGroup()
        for i in range(N_show):
            pts = [axes.c2p(t[k], paths[i, k]) for k in range(len(t))]
            curve = VMobject(stroke_color=ACCENT, stroke_opacity=0.35, stroke_width=1.5)
            curve.set_points_smoothly(pts)
            path_curves.add(curve)

        mean_m = VMobject(stroke_color=ACCENT2, stroke_width=3)
        mean_m.set_points_smoothly([axes.c2p(t[k], mean_line[k]) for k in range(len(t))])
        up_m = VMobject(stroke_color=ACCENT3, stroke_width=2, stroke_opacity=0.85)
        up_m.set_points_smoothly([axes.c2p(t[k], upper[k]) for k in range(len(t))])
        lo_m = VMobject(stroke_color=ACCENT3, stroke_width=2, stroke_opacity=0.85)
        lo_m.set_points_smoothly([axes.c2p(t[k], lower[k]) for k in range(len(t))])

        legend = VGroup(
            Text("paths MC", font_size=16, color=ACCENT),
            Text("E[S_t]", font_size=16, color=ACCENT2),
            Text("túnel ±2σ (log)", font_size=16, color=ACCENT3),
        ).arrange(RIGHT, buff=0.6).next_to(axes, DOWN, buff=0.25)

        self.play(FadeIn(header), Create(axes), FadeIn(x_lab), FadeIn(y_lab))
        self.play(
            LaggedStart(*[Create(c) for c in path_curves], lag_ratio=0.04),
            run_time=3.5,
        )
        self.play(Create(mean_m), Create(up_m), Create(lo_m), FadeIn(legend))
        self.wait(1.5)


class DensityConvergenceScene(Scene):
    """Histograma de S_T preenchendo + curva pdf teórica."""

    def construct(self):
        _setup_dark(self)
        title = Text("S_T → densidade log-normal", font_size=32, color=WHITE)
        subtitle = Text(
            f"σ={SIGMA} (lab) · N cresce 1k → 10k → 100k",
            font_size=18,
            color=MUTED,
        )
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(FadeIn(header))

        m, v = gbm_ln_params(S0, MU, SIGMA, T)
        mean_th, _ = gbm_ST_moments(S0, MU, SIGMA, T)
        paths = simulate_gbm_paths(S0, MU, SIGMA, T, NSTEPS, 100_000, seed=SEED)
        ST = paths[:, -1]

        s_min, s_max = float(np.percentile(ST, 0.2)), float(np.percentile(ST, 99.8))
        axes = Axes(
            x_range=[s_min, s_max, (s_max - s_min) / 5],
            y_range=[0, 0.25, 0.05],
            x_length=10,
            y_length=4.8,
            axis_config={"color": MUTED, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.2)
        x_lab = Text("S_T", font_size=18, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.15)
        y_lab = Text("densidade", font_size=18, color=MUTED).next_to(axes.y_axis, LEFT, buff=0.15)

        s_grid = np.linspace(s_min, s_max, 300)
        pdf = lognormal_pdf(s_grid, m, v)
        pdf_curve = VMobject(stroke_color=ACCENT3, stroke_width=4)
        pdf_curve.set_points_smoothly(
            [axes.c2p(s_grid[i], pdf[i]) for i in range(len(s_grid))]
        )

        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))
        self.play(Create(pdf_curve), run_time=1.2)

        bars_group = VGroup()
        label = None
        for N in (1_000, 10_000, 100_000):
            sample = ST[:N]
            hist, edges = np.histogram(sample, bins=40, density=True)
            new_bars = VGroup()
            for h, left, right in zip(hist, edges[:-1], edges[1:]):
                rect = Rectangle(
                    width=axes.c2p(right, 0)[0] - axes.c2p(left, 0)[0],
                    height=max(axes.c2p(0, h)[1] - axes.c2p(0, 0)[1], 1e-4),
                    stroke_width=0,
                    fill_color=ACCENT,
                    fill_opacity=0.45,
                )
                rect.move_to(axes.c2p((left + right) / 2, h / 2))
                new_bars.add(rect)

            mean_emp = float(sample.mean())
            new_label = Text(
                f"N={N:,}   mean={mean_emp:.3f}   (teoria {mean_th:.3f})",
                font_size=20,
                color=ACCENT2,
            ).to_corner(UR).shift(DOWN * 0.9 + LEFT * 0.2)

            anims = []
            if len(bars_group) > 0:
                anims.append(FadeOut(bars_group))
            if label is not None:
                anims.append(FadeOut(label))
            anims.extend([FadeIn(new_bars), FadeIn(new_label)])
            self.play(*anims, run_time=1.3)
            bars_group = new_bars
            label = new_label
            self.wait(0.8)

        note = Text(
            "Histograma → pdf teórica (máscara s>0)",
            font_size=18,
            color=MUTED,
        ).next_to(axes, DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(1.5)


class MonteCarloConvergenceScene(Scene):
    """Erro |mean−E| e |var−Var| vs N em escala log."""

    def construct(self):
        _setup_dark(self)
        title = Text("Convergência Monte Carlo", font_size=32, color=WHITE)
        subtitle = Text("subamostras aninhadas da mesma simulação", font_size=18, color=MUTED)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        self.play(FadeIn(header))

        mean_th, var_th = gbm_ST_moments(S0, MU, SIGMA, T)
        paths = simulate_gbm_paths(S0, MU, SIGMA, T, NSTEPS, 100_000, seed=SEED)
        ST = paths[:, -1]
        Ns = np.array([1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000])
        err_mean = []
        err_var = []
        for N in Ns:
            s = ST[: int(N)]
            err_mean.append(abs(float(s.mean()) - mean_th))
            err_var.append(abs(float(np.var(s, ddof=1)) - var_th))
        err_mean = np.array(err_mean)
        err_var = np.array(err_var)

        # plot in log-log via Axes with log ticks approximated by transforming
        logN = np.log10(Ns)
        log_em = np.log10(np.maximum(err_mean, 1e-8))
        log_ev = np.log10(np.maximum(err_var, 1e-8))

        axes = Axes(
            x_range=[2.8, 5.2, 0.5],
            y_range=[-4.5, -0.5, 1],
            x_length=10,
            y_length=4.6,
            axis_config={"color": MUTED, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.15)
        xlab = Text("log10 N", font_size=18, color=MUTED).next_to(axes.x_axis, DOWN)
        ylab = Text("log10 erro", font_size=18, color=MUTED).next_to(axes.y_axis, LEFT)

        def poly(xs, ys, color):
            m = VMobject(stroke_color=color, stroke_width=3.5)
            m.set_points_smoothly([axes.c2p(xs[i], ys[i]) for i in range(len(xs))])
            dots = VGroup(
                *[
                    Dot(axes.c2p(xs[i], ys[i]), radius=0.06, color=color)
                    for i in range(len(xs))
                ]
            )
            return m, dots

        line_m, dots_m = poly(logN, log_em, ACCENT)
        line_v, dots_v = poly(logN, log_ev, ACCENT2)

        # referência 1/√N
        c = err_mean[0] * np.sqrt(Ns[0])
        ref = c / np.sqrt(Ns)
        log_ref = np.log10(ref)
        line_ref, _ = poly(logN, log_ref, ACCENT3)
        line_ref.set_stroke(opacity=0.7, width=2)

        legend = VGroup(
            Text("|mean − E[S_T]|", font_size=16, color=ACCENT),
            Text("|var − Var(S_T)|", font_size=16, color=ACCENT2),
            Text("~ 1/√N", font_size=16, color=ACCENT3),
        ).arrange(RIGHT, buff=0.55).next_to(axes, DOWN, buff=0.35)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab))
        self.play(Create(line_ref))
        self.play(Create(line_m), FadeIn(dots_m), run_time=1.5)
        self.play(Create(line_v), FadeIn(dots_v), run_time=1.5)
        self.play(FadeIn(legend))

        takeaway = Text(
            "Lei dos grandes números: erro típico cai como 1/√N",
            font_size=20,
            color=WHITE,
        ).next_to(legend, DOWN, buff=0.25)
        self.play(FadeIn(takeaway))
        self.wait(2)


class Lab01Full(Scene):
    """Sequência pedagógica curta: título → paths → densidade → convergência."""

    def construct(self):
        _setup_dark(self)
        t1 = Text("Econofísica · @mosscardoso", font_size=36, color=WHITE)
        t2 = Text("Lab 01 — GBM + Monte Carlo", font_size=28, color=ACCENT)
        t3 = Text("teoria → simulação → validação", font_size=20, color=MUTED)
        intro = VGroup(t1, t2, t3).arrange(DOWN, buff=0.35)
        self.play(FadeIn(intro, shift=UP * 0.2))
        self.wait(1.2)
        self.play(FadeOut(intro))

        # Fórmulas em Text (sem LaTeX local) — instale TeX se quiser MathTex depois
        formulas = VGroup(
            Text("dS = μ S dt + σ S dW", font_size=34, color=WHITE),
            Text("m = ln(S0) + (μ − ½σ²)T    v = σ² T", font_size=26, color=ACCENT),
            Text("E[S_T] = S0 · exp(μ T)", font_size=28, color=ACCENT2),
        ).arrange(DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(f) for f in formulas], lag_ratio=0.35))
        self.wait(1.8)
        self.play(FadeOut(formulas))

        # mini path flash (few lines)
        paths = simulate_gbm_paths(S0, MU, SIGMA_WIDE, T, NSTEPS, 25, seed=SEED)
        t = np.linspace(0, T, NSTEPS + 1)
        axes = Axes(
            x_range=[0, T, 0.5],
            y_range=[70, 150, 20],
            x_length=10,
            y_length=4.5,
            axis_config={"color": MUTED},
            tips=False,
        )
        curves = VGroup()
        for i in range(25):
            c = VMobject(stroke_color=ACCENT, stroke_opacity=0.4, stroke_width=1.5)
            c.set_points_smoothly([axes.c2p(t[k], paths[i, k]) for k in range(len(t))])
            curves.add(c)
        label = Text("simular trajetórias → comparar com teoria", font_size=22, color=WHITE)
        label.next_to(axes, DOWN)
        self.play(Create(axes), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.03), run_time=2.5)
        self.play(FadeIn(label))
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        end = VGroup(
            Text("Próximo: rode run_lab.py e as cenas Manim", font_size=26, color=WHITE),
            Text("modules/M02-dinamica-gregas/labs/01-gbm-monte-carlo/", font_size=16, color=MUTED),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(end))
        self.wait(2)
