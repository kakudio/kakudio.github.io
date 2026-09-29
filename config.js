// Site content config. The page reads this on load.
// A link set to "PLACEHOLDER" (or anything that isn't an https:// URL) shows as "coming soon"; paste the real URL to make it live.
window.KAKUDIO_CONFIG = {
  randomizer: {
    name: "Shell Game",
    descriptor: "A key item randomizer for Spelunky 2",
    description:
      "A key item randomizer for Spelunky 2. Important checks and rewards are shuffled throughout the game, encouraging players to explore routes, bosses, characters, and objectives they might normally skip.",
    status: "Beta",
    statusNote: "Testers wanted. Expect rough edges, and please tell me about them.",
    requirements: "Needs Spelunky 2 on Steam, with Modlunky 2 and Playlunky.",
  },

  links: {
    download: "https://github.com/kakudio/spelunky2-key-item-randomizer/releases/latest",
    github: "https://github.com/kakudio/spelunky2-key-item-randomizer",
    discord: "PLACEHOLDER",
    spelunkyFyi: "PLACEHOLDER",
    githubOrg: "https://github.com/kakudio",
  },

  // Screenshots or gameplay GIFs, shown in order in the media slots. Example:
  // { src: "/assets/media/tide-pool-ankh.gif", alt: "The Ankh turning up in Tide Pool" }
  media: [],
};
