---
name: Clinical Precision
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#434654'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#737686'
  outline-variant: '#c3c5d7'
  surface-tint: '#1353d8'
  primary: '#003fb1'
  on-primary: '#ffffff'
  primary-container: '#1a56db'
  on-primary-container: '#d4dcff'
  inverse-primary: '#b5c4ff'
  secondary: '#00687a'
  on-secondary: '#ffffff'
  secondary-container: '#55e0fe'
  on-secondary-container: '#006171'
  tertiary: '#99000b'
  on-tertiary: '#ffffff'
  tertiary-container: '#c50514'
  on-tertiary-container: '#ffd3ce'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b5c4ff'
  on-primary-fixed: '#00174d'
  on-primary-fixed-variant: '#003dab'
  secondary-fixed: '#abedff'
  secondary-fixed-dim: '#49d7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#ffdad6'
  tertiary-fixed-dim: '#ffb4ab'
  on-tertiary-fixed: '#410002'
  on-tertiary-fixed-variant: '#93000a'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  data-tabular:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '700'
    lineHeight: 24px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  container-padding-desktop: 32px
  container-padding-mobile: 16px
  gutter: 20px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style

This design system is engineered for high-stakes medical environments where clarity, speed of cognition, and professional reliability are paramount. The aesthetic follows a **Corporate / Modern** approach with a heavy emphasis on **Clinical High-Contrast** to ensure that critical data points are immediately distinguishable from the UI chrome.

The target audience consists of medical professionals who require a tool that feels like a high-end medical instrument: precise, sterile but approachable, and focused. The UI prioritizes information density without sacrificing legibility, utilizing a systematic structure to reduce cognitive load during diagnosis and patient monitoring.

## Colors

The palette is anchored by **Deep Blue (#1A56DB)**, signifying authority and stability. This is used for primary navigation, headers, and core action buttons to draw the eye to essential controls. 

**Cyan (#1ABDDB)** serves as a functional accent, used for active states, badges, and secondary interactive elements to provide a lighter visual counterpoint.

A critical addition to the palette is a **High-Alert Red (#E02424)**, reserved strictly for emergency vitals and critical patient alerts. The background remains a clean, neutral off-white to prevent screen glare during long shifts, while borders use a crisp light-gray to maintain structural definition.

## Typography

The design system utilizes **Inter** exclusively to leverage its exceptional legibility and systematic weight distribution. 

For patient monitoring, we utilize `data-tabular` settings (tabular figures) to ensure that numerical vitals do not shift horizontally as values change, facilitating rapid scanning of heart rates and blood pressure. Headlines are kept tight and bold to establish a clear hierarchy, while labels utilize a slightly increased letter spacing and medium weights to remain readable at small sizes on dense medical charts.

## Layout & Spacing

This design system employs a **Fixed Grid** for dashboard views to maintain consistent placement of critical patient data, transitioning to a **Fluid Grid** for secondary administrative views. 

The layout is built on a 4px baseline grid. Content blocks are separated by `stack-lg` (24px) to provide visual breathing room between distinct data sets (e.g., separating Vitals from Lab Results). On mobile devices, margins compress to 16px to maximize the available data area, and multi-column tables reflow into vertical cards with high-contrast headers.

## Elevation & Depth

To maintain a professional and sterile feel, the design system avoids heavy shadows. Instead, it utilizes **Tonal Layers** and **Low-contrast outlines**.

Surfaces are distinguished by subtle background color shifts (e.g., a slightly darker gray for the sidebar vs. a pure white for the main patient card). When elevation is required for modals or pop-overs, a very soft, high-diffusion shadow with a 2% Deep Blue tint is used to prevent the UI from feeling "muddy." Primary containers use a 1px border (#E5E7EB) to provide crisp definition without adding visual weight.

## Shapes

The design system uses a **Rounded** shape language to soften the clinical environment and make the software feel modern and user-friendly. 

Standard components (buttons, inputs) use a 0.5rem (8px) radius. Larger containers, such as patient profile cards, utilize `rounded-xl` (1.5rem / 24px). Status indicators and specific badges use `rounded-full` (pill-shape) to distinguish them from interactive buttons, creating a clear visual taxonomy between "information" and "action."

## Components

### Buttons
Primary buttons are solid Deep Blue with white text and `rounded-lg`. Secondary buttons use a Deep Blue outline with a subtle Cyan hover state.

### Chips & Badges
Badges for status (e.g., "Stable," "Critical") use a pill-shaped (`rounded-full`) geometry. "Stable" uses a soft Cyan background, while "Critical" utilizes the High-Alert Red with high-contrast white text.

### Input Fields
Inputs feature a 1px neutral border that thickens and changes to Deep Blue on focus. Labels are always positioned above the field using `label-md` for maximum visibility.

### Cards
Patient cards are the core component. They use a white background, `rounded-xl` corners, and a subtle border. Vitals within these cards should be displayed using the `data-tabular` typography for clear vertical alignment.

### Progress & Vitals Sparklines
Vitals history should be represented by simplified sparklines in Deep Blue, with "out-of-range" segments highlighted in Red. This allows doctors to see trends at a glance without reading raw data logs.