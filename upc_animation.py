from manim import *

class PbPbUPC_WithDecay(Scene):
    def construct(self):
        # --- 1. SETUP OBJECTS (With Lorentz Contraction) ---

        # Physics Parameters
        impact_param = 3.0
        start_x = 7

        # Pb Ions: Use Ellipse for Lorentz contraction (pancake shape)
        # Squeezed width (0.5), Tall height (2.0)
        ion_color = BLUE_E

        # Ion 1 (Moving Right)
        ion1 = Ellipse(width=0.5, height=2.0, color=ion_color, fill_opacity=0.5)
        label1 = MathTex(r"Pb").move_to(ion1.get_center()).scale(0.7)
        group1 = VGroup(ion1, label1)
        group1.move_to(LEFT * start_x + UP * (impact_param/2))

        # Ion 2 (Moving Left)
        ion2 = Ellipse(width=0.5, height=2.0, color=ion_color, fill_opacity=0.5)
        label2 = MathTex(r"Pb").move_to(ion2.get_center()).scale(0.7)
        group2 = VGroup(ion2, label2)
        group2.move_to(RIGHT * start_x + DOWN * (impact_param/2))

        # --- 2. ANIMATE APPROACH ---

        self.add(group1, group2)

        # Move to center (t=0)
        self.play(
            group1.animate.move_to(UP * (impact_param/2)),
            group2.animate.move_to(DOWN * (impact_param/2)),
            run_time=1.5,
            rate_func=linear
        )

        # --- 3. INTERACTION & J/PSI ---

        # "Photon" Exchange (Wavy line)
        photon_start = group1.get_bottom()
        photon_end = group2.get_top()

        # Draw a quick dashed line or wave for the photon
        photon = DashedLine(photon_start, photon_end, color=YELLOW)
        self.play(Create(photon), run_time=0.2)

        # Create J/psi at the interaction point
        jpsi = Dot(color=RED, radius=0.15)
        jpsi_label = MathTex(r"J/\psi", color=RED).next_to(jpsi, UP, buff=0.1).scale(0.8)
        jpsi_group = VGroup(jpsi, jpsi_label)
        jpsi_group.move_to(photon_end) # Created at the target

        self.play(
            FadeIn(jpsi_group),
            FadeOut(photon),
            run_time=0.2
        )

        # --- 4. DEPARTURE & DRIFT ---

        # Ions move away, J/psi drifts left (conserving momentum from target)
        drift_time = 1.0

        self.play(
            group1.animate.shift(RIGHT * 4),
            group2.animate.shift(LEFT * 4),
            jpsi_group.animate.shift(LEFT * 1.5), # J/psi moves slowly left
            run_time=drift_time,
            rate_func=linear
        )

        # --- 5. THE DECAY (J/psi -> mu+ mu-) ---

        # Stop the J/psi to swap it for muons
        current_jpsi_pos = jpsi_group.get_center()

        # Define Muons
        # They share the J/psi's forward momentum (Left)
        # but have transverse momentum (Up/Down)
        muon_color = GREEN

        mu_plus = Dot(radius=0.08, color=muon_color)
        mu_plus_lbl = MathTex(r"\mu^+", color=muon_color).scale(0.6).next_to(mu_plus, UP, buff=0.1)
        mu_plus_grp = VGroup(mu_plus, mu_plus_lbl).move_to(current_jpsi_pos)

        mu_minus = Dot(radius=0.08, color=muon_color)
        mu_minus_lbl = MathTex(r"\mu^-", color=muon_color).scale(0.6).next_to(mu_minus, DOWN, buff=0.1)
        mu_minus_grp = VGroup(mu_minus, mu_minus_lbl).move_to(current_jpsi_pos)

        # The Flash (Decay event)
        flash = Flash(current_jpsi_pos, color=WHITE, line_length=0.2, flash_radius=0.3)

        # Remove J/psi, Add Muons
        self.remove(jpsi_group)
        self.play(
            flash,
            FadeIn(mu_plus_grp),
            FadeIn(mu_minus_grp),
            run_time=0.2
        )

        # Move Muons outward (The "V" shape)
        # Vector = Forward Motion (Left) + Transverse Motion (Up/Down)
        forward_vec = LEFT * 3
        transverse_vec = UP * 1.5

        self.play(
            # Ions continue fading into distance
            group1.animate.shift(RIGHT * 3).set_opacity(0),
            group2.animate.shift(LEFT * 3).set_opacity(0),

            # Muons fly out
            mu_plus_grp.animate.shift(forward_vec + transverse_vec),
            mu_minus_grp.animate.shift(forward_vec - transverse_vec),

            run_time=2,
            rate_func=linear
        )

        self.wait()
