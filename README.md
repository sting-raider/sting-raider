<p align="center">
  <img src="./assets/header.svg" width="100%" alt="Animated banner introducing Ali Khan" />
</p>

<p align="center">
  <a href="https://sting-raider.github.io/portfolio/">[ PORTFOLIO ]</a> ·
  <a href="https://github.com/sting-raider/Resume/blob/main/Ali_Sufiyan_Khan_Resume.pdf">[ RÉSUMÉ ]</a> ·
  <a href="https://www.linkedin.com/in/ali-khan-4197b1217/">[ LINKEDIN ]</a>
</p>

## about me

I'm **Ali** — a Computer Science student at **VIT Vellore** ('27) who likes building AI systems that have to survive outside a notebook.

> *I make cars and robot arms learn things the hard way, then build tools to make everyone else's life slightly easier.*

- 🧭 Building **[RoleAtlas](https://github.com/sting-raider/RoleAtlas)** — a qualification-first job discovery workspace with its own Rust crawler fleet.
- 🛡️ Growing **[AegisFlow](https://github.com/sting-raider/AegisFlow)** — a network intrusion detection system that publishes every one of its own evaluation results, passing or not.
- 🎮 Working on **[Plaid](https://github.com/sting-raider/Plaid)** — researching automatic N64 ROM-to-native recompilation.
- 🤖 On the record: a **[PPO agent that drives F1 22](https://github.com/sting-raider/f1-rl-agent)** from raw UDP telemetry, and a **[UR10e arm learning pick-and-place](https://sting-raider.github.io/portfolio/projects/robotic-arm/)** in Isaac Lab.
- 🧰 I care about measurable evaluation, traceable AI outputs, privacy-friendly defaults, and software people can actually run.
- 🌱 Open to internships and early-career **SWE / AI engineering** roles — [résumé here](https://github.com/sting-raider/Resume/blob/main/Ali_Sufiyan_Khan_Resume.pdf).

## featured builds

<table>
  <tr>
    <td width="50%" valign="top">
      <h3 align="center">
        <a href="https://github.com/sting-raider/RoleAtlas">RoleAtlas</a>
      </h3>
      <p align="center">
        <sub>job discovery that respects your actual qualifications</sub>
      </p>
      <p>
        A global, qualification-first job workspace. Resume-to-profile onboarding, editable search plans,
        an eligibility engine built on ISO 3166 data, application dossiers, and a Rust crawler fleet
        coordinated over NATS JetStream — all in a six-service Docker stack.
      </p>
      <p align="center">
        <a href="https://sting-raider.github.io/RoleAtlas/">product tour</a> ·
        <a href="https://github.com/sting-raider/RoleAtlas">repo</a>
      </p>
      <p align="center">
        <code>Next.js</code> <code>TypeScript</code> <code>Rust</code>
        <code>NATS JetStream</code> <code>PostgreSQL</code> <code>Docker</code>
      </p>
    </td>
    <td width="50%" valign="top">
      <h3 align="center">
        <a href="https://github.com/sting-raider/AegisFlow">AegisFlow</a>
      </h3>
      <p align="center">
        <sub>intrusion detection, built test-first</sub>
      </p>
      <p>
        An adaptive network intrusion detection pipeline fusing a calibrated classifier, Isolation Forest,
        and a denoising autoencoder over Redis streams, with Suricata EVE ingestion and a one-command
        offline replay demo. 160 tests, 84% coverage — and an acceptance harness that still refuses to
        pass the detector. Every result is public, including the failures.
      </p>
      <p align="center">
        <a href="https://github.com/sting-raider/AegisFlow">repo</a> ·
        <a href="https://github.com/sting-raider/AegisFlow#quick-start">offline demo</a>
      </p>
      <p align="center">
        <code>Python</code> <code>FastAPI</code> <code>Suricata</code>
        <code>PyTorch</code> <code>React</code> <code>Docker</code>
      </p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3 align="center">
        <a href="https://github.com/sting-raider/Plaid">Plaid</a>
      </h3>
      <p align="center">
        <sub>N64 ROMs to native applications — a research work in progress</sub>
      </p>
      <p>
        An experimental toolchain aiming to discover executable code in N64 ROMs and
        statically recompile it into native x86-64 / ARM64 applications. Currently building
        the <a href="https://github.com/sting-raider/Plaid/blob/main/docs/STATUS.md">Rust discovery foundation</a>: control-flow analysis, trace evidence, and
        fail-closed verification. Whole-ROM closure and native execution are still ahead.
      </p>
      <p align="center">
        <a href="https://github.com/sting-raider/Plaid">repo</a> ·
        <a href="https://github.com/sting-raider/Plaid/blob/main/docs/STATUS.md">research status</a>
      </p>
      <p align="center">
        <code>Rust</code> <code>Python</code> <code>MIPS</code>
        <code>Static Recompilation</code> <code>N64</code>
      </p>
    </td>
    <td width="50%" valign="top">
      <h3 align="center">
        <a href="https://sting-raider.github.io/portfolio/projects/robotic-arm/">6-DOF Arm RL</a>
      </h3>
      <p align="center">
        <sub>PPO reaches, a servo closes the gripper</sub>
      </p>
      <p>
        An Isaac Lab pick-and-place system for a UR10e with a Robotiq gripper: a PPO policy learns
        staged reaching, grasping, lifting, and placement. Repo currently private —
        <a href="https://sting-raider.github.io/portfolio/projects/robotic-arm/">full write-up lives on the portfolio</a>.
      </p>
      <p align="center">
        <a href="https://sting-raider.github.io/portfolio/projects/robotic-arm/">write-up</a>
      </p>
      <p align="center">
        <code>Python</code> <code>Isaac Lab</code> <code>PyTorch</code>
        <code>PPO</code> <code>Robotics</code>
      </p>
    </td>
  </tr>
</table>

<details>
  <summary><b>more builds hiding down here</b> ✨</summary>
  <br />
  <table>
    <tr>
      <td width="50%" valign="top">
        <a href="https://github.com/sting-raider/unthinkable-summarizeee"><b>The Abstract</b></a> —
        client-side PDF/OCR summarizer with a DeepSeek backend and a
        <a href="https://unthinkable-summarizeee.vercel.app/">live deployment</a>.
        Built, tested, and shipped in an evening.<br />
        <sub><code>TypeScript</code> <code>Tesseract.js</code> <code>Vercel</code></sub>
      </td>
      <td width="50%" valign="top">
        <a href="https://github.com/sting-raider/DiscArchive"><b>DiscArchive</b></a> —
        local-first search for DiscordChatExporter Group DM archives. Streams 400 MB+ exports in
        ~50 MB of RAM, searches millions of messages in milliseconds, optional CLIP reverse image search.
        All local. No servers.<br />
        <sub><code>TypeScript</code> <code>FastAPI</code> <code>Meilisearch</code> <code>CLIP</code></sub>
      </td>
    </tr>
    <tr>
      <td width="50%" valign="top">
        <a href="https://github.com/sting-raider/dockerscope"><b>DockerScope</b></a> —
        live Docker resource-waste analyzer: polls every 2 seconds, runs efficiency state machines per
        container, flags the over-provisioned ones, and offers safer right-sizing with one-click cleanup.<br />
        <sub><code>Python</code> <code>FastAPI</code> <code>Docker SDK</code></sub>
      </td>
      <td width="50%" valign="top">
        <a href="https://sting-raider.github.io/portfolio/"><b>+ the rest</b></a> — a <a href="https://github.com/sting-raider/hybrid-cloud-k8s-platform">hybrid K3s
        edge/cloud cluster</a> spanning on-prem, AWS, and GCP, and an
        <a href="https://sting-raider.github.io/portfolio/">Undertale-themed portfolio</a> I may have
        spent too long on.
      </td>
    </tr>
  </table>
  <br />
</details>

## toolbox

<p align="center">
  <a href="https://skillicons.dev">
    <img
      src="https://skillicons.dev/icons?i=py,ts,rust,java,bash&theme=dark"
      alt="Python, TypeScript, Rust, Java, Bash"
    />
  </a>
  <br />
  <a href="https://skillicons.dev">
    <img
      src="https://skillicons.dev/icons?i=pytorch,react,nextjs,fastapi,postgres,docker&theme=dark"
      alt="PyTorch, React, Next.js, FastAPI, PostgreSQL, Docker"
    />
  </a>
  <br />
  <a href="https://skillicons.dev">
    <img
      src="https://skillicons.dev/icons?i=kubernetes,redis,ghactions,linux,vercel&theme=dark"
      alt="Kubernetes, Redis, GitHub Actions, Linux, Vercel"
    />
  </a>
</p>

## SAVE file · contribution history

<p align="center">
  <a href="https://github.com/sting-raider?tab=overview">
    <img src="./assets/activity.svg" width="100%" alt="Daily updated contribution heatmap, weekly activity chart, last-year contributions and all-time public PR totals" />
  </a>
</p>

<sub>Generated daily from GitHub's public contribution calendar and PR search. PR counts cover public authored PRs; contributions follow GitHub's calendar visibility.</sub>

## tiny engineering manifesto

- A working system beats a beautiful mock-up.
- An evaluation should tell me *how* something failed, not merely that it failed.
- When the data says the model is wrong, the data wins — publish it anyway.
- AI recommendations should be traceable instead of pretending to be magic.
- If a boring process can be automated, I will probably over-automate it.

## find me

<p align="center">
  <a href="mailto:alizaydsab@gmail.com">
    <img alt="Email" src="https://img.shields.io/badge/Email-alizaydsab%40gmail.com-E24C81?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  <a href="https://www.linkedin.com/in/ali-khan-4197b1217/">
    <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-ali--khan-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://sting-raider.github.io/portfolio/">
    <img alt="Portfolio" src="https://img.shields.io/badge/Portfolio-al's_dark_world-8B5CF6?style=for-the-badge&logo=githubpages&logoColor=white" />
  </a>
</p>

## bonus encounter · contribution snake

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/sting-raider/sting-raider/output/github-snake-dark.svg"
    />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://raw.githubusercontent.com/sting-raider/sting-raider/output/github-snake.svg"
    />
    <img
      alt="Animated contribution snake"
      src="https://raw.githubusercontent.com/sting-raider/sting-raider/output/github-snake.svg"
    />
  </picture>
</p>

<p align="center">
  <sub>thanks for visiting — please do not feed the experimental robots ♡</sub>
</p>
