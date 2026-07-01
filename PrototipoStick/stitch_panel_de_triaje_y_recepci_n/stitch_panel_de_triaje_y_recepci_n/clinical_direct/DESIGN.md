---
name: Clinical Direct
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
  on-surface-variant: '#4a4733'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#7c7761'
  outline-variant: '#cdc7ad'
  surface-tint: '#695f00'
  primary: '#695f00'
  on-primary: '#ffffff'
  primary-container: '#dbc81a'
  on-primary-container: '#5c5300'
  inverse-primary: '#dbc81b'
  secondary: '#00687a'
  on-secondary: '#ffffff'
  secondary-container: '#55e0fe'
  on-secondary-container: '#006171'
  tertiary: '#326190'
  on-tertiary: '#ffffff'
  tertiary-container: '#9dcaff'
  on-tertiary-container: '#235583'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#f9e53c'
  primary-fixed-dim: '#dbc81b'
  on-primary-fixed: '#201c00'
  on-primary-fixed-variant: '#4f4700'
  secondary-fixed: '#abedff'
  secondary-fixed-dim: '#49d7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#d1e4ff'
  tertiary-fixed-dim: '#9dcaff'
  on-tertiary-fixed: '#001d35'
  on-tertiary-fixed-variant: '#124977'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-bold:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-md:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-margin: 16px
  gutter: 12px
---

## Brand & Style

This design system is engineered for high-stakes medical environments where speed of recognition and clarity of action are paramount. The brand personality is authoritative yet calm, prioritizing functional utility over decorative flair. It serves nursing staff and triage receptionists who require a high-efficiency interface to manage patient flow under pressure.

The design style follows a **Modern Corporate** approach with a focus on **Information Density and High-Contrast**. It utilizes a structured grid to organize complex data, ensuring that critical patient statuses are immediately identifiable. The aesthetic is clean and "clinical," using generous white space to reduce cognitive load while employing bold color accents to direct the user's eye to primary tasks and urgent alerts.

## Colors

The color palette is functional rather than purely aesthetic. 
- **Primary (#DBC81A):** Used exclusively for high-level global actions, primary buttons, and critical header states. Its golden hue provides high visibility without the inherent "danger" associated with red.
- **Secondary (#1ABDDB):** Acts as the "active" indicator. It is used for focused input states, selection indicators, and interactive icons.
- **Backgrounds:** A neutral light gray (#F8F9FA) is used for the main workspace to prevent the "vibrancy" of pure white, reducing eye strain during long shifts.
- **Semantic Palette:** A strict adherence to Red (Critical), Orange (Moderate), and Green (Stable) is maintained for triage categorization.

## Typography

The design system uses **Inter** for its exceptional legibility in data-heavy environments. The typographic hierarchy is designed to highlight patient names and priority levels first. 

- **Headlines:** Reserved for patient names within cards and section titles.
- **Labels:** Uppercase bold labels are used for metadata (e.g., "TIME IN QUEUE", "TRIAGE CAT") to distinguish data headers from the data itself.
- **Numerical Data:** Tabular figures are preferred for time-stamps and vitals to ensure vertical alignment in lists.

## Layout & Spacing

This is a **mobile-first** system designed for tablets and handheld devices used on the floor. 
- **Grid:** A 4-column fluid grid for mobile, expanding to 12 columns for desktop reception consoles.
- **Rhythm:** An 8px base unit (4px for tight components) ensures a consistent vertical rhythm.
- **Touch Targets:** All interactive elements maintain a minimum hit area of 44x44px. 
- **Safe Areas:** Cards use 16px internal padding to ensure text doesn't feel cramped, maintaining a professional, airy feel despite high information density.

## Elevation & Depth

To maintain a "clinical" look, this design system avoids heavy shadows. Depth is communicated through **Tonal Layers** and **Low-Contrast Outlines**:
- **Level 0 (Background):** #F8F9FA.
- **Level 1 (Cards/Sheets):** Pure White (#FFFFFF) with a 1px solid border (#E9ECEF).
- **Level 2 (Modals/Popovers):** Pure White with a subtle 8px blur, 10% opacity black shadow to lift the element during urgent interactions.
- **Interactive States:** Focused inputs use a 2px Cyan (#1ABDDB) border rather than a shadow to indicate "active" status.

## Shapes

The design system uses **Soft** geometry (4px radius). This slight rounding provides a modern, approachable feel while maintaining the structured, serious appearance expected of medical software.
- **Buttons & Inputs:** 4px (Soft) rounded corners.
- **Status Tags/Pills:** Fully rounded (Pill-shaped) to distinguish them from interactive buttons.
- **Cards:** 8px (Large) rounded corners to softly group patient information.

## Components

### Buttons
- **Primary:** Background #DBC81A, Text #000000 (High Contrast). Used for "Admit," "Complete Triage," or "Save."
- **Secondary:** Transparent background, 1px Cyan border, Cyan text. Used for "Cancel" or "Edit."
- **Emergency FAB:** A circular button, Primary color background, with a prominent icon. Always anchored to the bottom right.

### Patient Queue Cards
- White background, 1px neutral border.
- A vertical color-bar on the extreme left edge indicates triage status (Red/Orange/Green).
- Patient name in `headline-md`, vitals displayed in a 2-column grid within the card using `body-sm`.

### Input Fields
- Background: #FFFFFF.
- Border: 1px #DEE2E6.
- Active/Focus State: 2px #1ABDDB border.
- Error State: 2px #DC3545 border with helper text.

### Triage Status Indicators
- Small, high-saturation "pills."
- **Critical:** Red background, white text.
- **Moderate:** Orange background, white text.
- **Stable:** Green background, white text.

### List Items
- Compact rows with 12px vertical padding. 
- Dividers are 1px #E9ECEF. 
- Right-aligned "chevron" icons indicate drill-down capability for patient history.