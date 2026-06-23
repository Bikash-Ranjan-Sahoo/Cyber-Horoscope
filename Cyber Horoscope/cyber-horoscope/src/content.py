"""
CyberHoroscope — Content Module
=================================
All static content pools: prophecies, roast messages, lucky charms,
and lucky numbers. Kept separate from logic so content can be updated
without touching the scoring engine.

Tone: funny-but-educational. The user laughs first, then learns something.
"""

CONTENT: dict = {

    # ─────────────────────────────────────────────
    # PHISHING PROPHECIES
    # ─────────────────────────────────────────────
    "phishing_prophecies": {
        "high": [  # phishing_risk_pct >= 60
            "A mysterious email promising free AWS credits shall appear today. Resist temptation.",
            "A Nigerian prince has marked you as 'easy target of the month'. Congratulations.",
            "The stars see you hovering over 'CLICK HERE TO WIN'. Step away from the mouse.",
            "An email claiming your Netflix account has been suspended will arrive. It has not. Do not click.",
            "Your inbox is a phishing tournament bracket. You are seeded #1.",
            "A message from 'Apple Suport' will land today. Note the spelling. Note it well.",
        ],
        "medium": [  # phishing_risk_pct 30–59
            "An unverified sender will offer you something too good to be true. It is.",
            "Mercury is in phishing retrograde. Verify sender addresses twice today.",
            "The cosmic algorithm suggests hovering over links before clicking. The stars have spoken.",
            "A discount too large to be real will tempt you. Check the domain. Twice.",
        ],
        "low": [  # phishing_risk_pct < 30
            "Your phishing radar is finely tuned. Scammers have your address on a do-not-contact list.",
            "You are the natural predator of the phishing email. They fear you.",
            "The dark web's marketing team has removed you from their cold-outreach list.",
        ],
    },

    # ─────────────────────────────────────────────
    # PASSWORD PROPHECIES
    # ─────────────────────────────────────────────
    "password_prophecies": {
        "high": [  # password_raw >= 20
            "The stars suggest that 'Password123' is not the legendary shield you believe it is.",
            "Your password was last seen in 47 data breaches. It is tired. Retire it.",
            "Aries@123 has filed for retirement. A password manager is actively hiring.",
            "The cosmos sees you using your pet's name as a password. Your pet is embarrassed.",
            "Your password is on a first-name basis with every hacker forum moderator.",
            "haveibeenpwned.com has dedicated a memorial page to your credentials.",
        ],
        "medium": [  # password_raw >= 10
            "Your passwords are like a deadbolt on a screen door — present, but not protective.",
            "The cosmos whispers: length + randomness = destiny. Consider a passphrase.",
            "You have some strong passwords and some weak ones. The weak ones are having a party.",
            "Your password hygiene is improving. The dark web is cautiously disappointed.",
        ],
        "low": [  # password_raw < 10
            "Your password aura radiates strength. The dark web has moved on to easier targets.",
            "A password manager and 20-character random strings — the universe smiles upon you.",
            "Hackers see your credentials and close their laptops in quiet defeat.",
        ],
    },

    # ─────────────────────────────────────────────
    # WI-FI PROPHECIES
    # ─────────────────────────────────────────────
    "wifi_prophecies": {
        "high": [  # wifi_raw >= 30
            "Avoid any network named 'FreeAirportWiFi_NoScam'. Especially that one.",
            "A rogue access point disguised as your local café network awaits. Bring a VPN.",
            "The man-in-the-middle has reserved a table for three: you, him, and your bank details.",
            "The stars warn: 'Free_Hotel_WiFi_Totally_Legit' is neither free nor legitimate.",
            "Your unpatched software is broadcasting 'please attack me' on all frequencies.",
            "Three threat actors have you bookmarked. One sends a holiday card every year.",
        ],
        "medium": [  # wifi_raw >= 15
            "Public Wi-Fi beckons today. A VPN shall be your amulet.",
            "The cosmic firewall suggests enabling auto-updates before connecting to public networks.",
            "Your digital karma is wobbly. A VPN and a patch or two would restore cosmic balance.",
        ],
        "low": [  # wifi_raw < 15
            "Your Wi-Fi karma is pristine. You may safely update that 4GB game patch.",
            "Auto-updates enabled, VPN active — the network gods are pleased.",
            "Your digital hygiene has rendered you invisible to passive network scanners.",
        ],
    },

    # ─────────────────────────────────────────────
    # DATA LEAK PROPHECIES
    # ─────────────────────────────────────────────
    "data_leak_prophecies": {
        "high": [  # leak_raw >= 55
            "Three data brokers are currently bidding on your email address. The auction closes at midnight.",
            "haveibeenpwned.com has a fan page dedicated to your credentials.",
            "Your personal data has visited more countries than you have.",
            "Your email address is on so many breach lists it has its own Wikipedia disambiguation page.",
            "A threat intelligence firm has named a vulnerability after your browsing habits.",
        ],
        "medium": [  # leak_raw >= 25
            "A minor tremor in the data leak cosmos. Enable breach alerts on your email.",
            "The stars suggest checking haveibeenpwned.com this week. Just to be safe.",
            "Your data is partially exposed. Not a full breach — more of a slow drip.",
        ],
        "low": [  # leak_raw < 25
            "Your data footprint is impressively small. The dark web is unaware of your existence.",
            "Zero known breaches. You are a ghost in the data ecosystem. Respect.",
            "Your credentials remain private. The universe nods approvingly.",
        ],
    },

    # ─────────────────────────────────────────────
    # DAILY SECURITY PROPHECIES
    # Shown to every user regardless of score — one picked at random.
    # ─────────────────────────────────────────────
    "daily_security_prophecies": [
        "An unknown USB drive shall cross your path today. The stars advise caution.",
        "Mercury is in malware retrograde. Update your antivirus before leaving the house.",
        "A pop-up shall claim your computer has 47 viruses. It is lying. Close the tab.",
        "Someone will ask for your OTP 'just to verify your account'. They are lying.",
        "A certificate warning shall appear in your browser today. Heed it.",
        "A software update notification will feel inconvenient. Install it anyway.",
        "The stars align for enabling a password manager. Today is the day.",
        "A stranger will offer to charge your phone with their cable. Decline politely.",
        "Today's lucky action: lock your screen before stepping away from your desk.",
        "The cosmos recommends reviewing which apps have access to your location.",
        "A phishing email crafted with alarming attention to detail awaits your inbox.",
        "Today is an auspicious day to enable login notifications on your bank account.",
        "The universe suggests that 'your IT department' texting you for a password is suspicious.",
        "Cosmic forces advise: social engineers often call on Monday mornings. Stay alert.",
        "Today's prophecy: that browser extension you installed last month needs a review.",
    ],

    # ─────────────────────────────────────────────
    # LUCKY SECURITY CHARMS
    # Actionable educational tips — always shown.
    # ─────────────────────────────────────────────
    "lucky_security_charms": [
        "Enable Two-Factor Authentication on your email account.",
        "Check haveibeenpwned.com to see if your email appeared in a breach.",
        "Install a reputable password manager (Bitwarden is free and open-source).",
        "Enable auto-updates on your OS and browser.",
        "Use a VPN on public Wi-Fi networks.",
        "Review which apps have access to your Google/Apple account this week.",
        "Turn on login notifications for your bank account.",
        "Set a 6-digit PIN (not a 4-digit one) on your phone's lock screen.",
        "Revoke OAuth access for any app you no longer use.",
        "Freeze your credit at the major bureaus — it's free and prevents new account fraud.",
        "Back up your important files using the 3-2-1 rule: 3 copies, 2 media types, 1 offsite.",
        "Audit your browser extensions and remove any you don't recognise.",
        "Set your router's admin password to something other than 'admin'.",
    ],

    # ─────────────────────────────────────────────
    # LUCKY SECURITY NUMBERS
    # Well-known ports / numbers from security lore.
    # ─────────────────────────────────────────────
    "lucky_security_numbers": [
        404,    # Not Found — your data should be
        443,    # HTTPS — always prefer it
        1337,   # leet — hacker culture classic
        8080,   # alternate HTTP — proxy favourite
        256,    # AES key size (bits) — solid encryption
        2048,   # RSA key size (bits) — minimum recommended
        3389,   # RDP — "avoid exposing this to the internet"
    ],

    # ─────────────────────────────────────────────
    # ROAST MODE
    # Triggered when final_score >= 70
    # ─────────────────────────────────────────────
    "roast_mode": {
        "messages": [
            "The cybersecurity gods have reviewed your digital habits and are deeply concerned. A formal warning has been issued.",
            "Your password hygiene has been reported to three separate international authorities. Two have responded.",
            "Security researchers have nominated your browser history as a case study in 'what not to do'.",
            "Your cyber spirit animal is an unpatched Windows XP machine running in a hospital. Respect the legacy.",
            "A red team penetration tester looked at your answers and asked to be reassigned.",
            "The CISO of a Fortune 500 company reviewed your score and took a personal day.",
            "Your digital security posture has been classified as a 'critical infrastructure vulnerability' by three NATO members.",
            "Threat actors have rated your defences as 'disappointingly easy' in their internal Slack. One left a tip.",
        ],
    },
}


