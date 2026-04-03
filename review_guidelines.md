# Code Review Guidelines for Phishing Detection Project

## Project Overview
This repository contains an AI-powered email phishing detection system leveraging Google Gemini API with a browser extension interface for real-time threat analysis.

## Review Focus Areas

### 1. Primary Goal: Maximize Recall (Minimize False Negatives)
**Priority**: CRITICAL

- Focus on phishing email text classification with **high recall** to minimize missed threats
- False negatives (missing real phishing attempts) are more costly than false positives
- Target: 100% recall even if it means accepting moderate false positive rate
- Review whether the prompt engineering adequately captures all common phishing indicators

### 2. Security-First Design
**Priority**: CRITICAL

Please evaluate:
- **API Security**: Is the Flask API properly secured? Authentication needed?
- **Secrets Management**: Are API keys and credentials handled safely?
- **Input Validation**: Can malicious input exploit the system?
- **Privacy**: How is sensitive email data protected when sent to external APIs?

### 3. Prompt Engineering Effectiveness
**Priority**: HIGH

This project uses advanced prompt engineering rather than traditional ML training. Assess:
- **Few-Shot Learning**: Are the 3 example analyses effective for teaching the LLM?
- **Analysis Framework**: Does the 5-dimensional evaluation (sender, urgency, links, grammar, actions) cover all phishing tactics?
- **Structured Output**: Is the JSON output format consistently parseable?
- **Edge Cases**: How well does it handle sophisticated attacks (BEC, spear phishing, CEO fraud)?

### 4. Phishing Detection Robustness
**Priority**: HIGH

Evaluate how well the system handles:
- **Common Tactics**: Urgency language, spoofed senders, malicious links, social engineering
- **Advanced Techniques**: Business Email Compromise (BEC), typosquatting, homograph attacks
- **Evolving Threats**: Can the system adapt to new phishing patterns without retraining?
- **False Positive Management**: How to reduce false positives while maintaining 100% recall?

### 5. Code Quality & Maintainability
**Priority**: MEDIUM

Standard code review criteria:
- PEP 8 compliance
- Modular design and separation of concerns
- Error handling and edge cases
- Documentation quality (docstrings, comments, README)

### 6. Deployment & Production Readiness
**Priority**: MEDIUM

Consider:
- **Scalability**: Can the system handle production load?
- **Rate Limiting**: How are API limits (15 req/min) managed?
- **Monitoring**: What telemetry/logging is in place?
- **User Experience**: Is the browser extension intuitive and responsive?

### 7. Ethical & Responsible AI
**Priority**: MEDIUM

Important considerations:
- **Transparency**: Do users know their data is sent to Google Gemini API?
- **Bias**: Are there potential biases in phishing detection (language, region, sender type)?
- **Explainability**: Can users understand why something was flagged?
- **Privacy**: GDPR/privacy compliance for email analysis

## Specific Questions for Reviewers

1. **Recall vs Precision Tradeoff**: The current system prioritizes recall (100%) over precision (43%). Is this the right tradeoff for a security tool? How can precision be improved without sacrificing recall?

2. **Missing Features**: What critical phishing detection features are missing?
   - Email header analysis (DMARC, SPF, DKIM)?
   - URL reputation checking against blacklists?
   - Attachment analysis?
   - Sender reputation scoring?

3. **Prompt Injection Risk**: Since this uses an LLM, could a sophisticated attacker craft an email that manipulates the AI into misclassification?

4. **Scalability Concerns**: The free tier Gemini API has 15 requests/minute limit. What happens when users exceed this? How should it be architected for production?

5. **Browser Extension Security**: What permissions does the extension request? Are they justified? What's the attack surface?

6. **Continuous Learning**: The system has no feedback loop. Should user corrections be collected to improve the system over time?

## Success Criteria

A successful review should:
 Identify at least 3 critical security vulnerabilities or risks
 Propose concrete improvements to increase detection accuracy
 Assess the prompt engineering strategy's effectiveness
 Evaluate the false positive rate and suggest mitigation strategies
 Comment on production readiness and deployment risks
 Discuss ethical considerations specific to phishing detection tools

## Out of Scope

Please do NOT review:
-  The Gemini API itself (external dependency)
-  Phishing dataset quality (Kaggle third-party data)
-  Icon design or aesthetic UI elements
-  Performance optimization beyond critical bottlenecks

## Additional Context

**Project Constraints**:
- Must use free-tier APIs only (no paid services)
- Designed for defensive security purposes only
- Academic project with educational goals
- Browser extension must work on Chrome and Firefox

**Known Limitations** (already acknowledged):
- English-only optimization
- No offline mode (requires internet + API)
- Limited to 82,487 sample dataset evaluation (API costs)
- 57% false positive rate on legitimate emails

**GitHub Repository**: https://github.com/BengalPirate/Fraud_detection_Tool

---

*These guidelines help focus the AI code review on the most critical aspects of a phishing detection system while acknowledging the project's constraints and goals.*
