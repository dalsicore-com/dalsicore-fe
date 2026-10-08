// Single source of truth for Dalsicore's shipped history.
//
// Every number here comes from the user's own Google Play Console + GA4/Firebase
// exports. Nothing is invented. Where a figure was unavailable the field is simply
// absent rather than guessed. See /home/baobaojingyi/Documents/Daftar Claude startup
// for the raw exports.

export type AppStatus = "live" | "retired";

export interface AppEntry {
  slug: string;
  name: string;
  package: string;
  /** One line, plain English. */
  tagline: string;
  /** Longer Play-store style description. */
  description: string;
  category: string;
  status: AppStatus;
  /** Year first published to Google Play (from Play ratings history). */
  shipped: number;
  /** Year the listing was unpublished. Absent while live. */
  retired?: number;
  /** Mean of the app's 28-day average rating windows (Play Console export). */
  rating?: number;
  /** "built with Claude" highlight. */
  builtWithClaude?: boolean;
  /** Marquee product — gets a featured card on the homepage. */
  featured?: boolean;
  icon: string;
  banner: string;
  screenshots: string[];
  links?: {
    play?: string;
    github?: string;
  };
}

export const APPS: AppEntry[] = [
  {
    slug: "substracker",
    name: "SubsTracker",
    package: "com.dalsicore.substrack",
    tagline: "Track subscriptions, renewal reminders, recurring bills, and monthly cost.",
    description:
      "A subscription tracker and recurring-bill manager with renewal reminders, monthly cost breakdowns and a yearly projection. Local-first, manual control, no bank connection. Built end-to-end with Claude — no hand-written code.",
    category: "Finance / Tools",
    status: "live",
    shipped: 2026,
    builtWithClaude: true,
    featured: true,
    icon: "/apps/substracker/icon.png",
    banner: "/apps/substracker/banner.png",
    screenshots: [
      "/apps/substracker/ss1.png",
      "/apps/substracker/ss2.png",
      "/apps/substracker/ss3.png",
      "/apps/substracker/ss4.png",
      "/apps/substracker/ss5.jpg",
      "/apps/substracker/ss6.jpg"
    ],
    links: {
      play: "https://play.google.com/store/apps/details?id=com.dalsicore.substrack"
    }
  },
  {
    slug: "bookman",
    name: "BookMan: Bookmark Manager",
    package: "com.anafthdev.bookman",
    tagline: "Save, organise and back up links from any app or browser.",
    description:
      "A bookmark manager with Google Drive backup, collections, archiving, biometric locking, search, filtering and CSV export.",
    category: "Productivity",
    status: "retired",
    shipped: 2023,
    retired: 2025,
    rating: 2.8,
    icon: "/apps/bookman/icon.png",
    banner: "/apps/bookman/banner.png",
    screenshots: [
      "/apps/bookman/ss1.jpg",
      "/apps/bookman/ss2.jpg",
      "/apps/bookman/ss3.jpg",
      "/apps/bookman/ss4.jpg",
      "/apps/bookman/ss5.jpg",
      "/apps/bookman/ss6.jpg"
    ]
  },
  {
    slug: "financial-records",
    name: "Financial Records",
    package: "com.anafthdev.dujer",
    tagline: "Track income, expenses, budgets and wallets in one simple ledger.",
    description:
      "A personal finance recorder with income/expense tracking, budget limits, virtual wallets, statistics, fingerprint/PIN lock, multi-currency support and CSV export.",
    category: "Finance",
    status: "retired",
    shipped: 2022,
    retired: 2023,
    rating: 5.0,
    icon: "/apps/financial-records/icon.png",
    banner: "/apps/financial-records/banner.png",
    screenshots: [
      "/apps/financial-records/ss1.jpg",
      "/apps/financial-records/ss2.jpg",
      "/apps/financial-records/ss3.jpg",
      "/apps/financial-records/ss4.jpg",
      "/apps/financial-records/ss5.jpg",
      "/apps/financial-records/ss6.jpg",
      "/apps/financial-records/ss7.jpg",
      "/apps/financial-records/ss8.jpg"
    ]
  },
  {
    slug: "staver",
    name: "Staver — Status Saver",
    package: "com.anafthdev.staver",
    tagline: "Save and repost photo, GIF and video statuses from WhatsApp.",
    description:
      "A utility that lets you download, view and share WhatsApp / WhatsApp Business statuses with a built-in image viewer and media player.",
    category: "Utilities",
    status: "retired",
    shipped: 2022,
    retired: 2023,
    rating: 4.25,
    icon: "/apps/staver/icon.png",
    banner: "/apps/staver/banner.png",
    screenshots: [
      "/apps/staver/ss1.jpg",
      "/apps/staver/ss2.jpg",
      "/apps/staver/ss3.jpg",
      "/apps/staver/ss4.jpg",
      "/apps/staver/ss5.jpg",
      "/apps/staver/ss6.jpg"
    ]
  },
  {
    slug: "mathq",
    name: "MathQ: Math Riddle",
    package: "com.anafthdev.mathq",
    tagline: "Challenging, logic-first math puzzles for all ages.",
    description:
      "A puzzle game that presents a series of math problems requiring creative thinking and logic. Each level is built to teach more complex reasoning as you progress.",
    category: "Game / Education",
    status: "retired",
    shipped: 2022,
    retired: 2023,
    icon: "/apps/mathq/icon.png",
    banner: "/apps/mathq/banner.png",
    screenshots: [
      "/apps/mathq/ss1.jpg",
      "/apps/mathq/ss2.jpg",
      "/apps/mathq/ss3.jpg",
      "/apps/mathq/ss4.jpg"
    ]
  },
  {
    slug: "npuzzle",
    name: "NPuzzle — Sliding Puzzle",
    package: "com.anafthdev.npuzzle",
    tagline: "A light, cloud-synced sliding puzzle game with 5 difficulties.",
    description:
      "A simple sliding puzzle with five difficulty levels, themes, animations and sound effects, plus automatic score backup and recovery to the cloud.",
    category: "Game",
    status: "retired",
    shipped: 2022,
    retired: 2023,
    icon: "/apps/npuzzle/icon.png",
    banner: "/apps/npuzzle/banner.png",
    screenshots: [
      "/apps/npuzzle/ss1.jpg",
      "/apps/npuzzle/ss2.jpg",
      "/apps/npuzzle/ss3.jpg",
      "/apps/npuzzle/ss4.jpg",
      "/apps/npuzzle/ss5.jpg"
    ]
  },
  {
    slug: "android-material-components",
    name: "Android Material Components",
    package: "com.eunidev.materialdesign",
    tagline: "Live Material Components reference, with copy-ready code.",
    description:
      "A developer reference app showing Material Components — badges, bottom app bar, navigation, chips, date pickers, cards, menus and progress — with sample code to implement each one.",
    category: "Developer Tools",
    status: "retired",
    shipped: 2022,
    retired: 2023,
    rating: 4.33,
    icon: "/apps/android-material-components/icon.png",
    banner: "/apps/android-material-components/banner.png",
    screenshots: [
      "/apps/android-material-components/ss1.jpg",
      "/apps/android-material-components/ss2.jpg",
      "/apps/android-material-components/ss3.jpg",
      "/apps/android-material-components/ss4.jpg",
      "/apps/android-material-components/ss5.jpg"
    ]
  },
  {
    slug: "material-design-3-android",
    name: "Material Design 3 Android",
    package: "com.anafthdev.materialdesign3",
    tagline: "Material Design 3 component samples for Android developers.",
    description:
      "A sample-code app for Material Design 3: app bars, bottom navigation, buttons, cards, checkboxes, chips, date pickers, FABs and navigation rails.",
    category: "Developer Tools",
    status: "retired",
    shipped: 2022,
    retired: 2024,
    rating: 4.38,
    icon: "/apps/material-design-3-android/icon.png",
    banner: "/apps/material-design-3-android/banner.png",
    screenshots: [
      "/apps/material-design-3-android/ss1.jpg",
      "/apps/material-design-3-android/ss2.jpg",
      "/apps/material-design-3-android/ss3.jpg",
      "/apps/material-design-3-android/ss4.jpg",
      "/apps/material-design-3-android/ss5.jpg"
    ]
  },
  {
    slug: "compose-material-component",
    name: "Compose Material Component",
    package: "com.anafthdev.jetpackcomposetutorial",
    tagline: "Jetpack Compose component playground and tutorial.",
    description:
      "A hands-on Jetpack Compose reference covering bottom app bars, navigation, bottom sheets, cards, checkboxes, dialogs, images, drawers, rails, sliders and switches.",
    category: "Developer Tools",
    status: "retired",
    shipped: 2022,
    retired: 2023,
    rating: 5.0,
    icon: "/apps/compose-material-component/icon.png",
    banner: "/apps/compose-material-component/banner.png",
    screenshots: [
      "/apps/compose-material-component/ss1.jpg",
      "/apps/compose-material-component/ss2.jpg",
      "/apps/compose-material-component/ss3.jpg",
      "/apps/compose-material-component/ss4.jpg"
    ]
  },
  {
    slug: "compose-material-design-3",
    name: "Compose Material Design 3",
    package: "com.anafthdev.md3compose",
    tagline: "Material 3 preview app, fully built in Jetpack Compose.",
    description:
      "A Material Design 3 preview app built with Jetpack Compose, with live customisation of colour, elevation and shape for each component.",
    category: "Developer Tools",
    status: "retired",
    shipped: 2022,
    retired: 2024,
    rating: 4.4,
    icon: "/apps/compose-material-design-3/icon.png",
    banner: "/apps/compose-material-design-3/banner.png",
    screenshots: [
      "/apps/compose-material-design-3/ss1.jpg",
      "/apps/compose-material-design-3/ss2.jpg",
      "/apps/compose-material-design-3/ss3.jpg",
      "/apps/compose-material-design-3/ss4.jpg",
      "/apps/compose-material-design-3/ss5.jpg"
    ]
  }
];

export const LIVE_APPS = APPS.filter((a) => a.status === "live");
export const RETIRED_APPS = APPS.filter((a) => a.status === "retired");

export const getApp = (slug: string) => APPS.find((a) => a.slug === slug);