# ── Developer Mode Content ──────────────────────────────────────────────────
# Added in v2.0.0. The CONTENT dict above is unchanged.

DEV_CONTENT: dict = {
    "secret_prophecies": {
        "high": [
            "A GitHub Actions bot has already found your AWS key. It emailed the billing team.",
            "Your .env file has been committed, pushed, and indexed by three search engines.",
            "The spirits warn: 'AWS_SECRET_KEY=supersecret123' is not a secret. It is a confession.",
            "A threat actor is thanking you in their group chat for the hardcoded Stripe key.",
        ],
        "medium": [
            "Your config file sits one accidental git add away from infamy. Back away slowly.",
            "The cosmos sees a secret living where it should not. Move it to a secrets manager today.",
        ],
        "low": [
            "Your secrets are sealed, rotated, and properly stored. The dark web has given up on you.",
        ],
    },
    "dependency_prophecies": {
        "high": [
            "node_modules contains 47 transitive dependencies last updated in 2019. Three are sentient.",
            "A critical CVE in your auth library was patched six months ago. You were never informed.",
            "npm audit returns 1,337 vulnerabilities. You have chosen to ignore all of them. Bold.",
            "The stars align on Log4Shell energy. Your dependency tree is a historical artefact.",
        ],
        "medium": [
            "A moderate CVE in your ORM awaits your attention. It is not urgent. It is also not not urgent.",
            "Dependabot has opened 14 PRs since January. They are patient. You should not be.",
        ],
        "low": [
            "Your dependencies are patched, pinned, and scanned. Supply chain attackers have moved on.",
        ],
    },
    "environment_prophecies": {
        "high": [
            "You ran a DELETE query on prod thinking it was staging. The database remembers.",
            "A real customer's email address is sitting in your local dev logs. GDPR is watching.",
            "The prod database is your rubber duck. This is not the intended use of a rubber duck.",
            "You will push console.log('PROD DATA:', user) to production today. The stars have seen it.",
        ],
        "medium": [
            "A quick prod test awaits today. It will not be quick. Nothing is ever quick in prod.",
            "The line between staging and production grows thin. Reinforce it today.",
        ],
        "low": [
            "Your environments are isolated, your test data anonymised. DevOps angels watch over you.",
        ],
    },
    "code_integrity_prophecies": {
        "high": [
            "You pushed directly to main at 4:59 PM on a Friday. The deployment pipeline felt it.",
            "A force push has overwritten a colleague's work. They have not noticed yet.",
            "The spirits see a commit message that says 'fix'. It is unclear what was fixed.",
            "Branch protection is off. This is fine. Everything is fine. (It is not fine.)",
        ],
        "medium": [
            "A PR sits unreviewed for its third day. The code inside ages like milk, not wine.",
            "Your branch protection rules have exceptions. Someone will exploit one today.",
        ],
        "low": [
            "Your commits are signed, your PRs reviewed, your main branch protected. You may rest.",
        ],
    },
    "error_exposure_prophecies": {
        "high": [
            "Your 500 error page contains a full stack trace, the DB schema, and your home IP.",
            "A curious user found your /debug endpoint. It is not password protected. They are taking notes.",
            "The exception message 'NullPointerException at UserService.java:247' has been screenshot.",
            "Your error logs are public. A penetration tester is reading them right now and smiling.",
        ],
        "medium": [
            "A verbose error message will slip through to production today. It will contain more than intended.",
            "Your staging errors are detailed. Your prod errors are sometimes also detailed. Sometimes.",
        ],
        "low": [
            "Your errors are generic to users and detailed only in secured logs. Attackers learn nothing.",
        ],
    },
    "daily_dev_prophecies": [
        "A dependency you have never heard of is responsible for 40% of your attack surface. Run npm audit.",
        "Someone will push credentials to a public repo today. The stars hope it is not you.",
        "Mercury is in CVE retrograde. Do not deploy today without reading the changelog.",
        "An intern will ask why the API key is in the README. You will not have a good answer.",
        "A forgotten S3 bucket left public in 2022 will resurface today. Check your AWS console.",
        "Your Docker image runs as root. The container security gods are disappointed but not surprised.",
        "A SQL query built by string concatenation is waiting for its moment. Use parameterised queries.",
        "The .gitignore file has a gap. It always has a gap. Today you will find it.",
        "CORS is set to '*' somewhere in your codebase. It is waving at everyone.",
        "The ghost of a deleted branch still lives in someone's local clone. It contains secrets.",
    ],
    "lucky_dev_charms": [
        "Run truffleHog or git-secrets to scan your repo history for leaked credentials.",
        "Enable Dependabot on your repo — automated dependency PRs take 5 minutes to set up.",
        "Add branch protection to main: require at least 1 review and passing CI before merge.",
        "Move all secrets to AWS Secrets Manager or Parameter Store and rotate them today.",
        "Add 'npm audit --audit-level=high' as a required CI step to block deploys on critical CVEs.",
        "Set up separate AWS accounts for dev, staging, and prod under AWS Organizations.",
        "Add a generic error handler: log full traces internally, return only a reference ID to users.",
        "Enable CloudTrail in your AWS account — it records every API call free for 90 days.",
        "Run trivy or docker scout on your container images before pushing to prod.",
        "Sign your commits with GPG — GitHub shows a Verified badge and setup takes 10 minutes.",
    ],
    "lucky_dev_numbers": [443, 22, 8080, 3306, 9200, 1337, 4040, 6379],
    "dev_roast_messages": [
        "The OWASP Top 10 is not a bucket list. And yet here we are.",
        "Three CVEs, two prod incidents, and one hardcoded password walk into a bar. The bartender is your CTO.",
        "Security researchers have bookmarked your GitHub. Not as a reference. As a cautionary tale.",
        "Your application has been pentested by accident — a script kiddie stumbled in and left a note.",
        "The words 'it works on my machine' have been entered as evidence.",
    ],
}
