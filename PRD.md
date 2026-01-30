
SOROSURANCE PRD
Hackathon Goal: Build a voice-first, AI-powered insurance platform for Nigeria that handles claims, underwriting, and payments, while delivering an exceptional customer experience.
1. Core Feature Focus
The “core” in your hackathon project is where value is created. Based on your notes, the core is a combination of:
	•	Underwriting (Custom AI Soro-Score) – This is the intelligence that evaluates risk and determines premiums and claim recommendations.
	•	Customer Experience (Voice-first, inclusive, intuitive UI) – The AI Orb, keyword bubbles, claim receipt cards, and voice notifications make insurance accessible to low-literacy users.
Product distribution (widgets, USSD flows) and payment pipelines are enablers, not the “core” value—they help people access the system and complete transactions, but the AI decision-making + UX is what makes Sorosurance stand out.
2. Features
A. Product Distribution
	•	Embedded Voice-to-Buy Widget: JS snippet to embed in partners’ platforms (pension apps, blogs, e-commerce).
	•	Hybrid USSD Flow: Africa’s Talking triggers voice call → audio recorded → sent to backend for transcription.
B. Underwriting
	•	Soro-Score Algorithm: Processes voice + image + metadata to calculate risk.
	•	Variables: Inconsistency (40%), Urgency/Sentiment (20%), Media Integrity (25%), Historical Data (15%).
	•	Returns Risk Level (0–100) for auto-approval or manual review.
C. Payment
	•	RedPay / Paystack Integration: Voice-triggered payment for deductibles and premium renewals.
	•	Dynamic Premium Calculation: Adjusted in real-time based on Soro-Score.
D. User Experience
	•	Soro Interface / AI Orb:
	•	Color-changing feedback (green/red) based on recording quality.
	•	Real-time keyword bubbles.
	•	High-contrast claim receipt cards with QR code.
	•	Closing the Loop: Voice notifications via WhatsApp/Robocall for claim updates.
E. Admin Experience
	•	Heirs Reviewer Dashboard:
	•	Risk heatmap by Soro-Score.
	•	Voice sentiment highlights.
	•	One-click payment approval.

TEAM ROLES & RESPONSIBILITIES

1. UI / UX DESIGNER
	•	Design end-to-end user flow (Voice → Claim → Receipt → Payment).
	•	Design AI Orb states (idle, listening, processing, error).
	•	Design Voice Claim Page (icon-first, low-text UI).
	•	Design Keyword Bubble visual feedback system.
	•	Design Claim Receipt Card (high contrast + QR code).
	•	Design Payment Confirmation Screen.
	•	Design Admin Dashboard UI (Risk Heatmap, Claim Cards).
	•	Design Admin Claim Detail View (voice summary, actions).
	•	Define color meanings & motion rules (green/red/orange).
	•	Ensure accessibility (elderly & low-literacy users).
	•	Create mobile-first wireframes.
	•	Deliver high-fidelity Figma prototype.
	•	Share design system (colors, icons, components).
	•	Hand off interactive prototype link to frontend.
Deliverables:
	•	Figma file
	•	Clickable prototype
	•	Design system
2. FRONTEND DEVELOPER
	•	Set up frontend project (React/Vite).
	•	Build Embedded Voice-to-Buy Widget (JS snippet).
	•	Implement AI Orb component (volume-based animation).
	•	Implement Audio Recording (mic permissions + recording).
	•	Stream recorded audio to backend.
	•	Render real-time keyword bubbles.
	•	Handle recording states (idle, listening, error).
	•	Build Claim Receipt Page (QR code generation).
	•	Build Payment Page (RedPay/Paystack UI).
	•	Build Admin Dashboard UI.
	•	Build Risk Heatmap UI.
	•	Implement Voice Playback & AI summary display.
	•	Connect frontend to backend APIs.
	•	Handle loading, error, and success states.
	•	Ensure mobile responsiveness.
	•	Prepare demo-ready flows.
Deliverables:
	•	Working web app
	•	Embedded widget demo
	•	Admin dashboard frontend
3. BACKEND DEVELOPER
	•	Set up backend service (Django / Flask / FastAPI).
	•	Implement audio upload & storage.
	•	Integrate voice transcription service.
	•	Detect language & sentiment from voice.
	•	Extract keywords from transcript.
	•	Build Soro-Score underwriting algorithm.
	•	Implement risk scoring logic (0–100).
	•	Perform metadata & inconsistency checks.
	•	Store & query historical claim data.
	•	Generate AI claim summary.
	•	Recommend auto-approve / investigate.
	•	Calculate dynamic premium / deductible.
	•	Integrate RedPay / Paystack payment API.
	•	Handle payment webhooks & confirmation.
	•	Build Admin APIs (approve, reject, disburse).
	•	Integrate Africa’s Talking (voice + USSD).
	•	Implement Talk-Back notifications (voice updates).
	•	Secure APIs & manage errors.
	•	Prepare demo dataset & logs.
Deliverables:
	•	Backend APIs
	•	Soro-Score engine
	•	Payment + notification services



