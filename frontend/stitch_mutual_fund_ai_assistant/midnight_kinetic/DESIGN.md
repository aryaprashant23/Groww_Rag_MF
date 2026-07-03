---
name: Midnight Kinetic
colors:
  surface: '#0c1324'
  surface-dim: '#0c1324'
  surface-bright: '#33394c'
  surface-container-lowest: '#070d1f'
  surface-container-low: '#151b2d'
  surface-container: '#191f31'
  surface-container-high: '#23293c'
  surface-container-highest: '#2e3447'
  on-surface: '#dce1fb'
  on-surface-variant: '#c3c6d7'
  inverse-surface: '#dce1fb'
  inverse-on-surface: '#2a3043'
  outline: '#8d90a0'
  outline-variant: '#434655'
  surface-tint: '#b4c5ff'
  primary: '#b4c5ff'
  on-primary: '#002a78'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#0053db'
  secondary: '#c0c1ff'
  on-secondary: '#1000a9'
  secondary-container: '#3131c0'
  on-secondary-container: '#b0b2ff'
  tertiary: '#c4c7c9'
  on-tertiary: '#2d3133'
  tertiary-container: '#6b6e70'
  on-tertiary-container: '#eff1f3'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#e1e0ff'
  secondary-fixed-dim: '#c0c1ff'
  on-secondary-fixed: '#07006c'
  on-secondary-fixed-variant: '#2f2ebe'
  tertiary-fixed: '#e0e3e5'
  tertiary-fixed-dim: '#c4c7c9'
  on-tertiary-fixed: '#191c1e'
  on-tertiary-fixed-variant: '#444749'
  background: '#0c1324'
  on-background: '#dce1fb'
  surface-variant: '#2e3447'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Geist
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Geist
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

This design system embodies a "Next-Gen Fintech" aesthetic, merging the professional reliability of traditional finance with the forward-leaning energy of high-tech software. The brand personality is sophisticated, precise, and authoritative, yet visually immersive.

The visual style is **Glassmorphism**, executed with a dark-mode-first philosophy. It utilizes deep layering, background blurs, and luminous accents to create a sense of digital depth. The interface should evoke a "command center" feel—highly functional but aesthetically premium. Key characteristics include high-contrast typography for legibility and vibrant gradients to guide the eye toward primary actions.

## Colors

The palette is anchored in **Slate-950** (`#020617`) for the base background, providing a deep, ink-like foundation that allows glass elements to pop. 

- **Primary & Secondary:** A duo of Vibrant Blue and Indigo used primarily in gradients for buttons, active states, and data visualizations.
- **Surface Tiers:** Surfaces are constructed using semi-transparent overlays of Slate-900 with varying levels of opacity (10% to 60%) to facilitate the glass effect.
- **Accents:** Use a "Glow" treatment—low-opacity radial gradients—behind key cards or charts to suggest depth and importance.
- **Typography:** High-contrast White (`#FFFFFF`) for headings and Slate-300 for secondary text to ensure AA/AAA accessibility against the dark backdrop.

## Typography

This design system utilizes **Geist** for its systematic, technical, and clean appearance. The tight letter-spacing on display styles reinforces the premium, modern feel. 

**JetBrains Mono** is introduced for labels, data points, and financial figures. This monospaced choice ensures that fluctuating numbers (like stock prices or balances) remain stable and highly legible, reinforcing the "fintech" utility. All headers should favor a "Semi-Bold" or "Bold" weight to contrast against the ethereal glass backgrounds.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a 12-column structure for desktop. To maintain the sophisticated feel, whitespace is used generously (the "stack-lg" unit). 

- **Desktop:** 12 columns, 24px gutters, 40px side margins.
- **Tablet:** 8 columns, 20px gutters, 24px side margins.
- **Mobile:** 4 columns, 16px gutters, 16px side margins.

Content should be grouped into "Glass Containers" (cards). Spacing within these containers should be consistent, using a 4px base scale. High-priority dashboards should use a "tight" density for data tables, while marketing or landing pages should use "loose" density to emphasize the glass aesthetics.

## Elevation & Depth

Hierarchy is established through **Backdrop Blurs** and **Luminous Outlines** rather than traditional shadows.

1.  **Base:** The Slate-950 background.
2.  **Level 1 (Default Surface):** 10% opacity white overlay with a 12px backdrop blur. 1px border at 10% white opacity.
3.  **Level 2 (Active/Hover):** 18% opacity white overlay with a 20px backdrop blur. 1px border at 20% white opacity.
4.  **Level 3 (Modals/Popovers):** 25% opacity white overlay with a 40px backdrop blur.

**The "Glow" Effect:** For primary cards, apply a 1px border using the Action Gradient at 40% opacity. This creates a "subtle glowing border" that separates the element from the dark background without the muddiness of heavy shadows.

## Shapes

The design system uses a **Rounded** (Level 2) shape language. This softens the technical nature of the Geist typeface and the monospaced data, making the app feel more approachable and modern.

- **Standard Elements:** 0.5rem (8px) for input fields, small cards, and buttons.
- **Large Containers:** 1rem (16px) for main dashboard cards and modals.
- **Interactive Pill:** 1.5rem (24px) for tags, chips, and secondary navigation toggles.

All glass containers must have a consistent corner radius to ensure the "stacked glass" effect looks intentional and architectural.

## Components

### Buttons
- **Primary:** Action Gradient background, white text, 8px radius. No border. On hover, increase gradient saturation.
- **Secondary:** Glass background (15% white, 12px blur), 1px white-10% border.
- **Ghost:** No background, Slate-300 text. Use for low-emphasis actions.

### Cards (The Core Component)
The fundamental building block. Every card must have `backdrop-filter: blur(16px)` and a subtle 1px top-down gradient border (White 15% to White 0%) to simulate a light source hitting the edge of the glass.

### Input Fields
Darker than the surface background (Slate-900), 8px radius, 1px border (Slate-800). On focus, the border transitions to the Primary Blue with a 4px outer glow. Use JetBrains Mono for the input text.

### Chips & Badges
Small, pill-shaped elements. For status (e.g., "Success", "Pending"), use a low-opacity version of the status color (e.g., Green 10%) with a high-saturation 1px border.

### Icons
Use **Lucide** icons. Line weight should be consistent at 1.5px or 2px. Use a "duotone" approach where the primary part of the icon is White and a secondary accent part is Primary Blue.

### Data Visualizations
Charts should use the Primary/Secondary gradients. Area charts should have a gradient fill that fades from 30% opacity at the top to 0% at the bottom, maintaining the translucent glass theme.