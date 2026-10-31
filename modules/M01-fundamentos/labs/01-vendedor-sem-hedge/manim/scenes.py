"""
Animações Manim — Lab M01.01 vendedor de call sem hedge.

  manim -pql .../scenes.py PathsByMoneynessScene
  manim -pql .../scenes.py NakedSellerPnLScene
  manim -pql .../scenes.py LabM01SellerFull
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import *

_ROOT = Path(__file__).resolve().parents[5]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from econofisica.gbm import simulate_gbm_paths  # noqa: E402
from econofisica.options import naked_short_call_pnl  # noqa: E402

S0, K, MU, SIGMA, T, NSTEPS = 100.0, 100.0, 0.05, 0.20, 1.0, 252
N_PATHS, PREMIO, SEED = 1000, 7.0, 42

BG = "#0f1419"
BLUE = "#3d9cf0"
RED = "#e85d5d"
ORANGE = "#f0a03d"
MUTED = "#8b9bb4"
WHITE = "#e8eef7"


def _setup(scene: Scene) -> None:
    scene.camera.background_color = BG


def _data():
    paths = simulate_gbm_paths(S0, MU, SIGMA, T, NSTEPS, N_PATHS, seed=SEED)
    ST = paths[:, -1]
    pnl = naked_short_call_pnl(ST, K, PREMIO)
    return paths, ST, pnl


class PathsByMoneynessScene(Scene):
    def construct(self):
        _setup(self)
        title = Text("Call vendida naked — trajetórias", font_size=30, color=WHITE)
        sub = Text(
            f"S0=K={K:.0f}  μ={MU}  σ={SIGMA}  prêmio={PREMIO}",
            font_size=18,
            color=MUTED,
        )
        header = VGroup(title, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        self.play(FadeIn(header))

        paths, ST, _ = _data()
        t = np.linspace(0, T, NSTEPS + 1)
        axes = Axes(
            x_range=[0, T, 0.25],
            y_range=[40, 200, 40],
            x_length=10.5,
            y_length=5.0,
            axis_config={"color": MUTED, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.25)

        strike = DashedLine(
            axes.c2p(0, K),
            axes.c2p(T, K),
            color=ORANGE,
            stroke_width=2.5,
        )

        n_show = 60
        curves = VGroup()
        for i in range(n_show):
            color = RED if ST[i] > K else BLUE
            c = VMobject(stroke_color=color, stroke_opacity=0.4, stroke_width=1.6)
            c.set_points_smoothly([axes.c2p(t[k], paths[i, k]) for k in range(len(t))])
            curves.add(c)

        legend = VGroup(
            Text("OTM / ≈ATM", font_size=16, color=BLUE),
            Text("ITM (vendedor paga)", font_size=16, color=RED),
            Text("strike K", font_size=16, color=ORANGE),
        ).arrange(RIGHT, buff=0.55).next_to(axes, DOWN, buff=0.2)

        self.play(Create(axes), Create(strike))
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.03), run_time=3.2)
        self.play(FadeIn(legend))
        self.wait(1.4)


class NakedSellerPnLScene(Scene):
    def construct(self):
        _setup(self)
        title = Text("P&L do vendedor sem hedge", font_size=30, color=WHITE)
        sub = Text("massa em +prêmio  ·  cauda longa de perdas", font_size=18, color=MUTED)
        header = VGroup(title, sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        self.play(FadeIn(header))

        _, ST, pnl = _data()
        lo, hi = float(np.percentile(pnl, 1)), float(np.percentile(pnl, 99.5))
        # stretch left a bit for losses
        lo = min(lo, -40)
        axes = Axes(
            x_range=[lo, hi, (hi - lo) / 5],
            y_range=[0, 350, 50],
            x_length=10.5,
            y_length=4.6,
            axis_config={"color": MUTED, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.15)

        hist, edges = np.histogram(pnl, bins=36, range=(lo, hi))
        bars = VGroup()
        for h, left, right in zip(hist, edges[:-1], edges[1:]):
            height = max(axes.c2p(0, h)[1] - axes.c2p(0, 0)[1], 1e-4)
            width = axes.c2p(right, 0)[0] - axes.c2p(left, 0)[0]
            color = RED if (left + right) / 2 < 0 else BLUE
            rect = Rectangle(
                width=width,
                height=height,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.7,
            )
            rect.move_to(axes.c2p((left + right) / 2, h / 2))
            bars.add(rect)

        zero = DashedLine(
            axes.c2p(0, 0),
            axes.c2p(0, hist.max() * 1.05),
            color=WHITE,
            stroke_width=2,
        )
        prem = DashedLine(
            axes.c2p(PREMIO, 0),
            axes.c2p(PREMIO, hist.max() * 1.05),
            color=ORANGE,
            stroke_width=2,
        )

        stats = Text(
            f"E[pnl]={pnl.mean():.2f}   min={pnl.min():.1f}   P(pnl<0)={(pnl < 0).mean():.0%}",
            font_size=18,
            color=WHITE,
        ).next_to(axes, DOWN, buff=0.3)

        self.play(Create(axes))
        self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.01), run_time=2.0)
        self.play(Create(zero), Create(prem), FadeIn(stats))
        note = Text(
            "Wait-and-see: lucro limitado, perda potencialmente ilimitada",
            font_size=18,
            color=ORANGE,
        ).next_to(stats, DOWN, buff=0.2)
        self.play(FadeIn(note))
        self.wait(2.0)


class LabM01SellerFull(Scene):
    def construct(self):
        _setup(self)
        intro = VGroup(
            Text("Econofísica · @mosscardoso", font_size=34, color=WHITE),
            Text("M01 Lab 01 — Vendedor sem hedge", font_size=26, color=BLUE),
            Text("por que wait-and-see quebra", font_size=20, color=MUTED),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(intro))
        self.wait(1.2)
        self.play(FadeOut(intro))

        bullets = VGroup(
            Text("1. Simular S_t com GBM", font_size=26, color=WHITE),
            Text("2. Payoff call = max(S_T − K, 0)", font_size=26, color=WHITE),
            Text("3. pnl vendedor = prêmio − payoff", font_size=26, color=WHITE),
            Text("4. Ver a cauda de perdas → precisa de hedge", font_size=26, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bullets], lag_ratio=0.35))
        self.wait(2.0)
        self.play(FadeOut(bullets))

        end = Text("Rode run_lab.py --plot  ·  depois: delta hedge", font_size=22, color=MUTED)
        self.play(FadeIn(end))
        self.wait(1.5)
